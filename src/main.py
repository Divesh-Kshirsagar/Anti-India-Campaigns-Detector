"""
Main runner for Twitter Scraper v1.0
Enhanced command-line interface with queue management
"""

import asyncio
import sys
import os

# Ensure we can import from the twitter module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from twitter.main import main as twitter_main
    
    if __name__ == "__main__":
        asyncio.run(twitter_main())
        
except ImportError as e:
    print(f"Import error: {e}")
    print("Please make sure playwright and python-dotenv are installed:")
    print("pip install playwright python-dotenv")
    sys.exit(1)
