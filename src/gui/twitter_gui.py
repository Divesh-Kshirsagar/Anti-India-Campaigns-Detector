"""
GUI Module - Enhanced Twitter Scraper Interface
Improved Tkinter-based interface with queue management and real-time status
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import asyncio
import os
import sys
from datetime import datetime
from typing import List, Optional
import queue
import json
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the simplified scraper (TwitterDatabase removed in simplified version)
from twitter.scraper import TwitterScraper
from twitter.config import TwitterConfig

class TwitterScraperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Anti-India Campaign Detector v1.0 - Twitter Scraper")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Variables
        self.search_var = tk.StringVar(value="anti india campaigns")
        self.status_var = tk.StringVar(value="Ready")
        self.progress_var = tk.DoubleVar()
        
        # Queue for thread communication
        self.message_queue = queue.Queue()
        
        # Threading variables
        self.scraping_thread = None
        self.is_scraping = False
        
        # TODO: Database functionality removed in simplified version
        # Next developer should implement TwitterDatabase for queue management
        # self.db = TwitterDatabase()
        
        # Setup GUI
        self.setup_gui()
        
        # Start message queue checker
        self.check_message_queue()
        
    def setup_gui(self):
        """Setup the GUI components"""
        
        # Create main container with padding
        main_container = tk.Frame(self.root, padx=20, pady=20)
        main_container.pack(fill='both', expand=True)
        
        # Title Frame
        self.create_title_frame(main_container)
        
        # Configuration Frame
        self.create_config_frame(main_container)
        
        # Search Frame
        self.create_search_frame(main_container)
        
        # Queue Management Frame
        self.create_queue_frame(main_container)
        
        # Progress Frame
        self.create_progress_frame(main_container)
        
        # Log Frame
        self.create_log_frame(main_container)
        
        # Button Frame
        self.create_button_frame(main_container)
        
        # Update initial status
        self.update_status_display()
    
    def create_title_frame(self, parent):
        """Create title section"""
        title_frame = tk.Frame(parent, bg='#1DA1F2', height=80)
        title_frame.pack(fill='x', pady=(0, 20))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="Anti-India Campaign Detector",
            font=('Arial', 18, 'bold'),
            bg='#1DA1F2',
            fg='white'
        )
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(
            title_frame,
            text="Twitter Scraper v1.0 - Automated Detection System",
            font=('Arial', 10),
            bg='#1DA1F2',
            fg='white'
        )
        subtitle_label.pack()
    
    def create_config_frame(self, parent):
        """Create configuration section"""
        config_frame = tk.LabelFrame(parent, text="Configuration", font=('Arial', 10, 'bold'))
        config_frame.pack(fill='x', pady=(0, 15))
        
        # Status indicators
        status_inner = tk.Frame(config_frame)
        status_inner.pack(fill='x', padx=10, pady=10)
        
        # Credentials status
        creds_valid = TwitterConfig.validate_credentials()
        creds_color = '#28a745' if creds_valid else '#dc3545'
        creds_text = '✅ Valid' if creds_valid else '❌ Invalid'
        
        tk.Label(status_inner, text="Credentials:", font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky='w', padx=(0, 10))
        tk.Label(status_inner, text=creds_text, fg=creds_color, font=('Arial', 9)).grid(row=0, column=1, sticky='w')
        
        # Settings display
        settings = TwitterConfig.get_scraper_settings()
        tk.Label(status_inner, text="Mode:", font=('Arial', 9, 'bold')).grid(row=1, column=0, sticky='w', padx=(0, 10))
        mode_text = 'Headless' if settings['headless'] else 'Visible Browser'
        tk.Label(status_inner, text=mode_text, font=('Arial', 9)).grid(row=1, column=1, sticky='w')
        
        tk.Label(status_inner, text="Data Dir:", font=('Arial', 9, 'bold')).grid(row=2, column=0, sticky='w', padx=(0, 10))
        tk.Label(status_inner, text=settings['data_dir'], font=('Arial', 9)).grid(row=2, column=1, sticky='w')
    
    def create_search_frame(self, parent):
        """Create search input section"""
        search_frame = tk.LabelFrame(parent, text="Search Query", font=('Arial', 10, 'bold'))
        search_frame.pack(fill='x', pady=(0, 15))
        
        search_inner = tk.Frame(search_frame)
        search_inner.pack(fill='x', padx=10, pady=10)
        
        tk.Label(search_inner, text="Custom Search:", font=('Arial', 9)).pack(anchor='w')
        search_entry = tk.Entry(search_inner, textvariable=self.search_var, width=60, font=('Arial', 10))
        search_entry.pack(fill='x', pady=(5, 10))
        
        # Preset buttons
        preset_frame = tk.Frame(search_inner)
        preset_frame.pack(fill='x')
        
        presets = [
            "anti india campaigns",
            "india propaganda", 
            "fake news india",
            "india disinformation"
        ]
        
        for i, preset in enumerate(presets):
            btn = tk.Button(
                preset_frame,
                text=preset,
                command=lambda p=preset: self.search_var.set(p),
                font=('Arial', 8),
                bg='#f8f9fa',
                relief='flat',
                padx=10,
                pady=2
            )
            btn.pack(side='left', padx=(0, 5) if i < len(presets)-1 else 0)
    
    def create_queue_frame(self, parent):
        """Create queue management section"""
        queue_frame = tk.LabelFrame(parent, text="Queue Management", font=('Arial', 10, 'bold'))
        queue_frame.pack(fill='x', pady=(0, 15))
        
        queue_inner = tk.Frame(queue_frame)
        queue_inner.pack(fill='x', padx=10, pady=10)
        
        # Queue controls
        control_frame = tk.Frame(queue_inner)
        control_frame.pack(fill='x', pady=(0, 10))
        
        tk.Button(
            control_frame,
            text="Add to Queue",
            command=self.add_to_queue,
            bg='#17a2b8',
            fg='white',
            font=('Arial', 9, 'bold'),
            padx=15,
            pady=5
        ).pack(side='left', padx=(0, 10))
        
        tk.Button(
            control_frame,
            text="Add Default Queries",
            command=self.add_default_queries,
            bg='#6c757d',
            fg='white',
            font=('Arial', 9),
            padx=15,
            pady=5
        ).pack(side='left', padx=(0, 10))
        
        tk.Button(
            control_frame,
            text="Process HTML Data",
            command=self.process_html_data,
            bg='#6f42c1',
            fg='white',
            font=('Arial', 9),
            padx=15,
            pady=5
        ).pack(side='left', padx=(10, 0))
        
        tk.Button(
            control_frame,
            text="Clear Queue",
            command=self.clear_queue,
            bg='#dc3545',
            fg='white',
            font=('Arial', 9),
            padx=15,
            pady=5
        ).pack(side='left', padx=(10, 0))
        
        # Queue status
        self.queue_status_var = tk.StringVar(value="Queue: 0 pending tasks")
        tk.Label(queue_inner, textvariable=self.queue_status_var, font=('Arial', 9)).pack(anchor='w')
    
    def create_progress_frame(self, parent):
        """Create progress section"""
        progress_frame = tk.LabelFrame(parent, text="Progress", font=('Arial', 10, 'bold'))
        progress_frame.pack(fill='x', pady=(0, 15))
        
        progress_inner = tk.Frame(progress_frame)
        progress_inner.pack(fill='x', padx=10, pady=10)
        
        # Status label
        tk.Label(progress_inner, textvariable=self.status_var, font=('Arial', 9), wraplength=700).pack(anchor='w', pady=(0, 5))
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(progress_inner, mode='indeterminate')
        self.progress_bar.pack(fill='x')
    
    def create_log_frame(self, parent):
        """Create log display section"""
        log_frame = tk.LabelFrame(parent, text="Activity Log", font=('Arial', 10, 'bold'))
        log_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        # Create scrolled text widget
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=8,
            width=80,
            font=('Consolas', 9),
            bg='#f8f9fa',
            fg='#495057',
            wrap=tk.WORD
        )
        self.log_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Add initial log message
        self.add_log("Application started - Ready for scraping")
    
    def create_button_frame(self, parent):
        """Create button section"""
        button_frame = tk.Frame(parent)
        button_frame.pack(fill='x')
        
        # Main action buttons
        self.start_btn = tk.Button(
            button_frame,
            text="Start Scraping",
            command=self.start_scraping,
            bg='#28a745',
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=25,
            pady=10
        )
        self.start_btn.pack(side='left', padx=(0, 10))
        
        self.stop_btn = tk.Button(
            button_frame,
            text="Stop",
            command=self.stop_scraping,
            bg='#dc3545',
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=25,
            pady=10,
            state='disabled'
        )
        self.stop_btn.pack(side='left', padx=(0, 10))
        
        # Utility buttons
        tk.Button(
            button_frame,
            text="Clear Session",
            command=self.clear_session,
            bg='#fd7e14',
            fg='white',
            font=('Arial', 10),
            padx=15,
            pady=10
        ).pack(side='left', padx=(10, 0))
        
        tk.Button(
            button_frame,
            text="Open Data Folder",
            command=self.open_data_folder,
            bg='#17a2b8',
            fg='white',
            font=('Arial', 10),
            padx=15,
            pady=10
        ).pack(side='left', padx=(10, 0))
        
        tk.Button(
            button_frame,
            text="Refresh Status",
            command=self.update_status_display,
            bg='#ffc107',
            fg='black',
            font=('Arial', 10),
            padx=15,
            pady=10
        ).pack(side='right')
    
    def add_log(self, message: str):
        """Add message to log with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        # Insert at the end
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)  # Auto-scroll to bottom
        
        # Keep only last 1000 lines
        lines = self.log_text.get('1.0', tk.END).split('\n')
        if len(lines) > 1000:
            self.log_text.delete('1.0', f'{len(lines) - 1000}.0')
    
    def update_status(self, status: str):
        """Update status display"""
        self.status_var.set(status)
        self.add_log(status)
    
    def add_to_queue(self):
        """Add current search query to queue"""
        query = self.search_var.get().strip()
        if not query:
            messagebox.showwarning("Warning", "Please enter a search query")
            return
        
        try:
            # TODO: Database functionality removed in simplified version
            # Next developer should implement task queue management with TwitterDatabase
            # For now, just add to a simple list for immediate processing
            if not hasattr(self, 'pending_queries'):
                self.pending_queries = []
            
            if query not in self.pending_queries:
                self.pending_queries.append(query)
                self.add_log(f"Added to queue: '{query}'")
            else:
                self.add_log(f"Query already in queue: '{query}'")
            
            self.update_status_display()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add to queue: {str(e)}")
    
    def add_default_queries(self):
        """Add all default queries to queue"""
        try:
            queries = TwitterConfig.DEFAULT_SEARCH_QUERIES
            if not hasattr(self, 'pending_queries'):
                self.pending_queries = []
            
            count = 0
            for query in queries:
                if query not in self.pending_queries:
                    self.pending_queries.append(query)
                    count += 1
            
            self.add_log(f"Added {count} default queries to queue")
            self.update_status_display()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add default queries: {str(e)}")
    
    def process_html_data(self):
        """Process HTML files to extract structured data"""
        if self.is_scraping:
            messagebox.showwarning("Warning", "Scraping in progress. Please wait.")
            return
        
        self.add_log("Starting HTML data processing...")
        self.update_status("Processing HTML files...")
        
        # Start processing in separate thread
        thread = threading.Thread(target=self.run_html_processing_thread)
        thread.daemon = True
        thread.start()
    
    def run_html_processing_thread(self):
        """Run HTML processing in separate thread"""
        try:
            # Create new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Run HTML processing
            result = loop.run_until_complete(self.process_html_async())
            
            # Update GUI on completion
            self.message_queue.put(('log', f"✅ HTML processing completed: {result} files processed"))
            self.message_queue.put(('status', f"HTML processing completed: {result} files"))
            
        except Exception as e:
            self.message_queue.put(('error', f"HTML processing error: {str(e)}"))
    
    async def process_html_async(self):
        """Async HTML processing execution"""
        try:
            # TODO: Database functionality removed in simplified version
            # Next developer should implement TwitterDataProcessor with database
            # For now, just scan for HTML files in data directory
            
            import os
            import glob
            
            html_dir = os.path.join("data", "twitter")
            if not os.path.exists(html_dir):
                return 0
            
            html_files = glob.glob(os.path.join(html_dir, "*.html"))
            
            # TODO: Process HTML files with BeautifulSoup when database is added
            # This is just a placeholder for the next developer
            
            return len(html_files)
            
        except Exception as e:
            logger.error(f"HTML processing error: {str(e)}")
            raise
    
    def clear_queue(self):
        """Clear all pending tasks from queue"""
        if messagebox.askyesno("Confirm", "Clear all pending tasks from queue?"):
            try:
                # This would require a new method in TwitterDatabase
                # For now, just log the action
                self.add_log("Queue clear requested - Feature not implemented yet")
                messagebox.showinfo("Info", "Queue clear feature will be added in next update")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to clear queue: {str(e)}")
    
    def clear_session(self):
        """Clear saved Twitter session"""
        if messagebox.askyesno("Confirm", "Clear saved Twitter session?\nYou will need to login again next time."):
            try:
                from twitter.scraper import TwitterScraper
                scraper = TwitterScraper()
                scraper.clear_session()
                self.add_log("🗑️ Twitter session cleared - fresh login required next time")
                messagebox.showinfo("Success", "Session cleared successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to clear session: {str(e)}")
    
    def update_status_display(self):
        """Update queue and status display"""
        try:
            pending_tasks = self.db.get_pending_tasks()
            count = len(pending_tasks)
            self.queue_status_var.set(f"Queue: {count} pending tasks")
            
            if not self.is_scraping:
                if count > 0:
                    self.status_var.set(f"Ready - {count} tasks in queue")
                else:
                    self.status_var.set("Ready - Queue empty")
        except Exception as e:
            self.add_log(f"Error updating status: {str(e)}")
    
    def start_scraping(self):
        """Start the scraping process"""
        # Validate credentials
        if not TwitterConfig.validate_credentials():
            messagebox.showerror(
                "Credentials Error", 
                "Twitter credentials not configured!\n\n"
                "Please update your .env file with valid credentials:\n"
                "- TWITTER_EMAIL\n"
                "- TWITTER_PASSWORD"
            )
            return
        
        # Check if there are tasks to process
        pending_tasks = self.db.get_pending_tasks()
        if not pending_tasks:
            messagebox.showwarning(
                "No Tasks", 
                "No tasks in queue!\n\n"
                "Please add some search queries to the queue first."
            )
            return
        
        # Update UI state
        self.is_scraping = True
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.progress_bar.start(10)
        
        self.update_status("Starting scraper...")
        self.add_log(f"Starting scraping process with {len(pending_tasks)} tasks")
        
        # Start scraping in separate thread
        self.scraping_thread = threading.Thread(target=self.run_scraper_thread)
        self.scraping_thread.daemon = True
        self.scraping_thread.start()
    
    def stop_scraping(self):
        """Stop the scraping process"""
        self.is_scraping = False
        self.update_status("Stopping scraper...")
        self.add_log("Stop requested - scraper will stop after current task")
    
    def run_scraper_thread(self):
        """Run scraper in separate thread"""
        try:
            # Create new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Run scraper
            loop.run_until_complete(self.run_scraper_async())
            
        except Exception as e:
            self.message_queue.put(('error', f"Scraping error: {str(e)}"))
        finally:
            self.message_queue.put(('completed', None))
    
    async def run_scraper_async(self):
        """Async scraper execution"""
        try:
            settings = TwitterConfig.get_scraper_settings()
            
            async with TwitterScraper(headless=settings['headless']) as scraper:
                self.message_queue.put(('status', "Logging in to Twitter..."))
                
                # Login
                if not await scraper.login():
                    self.message_queue.put(('error', "Login failed!"))
                    return
                
                self.message_queue.put(('status', "Login successful! Processing queue..."))
                
                # Process queue with status updates
                completed_count = 0
                pending_tasks = self.db.get_pending_tasks()
                total_tasks = len(pending_tasks)
                
                for i, task in enumerate(pending_tasks, 1):
                    if not self.is_scraping:  # Check stop flag
                        self.message_queue.put(('status', "Scraping stopped by user"))
                        break
                    
                    if task.id is None:  # Skip tasks without valid ID
                        continue
                    
                    self.message_queue.put(('status', f"Processing task {i}/{total_tasks}: {task.query}"))
                    
                    try:
                        self.db.update_task_status(task.id, 'running')
                        result_file = await scraper.search_and_scrape(task.query, task.id)
                        
                        if result_file:
                            self.db.update_task_status(task.id, 'completed', result_file)
                            completed_count += 1
                            self.message_queue.put(('log', f"✅ Completed: {task.query}"))
                        else:
                            self.db.update_task_status(task.id, 'failed', error_message="Search failed")
                            self.message_queue.put(('log', f"❌ Failed: {task.query}"))
                        
                        # Delay between tasks
                        if i < total_tasks and self.is_scraping:
                            await scraper.random_delay(10, 15)
                            
                    except Exception as e:
                        self.db.update_task_status(task.id, 'failed', error_message=str(e))
                        self.message_queue.put(('log', f"❌ Error in {task.query}: {str(e)}"))
                
                self.message_queue.put(('status', f"Completed {completed_count}/{total_tasks} tasks"))
                
        except Exception as e:
            self.message_queue.put(('error', f"Scraper error: {str(e)}"))
    
    def check_message_queue(self):
        """Check for messages from scraping thread"""
        try:
            while True:
                message_type, data = self.message_queue.get_nowait()
                
                if message_type == 'status':
                    self.update_status(data)
                elif message_type == 'log':
                    self.add_log(data)
                elif message_type == 'error':
                    self.add_log(f"ERROR: {data}")
                    messagebox.showerror("Scraping Error", data)
                elif message_type == 'completed':
                    self.scraping_completed()
                    
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.check_message_queue)
    
    def scraping_completed(self):
        """Handle scraping completion"""
        self.is_scraping = False
        self.progress_bar.stop()
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        
        self.add_log("Scraping process completed")
        self.update_status_display()
        
        # Show completion message
        messagebox.showinfo("Complete", "Scraping process completed!\nCheck the activity log for details.")
    
    def open_data_folder(self):
        """Open the data folder"""
        settings = TwitterConfig.get_scraper_settings()
        data_dir = settings['data_dir']
        
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        try:
            if os.name == 'nt':  # Windows
                os.startfile(data_dir)
            elif os.name == 'posix':  # macOS and Linux
                os.system(f'open "{data_dir}"' if sys.platform == 'darwin' else f'xdg-open "{data_dir}"')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open data folder: {str(e)}")

def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    app = TwitterScraperGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
