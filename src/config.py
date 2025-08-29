"""
Configuration file for Twitter Scraper
"""

# Twitter Login Credentials
TWITTER_CREDENTIALS = {
    "email": "antiindia81@gmail.com",  # From your screenshot
    "password": "your_password_here"   # Replace with actual password
}

# Search Configuration
SEARCH_QUERIES = [
    "anti india campaign",
    "india propaganda", 
    "fake news india",
    "india disinformation",
    "anti indian sentiment"
]

# Scraper Settings
SCRAPER_CONFIG = {
    "headless": False,  # Set to True for headless mode
    "delay_between_searches": (10, 15),  # Min, Max seconds
    "delay_between_actions": (1, 3),     # Min, Max seconds
    "scroll_count": 3,                   # Number of scrolls to load content
    "max_retries": 3                     # Maximum retry attempts
}

# Output Settings
OUTPUT_CONFIG = {
    "data_directory": "data",
    "filename_prefix": "twitter_search_",
    "file_extension": ".html"
}
