"""
Twitter Scraper Module - Version 1.0
Simplified HTML retrieval scraper with session persistence and cookie support

TODO for next developer:
- Implement database functionality (SQLite) for task queue management
- Add structured data extraction using BeautifulSoup
- Implement task status tracking and error handling
- Add data processing pipeline for extracted tweets
- Consider adding async task processing for better performance
"""

import asyncio
import random
import time
import os
import json
import logging
from typing import Optional, Dict, Any, List, Union
from datetime import datetime, timedelta
from dataclasses import dataclass
from playwright.async_api import async_playwright, Browser, Page
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class TwitterCredentials:
    """Twitter login credentials"""
    email: str
    password: str
    username: Optional[str] = None

class TwitterScraper:
    """Simplified Twitter scraper for HTML retrieval only"""
    
    # Updated selectors for current Twitter (X.com)
    SELECTORS = {
        'email_input': 'input[name="text"]',
        'username_input': 'input[name="text"]',  # Same as email, but used after email step
        'next_button': 'button.css-175oi2r:nth-child(6)',
        'next_button_xpath': '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]',
        'next_button_alt': '[data-testid="LoginForm_Login_Button"]',
        'password_input': 'input[name="password"]',
        'login_button': '[data-testid="LoginForm_Login_Button"]',
        'search_input': '[data-testid="SearchBox_Search_Input"]',
        'tweet_selector': '[data-testid="tweet"]'
    }
    
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ]
    
    def __init__(self, headless: Optional[bool] = None):
        self.headless = headless if headless is not None else os.getenv('HEADLESS_MODE', 'false').lower() == 'true'
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.context = None
        self.delay_min = float(os.getenv('DELAY_MIN', '2'))
        self.delay_max = float(os.getenv('DELAY_MAX', '5'))
        self.max_retries = int(os.getenv('MAX_RETRIES', '3'))
        
        # Session persistence
        self.session_file = os.path.join('data', 'twitter_session.json')
        self.session_valid = False
        
    async def __aenter__(self):
        await self.setup_browser()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
    
    async def setup_browser(self) -> None:
        """Setup browser with session persistence"""
        try:
            playwright = await async_playwright().start()
            user_agent = random.choice(self.USER_AGENTS)
            
            # Launch browser with stealth args
            self.browser = await playwright.chromium.launch(
                headless=self.headless,
                args=[
                    '--no-first-run',
                    '--no-default-browser-check',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-features=VizDisplayCompositor',
                    '--disable-web-security',
                    '--no-sandbox',
                    '--disable-dev-shm-usage'
                ]
            )
            
            # Try to load saved session
            saved_session = self._load_session()
            
            # Create context with session if available
            if saved_session:
                logger.info("🔄 Restoring saved session...")
                self.context = await self.browser.new_context(
                    storage_state=saved_session,
                    user_agent=user_agent,
                    viewport={'width': 1920, 'height': 1080},
                    locale='en-US',
                    timezone_id='America/New_York'
                )
            else:
                logger.info("🆕 Creating new session...")
                self.context = await self.browser.new_context(
                    user_agent=user_agent,
                    viewport={'width': 1920, 'height': 1080},
                    locale='en-US',
                    timezone_id='America/New_York'
                )
            
            self.page = await self.context.new_page()
            
            # Add stealth script
            await self.page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
                window.chrome = {
                    runtime: {},
                };
            """)
            
            # Check if session is still valid
            if saved_session:
                self.session_valid = await self._check_login_status()
            
            logger.info(f"Browser setup complete with User-Agent: {user_agent[:50]}...")
            
        except Exception as e:
            logger.error(f"Browser setup failed: {str(e)}")
            raise
    
    async def random_delay(self, min_seconds: Optional[float] = None, max_seconds: Optional[float] = None) -> None:
        """Add random delay"""
        min_sec = min_seconds or self.delay_min
        max_sec = max_seconds or self.delay_max
        delay = random.uniform(min_sec, max_sec)
        await asyncio.sleep(delay)
    
    async def get_credentials(self) -> TwitterCredentials:
        """Get credentials from environment variables"""
        email = os.getenv('TWITTER_EMAIL')
        password = os.getenv('TWITTER_PASSWORD')
        username = os.getenv('TWITTER_USERNAME')  # Optional username for verification
        
        if not email or not password:
            raise ValueError("Twitter credentials not found in environment variables")
        
        if email == 'your_email@example.com' or password == 'your_password_here':
            raise ValueError("Please update Twitter credentials in .env file")
        
        return TwitterCredentials(email=email, password=password, username=username)
    
    def _load_session(self) -> Optional[Dict]:
        """Load saved session state"""
        try:
            if os.path.exists(self.session_file):
                with open(self.session_file, 'r') as f:
                    session_data = json.load(f)
                    
                # Check if session is not too old (30 days)
                saved_time = datetime.fromisoformat(session_data.get('saved_at', ''))
                if datetime.now() - saved_time < timedelta(days=30):
                    logger.info("✅ Found valid saved session")
                    return session_data['storage_state']
                else:
                    logger.info("🕐 Saved session expired, will login fresh")
                    os.remove(self.session_file)
        except Exception as e:
            logger.warning(f"Failed to load session: {e}")
        return None
    
    def _save_session(self, storage_state: Dict):
        """Save session state to disk"""
        try:
            os.makedirs(os.path.dirname(self.session_file), exist_ok=True)
            session_data = {
                'storage_state': storage_state,
                'saved_at': datetime.now().isoformat()
            }
            with open(self.session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            logger.info(f"✅ Session saved to {self.session_file}")
        except Exception as e:
            logger.error(f"Failed to save session: {e}")
    
    async def _check_login_status(self) -> bool:
        """Check if we're already logged in"""
        try:
            await self.page.goto("https://x.com/home", wait_until='networkidle', timeout=15000)
            current_url = self.page.url
            
            if "home" in current_url or current_url == "https://x.com/":
                logger.info("✅ Already logged in via saved session!")
                return True
            else:
                logger.info("❌ Saved session invalid, need to login")
                return False
        except Exception as e:
            logger.warning(f"Login status check failed: {e}")
            return False
    
    async def login(self, credentials: Optional[TwitterCredentials] = None, cookies_file: Optional[str] = None) -> bool:
        """Login to Twitter with session persistence or cookies"""
        try:
            if not credentials:
                credentials = await self.get_credentials()
            
            if not self.page:
                await self.setup_browser()
            
            # Try to use cookies file if provided
            if cookies_file:
                logger.info(f"🍪 Attempting to use cookies from: {cookies_file}")
                if await self.apply_cookies_from_file(cookies_file):
                    logger.info("✅ Successfully logged in using cookies!")
                    return True
                else:
                    logger.warning("⚠️ Cookie login failed, falling back to regular login...")
            
            # Check if we already have a valid session
            if self.session_valid:
                logger.info("✅ Using existing session, no login needed!")
                return True
            
            logger.info("🔐 Session invalid or not found, performing fresh login...")
            await self.page.goto("https://x.com/i/flow/login", wait_until='networkidle')
            await self.random_delay(2, 4)
            
            # Enter email
            logger.info("📧 Entering email...")
            email_input = await self.page.wait_for_selector(self.SELECTORS['email_input'], timeout=15000)
            await email_input.click()
            await email_input.fill(credentials.email)
            await self.random_delay(1, 2)
            
            # Click next
            logger.info("➡️ Clicking Next button...")
            try:
                # Try the new CSS selector first
                next_button = await self.page.wait_for_selector(self.SELECTORS['next_button'], timeout=10000)
                await next_button.click()
            except Exception as e:
                logger.warning(f"CSS selector failed: {e}")
                try:
                    # Try XPath as fallback
                    next_button = await self.page.wait_for_selector(f"xpath={self.SELECTORS['next_button_xpath']}", timeout=10000)
                    await next_button.click()
                except Exception as e2:
                    logger.warning(f"XPath selector failed: {e2}")
                    # Try alternative data-testid selector
                    next_button = await self.page.wait_for_selector(self.SELECTORS['next_button_alt'], timeout=10000)
                    await next_button.click()
            await self.random_delay(2, 4)
            
            # Check if Twitter is asking for username (suspicious activity)
            logger.info("🔍 Checking if username verification is needed...")
            try:
                # Look for the specific verification screen elements from the screenshot
                verification_detected = False
                
                # Try to find the verification screen title
                try:
                    title_element = await self.page.wait_for_selector(
                        'text="Enter your phone number or username"', 
                        timeout=5000
                    )
                    if title_element:
                        verification_detected = True
                        logger.info("🔍 Username verification screen detected by title!")
                except:
                    pass
                
                # Try to find the placeholder text
                if not verification_detected:
                    try:
                        input_element = await self.page.wait_for_selector(
                            'input[placeholder*="Phone or username"]', 
                            timeout=3000
                        )
                        if input_element:
                            verification_detected = True
                            logger.info("🔍 Username verification screen detected by placeholder!")
                    except:
                        pass
                
                # Try to find the description text
                if not verification_detected:
                    try:
                        desc_element = await self.page.wait_for_selector(
                            'text*="There was unusual login activity"', 
                            timeout=3000
                        )
                        if desc_element:
                            verification_detected = True
                            logger.info("🔍 Username verification screen detected by description!")
                    except:
                        pass
                
                # Fallback: check for any text input after email step
                if not verification_detected:
                    try:
                        # Look for any text input that might be the username field
                        input_element = await self.page.wait_for_selector(
                            'input[name="text"]', 
                            timeout=3000
                        )
                        if input_element:
                            # Check if we're still on a form (not the main Twitter page)
                            page_content = await self.page.content()
                            if "Enter your" in page_content or "verify" in page_content.lower():
                                verification_detected = True
                                logger.info("🔍 Username verification detected by fallback method!")
                    except:
                        pass
                
                if verification_detected:
                    if not credentials.username:
                        logger.error("❌ Twitter is asking for username but TWITTER_USERNAME not set in .env file")
                        return False
                    
                    logger.info(f"👤 Entering username for verification: {credentials.username}")
                    
                    # Find the username input field (try multiple selectors)
                    username_input = None
                    selectors_to_try = [
                        'input[placeholder*="Phone or username"]',
                        'input[name="text"]',
                        'input[type="text"]',
                        'input[data-testid*="ocfEnterTextTextInput"]'
                    ]
                    
                    for selector in selectors_to_try:
                        try:
                            username_input = await self.page.wait_for_selector(selector, timeout=5000)
                            if username_input:
                                logger.info(f"✅ Found username input with selector: {selector}")
                                break
                        except:
                            continue
                    
                    if not username_input:
                        logger.error("❌ Could not find username input field")
                        return False
                    
                    # Clear and fill the username field
                    await username_input.click()
                    await self.random_delay(0.5, 1)
                    await username_input.clear()
                    await self.random_delay(0.5, 1)
                    await username_input.fill(credentials.username)
                    await self.random_delay(1, 2)
                    
                    # Find and click the Next button
                    logger.info("➡️ Clicking Next after username...")
                    next_clicked = False
                    next_selectors = [
                        'div[role="button"]:has-text("Next")',
                        'button:has-text("Next")',
                        '[data-testid*="ocfEnterTextNextButton"]',
                        'div[role="button"][data-testid]:has-text("Next")',
                        'div.css-175oi2r:has-text("Next")'
                    ]
                    
                    for selector in next_selectors:
                        try:
                            next_button = await self.page.wait_for_selector(selector, timeout=5000)
                            if next_button:
                                await next_button.click()
                                logger.info(f"✅ Clicked Next button with: {selector}")
                                next_clicked = True
                                break
                        except Exception as e:
                            logger.debug(f"Next button selector failed: {selector} - {e}")
                            continue
                    
                    if not next_clicked:
                        logger.warning("⚠️ Could not find Next button, trying Enter key...")
                        await self.page.keyboard.press('Enter')
                    
                    await self.random_delay(3, 5)
                    logger.info("✅ Username verification completed")
                else:
                    logger.info("✅ No username verification needed - proceeding to password")
                    
            except Exception as e:
                logger.warning(f"Username verification check failed: {e}")
                # Continue anyway - might still work
            
            
            
            # Enter password
            logger.info("🔒 Entering password...")
            try:
                password_input = await self.page.wait_for_selector(self.SELECTORS['password_input'], timeout=10000)
                await password_input.click()
                await password_input.fill(credentials.password)
                await self.random_delay(1, 2)
                
                # Click login
                logger.info("🚀 Clicking Login button...")
                login_button = await self.page.wait_for_selector(self.SELECTORS['login_button'], timeout=10000)
                await login_button.click()
                
            except Exception as e:
                logger.warning(f"Standard login flow failed: {e}")
                # Try alternative selectors
                password_input = await self.page.wait_for_selector('input[type="password"]', timeout=10000)
                await password_input.click()
                await password_input.fill(credentials.password)
                await self.random_delay(1, 2)
                
                login_button = await self.page.wait_for_selector('div[data-testid="LoginForm_Login_Button"]', timeout=10000)
                await login_button.click()
            
            # Wait for login completion
            await self.random_delay(5, 8)
            
            # Check if login was successful
            current_url = self.page.url
            if "home" in current_url or current_url == "https://x.com/":
                logger.info("✅ Login successful!")
                
                # Save session for future use
                try:
                    storage_state = await self.context.storage_state()
                    self._save_session(storage_state)
                    self.session_valid = True
                    logger.info("💾 Session saved for future use")
                except Exception as e:
                    logger.warning(f"Failed to save session: {e}")
                
                return True
            else:
                logger.error(f"❌ Login failed. Current URL: {current_url}")
                return False
                
        except Exception as e:
            logger.error(f"Login failed with error: {str(e)}")
            return False
    
    async def search_and_scrape(self, query: str) -> Optional[str]:
        """Search Twitter and scrape HTML content - simplified version"""
        try:
            if not self.page:
                logger.error("Browser not initialized")
                return None
            
            logger.info(f"Searching for: {query}")
            
            # Navigate to search URL with retry logic
            search_url = f"https://x.com/search?q={query.replace(' ', '%20')}&src=typed_query&f=live"
            
            # Try navigation with retries
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    await self.page.goto(search_url, wait_until='networkidle', timeout=30000)
                    break
                except Exception as e:
                    logger.warning(f"Navigation attempt {attempt + 1} failed: {e}")
                    if attempt == max_retries - 1:
                        raise
                    await self.random_delay(2, 4)
            
            await self.random_delay(3, 5)
            
            # Wait for page to load initially
            await self.random_delay(2, 3)
            
            # Simple scrolling to load more tweets - using Page Down key for visibility
            scroll_count = int(os.getenv('SCROLL_COUNT', '3'))
            logger.info(f"🔄 Starting to scroll {scroll_count} times (you should see this in browser)...")
            
            for i in range(scroll_count):
                try:
                    # Use Page Down key - this should be visible in the browser
                    await self.page.keyboard.press('PageDown')
                    logger.info(f"📄 Pressed Page Down {i+1}/{scroll_count}")
                    await self.random_delay(2, 3)
                except Exception as e:
                    logger.warning(f"Page Down failed for scroll {i+1}: {e}")
                    # Fallback to JavaScript scroll
                    try:
                        await self.page.evaluate("window.scrollBy(0, 1000)")
                        logger.info(f"🔽 JavaScript scroll {i+1}/{scroll_count}")
                        await self.random_delay(2, 3)
                    except Exception as e2:
                        logger.error(f"Both scroll methods failed: {e2}")
            
            logger.info("✅ Scrolling completed")
            
            # Get HTML content immediately
            logger.info("Getting HTML content...")
            html_content = await self.page.content()
            
            if len(html_content) < 5000:  # Basic check for empty page
                logger.warning(f"HTML content seems small ({len(html_content)} chars) - might be an error page")
            else:
                logger.info(f"✅ Got HTML content: {len(html_content):,} characters")
            
            # Save HTML to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_query = "".join(c for c in query if c.isalnum() or c in (' ', '-', '_')).replace(' ', '_')
            filename = f"twitter_search_{safe_query}_{timestamp}.html"
            
            await self.save_html(html_content, filename)
            
            logger.info(f"✅ Successfully scraped: {query}")
            return filename
            
        except Exception as e:
            logger.error(f"Search failed for '{query}': {str(e)}")
            return None
    
    async def save_html(self, html_content: str, filename: str) -> None:
        """Save HTML content to file in twitter subdirectory"""
        try:
            # Use twitter-specific data directory
            data_dir = os.path.join('data', 'twitter')
            os.makedirs(data_dir, exist_ok=True)
            
            filepath = os.path.join(data_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"✅ HTML saved: {filepath} ({len(html_content):,} chars)")
            
        except Exception as e:
            logger.error(f"❌ Failed to save HTML: {str(e)}")
            raise
    
    async def close(self) -> None:
        """Close browser"""
        if self.browser:
            await self.browser.close()
            logger.info("Browser closed")
    
    def clear_session(self):
        """Clear saved session (force fresh login next time)"""
        try:
            if os.path.exists(self.session_file):
                os.remove(self.session_file)
                logger.info("🗑️ Saved session cleared")
            self.session_valid = False
        except Exception as e:
            logger.error(f"Failed to clear session: {e}")
    
    # TODO for next developer: Implement these database and processing methods
    # def process_queue(self) -> int:
    #     """TODO: Process all pending tasks in the queue using database"""
    #     pass
    # 
    # def add_search_queries(self, queries: List[str]) -> List[int]:
    #     """TODO: Add multiple search queries to the database queue"""
    #     pass
    # 
    # def process_html_data(self) -> int:
    #     """TODO: Process all unprocessed HTML files and extract structured data"""
    #     pass
    # 
    # def scrape_and_process_all(self, queries: List[str]) -> Dict[str, int]:
    #     """TODO: Complete workflow: add queries, scrape HTML, and process data"""
    #     pass
    
    def load_cookies_from_file(self, cookies_file: str) -> bool:
        """Load cookies from a JSON file and apply them to the session"""
        try:
            if not os.path.exists(cookies_file):
                logger.error(f"Cookies file not found: {cookies_file}")
                return False
            
            with open(cookies_file, 'r', encoding='utf-8') as f:
                cookies_data = json.load(f)
            
            # Convert cookies to Playwright storage state format
            storage_state = {
                'cookies': [],
                'origins': []
            }
            
            # Handle different cookie formats
            if isinstance(cookies_data, list):
                # Format: [{name, value, domain, path, ...}, ...]
                for cookie in cookies_data:
                    playwright_cookie = {
                        'name': cookie.get('name', ''),
                        'value': cookie.get('value', ''),
                        'domain': cookie.get('domain', '.x.com'),
                        'path': cookie.get('path', '/'),
                        'expires': cookie.get('expires', -1),
                        'httpOnly': cookie.get('httpOnly', False),
                        'secure': cookie.get('secure', True),
                        'sameSite': cookie.get('sameSite', 'Lax')
                    }
                    storage_state['cookies'].append(playwright_cookie)
                    
            elif isinstance(cookies_data, dict):
                # Handle different dictionary formats
                if 'cookies' in cookies_data:
                    # Already in storage state format
                    storage_state = cookies_data
                else:
                    # Simple name-value pairs: {name: value, ...}
                    for name, value in cookies_data.items():
                        playwright_cookie = {
                            'name': name,
                            'value': str(value),
                            'domain': '.x.com',
                            'path': '/',
                            'expires': -1,
                            'httpOnly': False,
                            'secure': True,
                            'sameSite': 'Lax'
                        }
                        storage_state['cookies'].append(playwright_cookie)
            
            # Save the cookies as a session file
            self._save_session(storage_state)
            logger.info(f"✅ Loaded {len(storage_state['cookies'])} cookies from {cookies_file}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load cookies from file: {e}")
            return False
    
    async def apply_cookies_from_file(self, cookies_file: str) -> bool:
        """Load and apply cookies from file to current browser context"""
        try:
            if not self.context:
                logger.error("Browser context not initialized")
                return False
            
            if not os.path.exists(cookies_file):
                logger.error(f"Cookies file not found: {cookies_file}")
                return False
            
            with open(cookies_file, 'r', encoding='utf-8') as f:
                cookies_data = json.load(f)
            
            cookies_to_add = []
            
            # Handle different cookie formats
            if isinstance(cookies_data, list):
                for cookie in cookies_data:
                    playwright_cookie = {
                        'name': cookie.get('name', ''),
                        'value': cookie.get('value', ''),
                        'domain': cookie.get('domain', '.x.com'),
                        'path': cookie.get('path', '/'),
                        'expires': cookie.get('expires', -1),
                        'httpOnly': cookie.get('httpOnly', False),
                        'secure': cookie.get('secure', True),
                        'sameSite': cookie.get('sameSite', 'Lax')
                    }
                    cookies_to_add.append(playwright_cookie)
                    
            elif isinstance(cookies_data, dict):
                if 'cookies' in cookies_data:
                    cookies_to_add = cookies_data['cookies']
                else:
                    for name, value in cookies_data.items():
                        playwright_cookie = {
                            'name': name,
                            'value': str(value),
                            'domain': '.x.com',
                            'path': '/',
                            'expires': -1,
                            'httpOnly': False,
                            'secure': True,
                            'sameSite': 'Lax'
                        }
                        cookies_to_add.append(playwright_cookie)
            
            # Add cookies to the browser context
            await self.context.add_cookies(cookies_to_add)
            
            # Test if cookies work by checking login status
            self.session_valid = await self._check_login_status()
            
            if self.session_valid:
                # Save as session file for future use
                storage_state = await self.context.storage_state()
                self._save_session(storage_state)
                logger.info(f"✅ Successfully applied {len(cookies_to_add)} cookies and verified login!")
                return True
            else:
                logger.warning("⚠️ Cookies applied but login verification failed")
                return False
                
        except Exception as e:
            logger.error(f"Failed to apply cookies from file: {e}")
            return False
