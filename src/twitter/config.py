"""
Twitter Configuration Module
Handles all Twitter scraper configuration and settings
"""

import os
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TwitterConfig:
    """Twitter scraper configuration"""
    
    # Default search queries for anti-India campaign detection
    DEFAULT_SEARCH_QUERIES = [
        "anti india campaign",
        "india propaganda",
        "fake news india",
        "india disinformation",
        "anti indian sentiment",
        "india bot network",
        "manipulated media india"
    ]
    
    # Twitter selectors (updated for current X.com)
    SELECTORS = {
        'email_input': 'input[name="text"]',
        'next_button': 'button.css-175oi2r:nth-child(6)',
        'next_button_xpath': '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]',
        'next_button_alt': '[data-testid="LoginForm_Login_Button"]',
        'password_input': 'input[name="password"]',
        'login_button': '[data-testid="LoginForm_Login_Button"]',
        'search_input': '[data-testid="SearchBox_Search_Input"]',
        'tweet_selector': '[data-testid="tweet"]',
        'like_button': '[data-testid="like"]',
        'retweet_button': '[data-testid="retweet"]',
        'reply_button': '[data-testid="reply"]'
    }
    
    @classmethod
    def get_credentials(cls) -> Dict[str, str]:
        """Get Twitter credentials from environment"""
        return {
            'email': os.getenv('TWITTER_EMAIL', ''),
            'password': os.getenv('TWITTER_PASSWORD', '')
        }
    
    @classmethod
    def get_scraper_settings(cls) -> Dict[str, Any]:
        """Get scraper settings from environment"""
        return {
            'headless': os.getenv('HEADLESS_MODE', 'false').lower() == 'true',
            'delay_min': float(os.getenv('DELAY_MIN', '2')),
            'delay_max': float(os.getenv('DELAY_MAX', '5')),
            'scroll_count': int(os.getenv('SCROLL_COUNT', '3')),
            'max_retries': int(os.getenv('MAX_RETRIES', '3')),
            'data_dir': os.getenv('DATA_DIR', 'data'),
            'db_path': os.getenv('DB_PATH', 'data/twitter_data.db')
        }
    
    @classmethod
    def validate_credentials(cls) -> bool:
        """Validate that credentials are properly configured"""
        creds = cls.get_credentials()
        return (
            bool(creds['email']) and 
            bool(creds['password']) and
            creds['email'] != 'your_email@example.com' and
            creds['password'] != 'your_password_here'
        )
    
    @classmethod
    def get_user_agents(cls) -> List[str]:
        """Get list of user agents for rotation"""
        return [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
