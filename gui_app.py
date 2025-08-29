"""
Twitter Scraper GUI Application - Main Entry Point
Enhanced Tkinter-based interface for the Anti-India Campaign Detector v1.0
"""

import tkinter as tk
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from gui.twitter_gui import TwitterScraperGUI
except ImportError as e:
    print(f"Import error: {e}")
    print("Please make sure all required packages are installed:")
    print("pip install playwright python-dotenv")
    sys.exit(1)

def main():
    """Main function to run the GUI application"""
    try:
        root = tk.Tk()
        app = TwitterScraperGUI(root)
        root.mainloop()
    except Exception as e:
        print(f"Error starting GUI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
