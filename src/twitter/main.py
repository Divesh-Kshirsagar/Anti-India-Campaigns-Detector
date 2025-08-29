"""
Twitter Scraper Main Runner
Command-line interface for the Twitter scraper
"""

import asyncio
import sys
import os
from typing import List
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from twitter.scraper import TwitterScraper, TwitterCredentials
from twitter.config import TwitterConfig

async def run_single_search(query: str, headless: bool = False) -> bool:
    """Run a single search query"""
    try:
        async with TwitterScraper(headless=headless) as scraper:
            # Login
            if not await scraper.login():
                print(f"❌ Login failed!")
                return False
            
            # Search
            result_file = await scraper.search_and_scrape(query)
            if result_file:
                print(f"✅ Search completed: {result_file}")
                return True
            else:
                print(f"❌ Search failed for: {query}")
                return False
                
    except Exception as e:
        print(f"❌ Error during search: {str(e)}")
        return False

async def run_multiple_searches(queries: List[str], headless: bool = False) -> int:
    """Run multiple search queries"""
    try:
        async with TwitterScraper(headless=headless) as scraper:
            # Add queries to queue
            task_ids = await scraper.add_search_queries(queries)
            print(f"📝 Added {len(task_ids)} tasks to queue")
            
            # Process queue
            completed_count = await scraper.process_queue()
            return completed_count
            
    except Exception as e:
        print(f"❌ Error during batch processing: {str(e)}")
        return 0

async def main():
    """Main entry point"""
    print("=" * 60)
    print("Anti-India Campaign Detector - Twitter Scraper v1.0")
    print("=" * 60)
    
    # Check credentials
    if not TwitterConfig.validate_credentials():
        print("❌ Twitter credentials not configured!")
        print("Please update your .env file with valid Twitter credentials.")
        print("Required variables:")
        print("  - TWITTER_EMAIL")
        print("  - TWITTER_PASSWORD")
        return sys.exit(1)
    
    # Get configuration
    settings = TwitterConfig.get_scraper_settings()
    creds = TwitterConfig.get_credentials()
    
    print(f"📧 Email: {creds['email']}")
    print(f"🤖 Headless Mode: {settings['headless']}")
    print(f"📁 Data Directory: {settings['data_dir']}")
    print(f"💾 Database: {settings['db_path']}")
    print("-" * 60)
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--single" and len(sys.argv) > 2:
            query = " ".join(sys.argv[2:])
            print(f"🔍 Running single search: '{query}'")
            success = await run_single_search(query, settings['headless'])
            sys.exit(0 if success else 1)
        
        elif sys.argv[1] == "--help":
            print("Usage:")
            print("  python main.py                    # Run default batch searches")
            print("  python main.py --single <query>   # Run single search")
            print("  python main.py --help             # Show this help")
            sys.exit(0)
    
    # Run default batch searches
    queries = TwitterConfig.DEFAULT_SEARCH_QUERIES
    print(f"🚀 Starting batch scraping with {len(queries)} queries...")
    print(f"📝 Queries: {', '.join(queries)}")
    print("-" * 60)
    
    start_time = datetime.now()
    completed_count = await run_multiple_searches(queries, settings['headless'])
    end_time = datetime.now()
    duration = end_time - start_time
    
    print("-" * 60)
    print(f"📊 Summary:")
    print(f"   Total queries: {len(queries)}")
    print(f"   Completed: {completed_count}")
    print(f"   Success rate: {(completed_count/len(queries)*100):.1f}%")
    print(f"   Duration: {duration}")
    print(f"   Data saved in: {settings['data_dir']}")
    
    if completed_count > 0:
        print("✅ Scraping completed successfully!")
        sys.exit(0)
    else:
        print("❌ No searches completed successfully!")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Scraping interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        sys.exit(1)
