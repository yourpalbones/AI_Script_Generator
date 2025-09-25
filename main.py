import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import json
import os
from datetime import datetime, timedelta
import time
from scrapers import NewsScraper
from chatgpt_automation import ChatGPTAutomation
from settings_manager import SettingsManager

class ScriptWriterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ScriptWriter - Comedy Commentary Generator")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2b2b2b')
        
        # Initialize components
        self.settings_manager = SettingsManager()
        self.scraper = NewsScraper()
        self.chatgpt = ChatGPTAutomation()
        self.current_topics = []
        self.is_generating = False
        
        # Category options
        self.categories = [
            "US Political News",
            "Ohio Political News",
            "Local Ohio News (Columbiana, Trumbull, Mahoning Counties)",
            "Funny Stories (US National)",
            "Local Funny Stories (Columbiana, Trumbull, Mahoning Counties)",
            "Funny Criminal Stories (US National)",
            "Funny Criminal Stories (Ohio Statewide)",
            "Funny Criminal Stories (Columbiana, Mahoning, Trumbull Counties)"
        ]
        
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2b2b2b')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(main_frame, text="ScriptWriter", 
                              font=('Arial', 24, 'bold'), 
                              fg='#ffffff', bg='#2b2b2b')
        title_label.pack(pady=(0, 20))
        
        # Control panel
        control_frame = tk.Frame(main_frame, bg='#2b2b2b')
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Category selection
        tk.Label(control_frame, text="Category:", 
                font=('Arial', 12), fg='#ffffff', bg='#2b2b2b').pack(side=tk.LEFT, padx=(0, 10))
        
        self.category_var = tk.StringVar(value=self.categories[0])
        self.category_dropdown = ttk.Combobox(control_frame, textvariable=self.category_var,
                                            values=self.categories, state="readonly", width=50)
        self.category_dropdown.pack(side=tk.LEFT, padx=(0, 20))
        
        # Generate button
        self.generate_btn = tk.Button(control_frame, text="Generate Topics", 
                                     command=self.generate_topics,
                                     bg='#4CAF50', fg='white', font=('Arial', 12, 'bold'),
                                     padx=20, pady=5)
        self.generate_btn.pack(side=tk.LEFT, padx=(0, 20))
        
        # Settings button
        settings_btn = tk.Button(control_frame, text="Settings", 
                                command=self.open_settings,
                                bg='#2196F3', fg='white', font=('Arial', 12),
                                padx=20, pady=5)
        settings_btn.pack(side=tk.RIGHT)
        
        # Search/filter frame
        search_frame = tk.Frame(main_frame, bg='#2b2b2b')
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(search_frame, text="Search Topics:", 
                font=('Arial', 12), fg='#ffffff', bg='#2b2b2b').pack(side=tk.LEFT, padx=(0, 10))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_topics)
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, 
                               font=('Arial', 12), width=40)
        search_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # Status label
        self.status_label = tk.Label(search_frame, text="Ready", 
                                    font=('Arial', 10), fg='#888888', bg='#2b2b2b')
        self.status_label.pack(side=tk.RIGHT)
        
        # Topics list frame
        topics_frame = tk.Frame(main_frame, bg='#2b2b2b')
        topics_frame.pack(fill=tk.BOTH, expand=True)
        
        # Topics listbox with scrollbar
        list_frame = tk.Frame(topics_frame, bg='#2b2b2b')
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.topics_listbox = tk.Listbox(list_frame, font=('Arial', 10), 
                                        bg='#3b3b3b', fg='#ffffff', 
                                        selectbackground='#4CAF50',
                                        height=20)
        
        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.topics_listbox.yview)
        self.topics_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.topics_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double-click to generate script
        self.topics_listbox.bind('<Double-1>', self.on_topic_double_click)
        
        # Script generation frame
        script_frame = tk.Frame(main_frame, bg='#2b2b2b')
        script_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.make_script_btn = tk.Button(script_frame, text="Make TikTok Script", 
                                        command=self.make_script,
                                        bg='#FF9800', fg='white', font=('Arial', 12, 'bold'),
                                        padx=20, pady=5, state=tk.DISABLED)
        self.make_script_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.make_facebook_btn = tk.Button(script_frame, text="Make Facebook Post", 
                                          command=self.make_facebook_post,
                                          bg='#4267B2', fg='white', font=('Arial', 12, 'bold'),
                                          padx=20, pady=5, state=tk.DISABLED)
        self.make_facebook_btn.pack(side=tk.LEFT)
        
        # Progress bar
        self.progress = ttk.Progressbar(script_frame, mode='indeterminate')
        self.progress.pack(side=tk.RIGHT, padx=(20, 0), fill=tk.X, expand=True)
    
    def generate_topics(self):
        if self.is_generating:
            return
        
        category = self.category_var.get()
        self.is_generating = True
        self.generate_btn.config(state=tk.DISABLED, text="Generating...")
        self.status_label.config(text=f"Generating topics for {category}...")
        self.progress.start()
        
        # Run scraping in separate thread
        thread = threading.Thread(target=self._scrape_topics, args=(category,))
        thread.daemon = True
        thread.start()
    
    def _scrape_topics(self, category):
        try:
            self.current_topics = self.scraper.scrape_category(category)
            self.root.after(0, self._update_topics_display)
        except Exception as e:
            self.root.after(0, lambda: self._show_error(f"Error generating topics: {str(e)}"))
        finally:
            self.root.after(0, self._scraping_finished)
    
    def _update_topics_display(self):
        self.topics_listbox.delete(0, tk.END)
        for i, topic in enumerate(self.current_topics):
            display_text = f"{topic['title']} | {topic['source']} | {topic['time_ago']} | {topic['timestamp']}"
            self.topics_listbox.insert(tk.END, display_text)
        
        self.status_label.config(text=f"Found {len(self.current_topics)} topics")
        
        # Enable both buttons when topics are loaded
        self.make_script_btn.config(state=tk.NORMAL)
        self.make_facebook_btn.config(state=tk.NORMAL)
    
    def _scraping_finished(self):
        self.is_generating = False
        self.generate_btn.config(state=tk.NORMAL, text="Generate Topics")
        self.progress.stop()
    
    def _show_error(self, message):
        messagebox.showerror("Error", message)
        self.status_label.config(text="Error occurred")
    
    def filter_topics(self, *args):
        search_term = self.search_var.get().lower()
        if not search_term:
            self._update_topics_display()
            return
        
        filtered_topics = [topic for topic in self.current_topics 
                          if search_term in topic['title'].lower() or 
                          search_term in topic['source'].lower()]
        
        self.topics_listbox.delete(0, tk.END)
        for topic in filtered_topics:
            display_text = f"{topic['title']} | {topic['source']} | {topic['time_ago']} | {topic['timestamp']}"
            self.topics_listbox.insert(tk.END, display_text)
    
    def on_topic_double_click(self, event):
        self.make_script()
    
    def make_facebook_post(self):
        selection = self.topics_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a topic first.")
            return
        
        topic_index = selection[0]
        # Find the actual topic (accounting for filtering)
        search_term = self.search_var.get().lower()
        if search_term:
            filtered_topics = [topic for topic in self.current_topics 
                              if search_term in topic['title'].lower() or 
                              search_term in topic['source'].lower()]
            topic = filtered_topics[topic_index]
        else:
            topic = self.current_topics[topic_index]
        
        # Generate Facebook post in separate thread
        self.make_facebook_btn.config(state=tk.DISABLED, text="Generating Post...")
        self.progress.start()
        
        thread = threading.Thread(target=self._generate_facebook_post, args=(topic,))
        thread.daemon = True
        thread.start()
    
    def make_script(self):
        selection = self.topics_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a topic first.")
            return
        
        topic_index = selection[0]
        # Find the actual topic (accounting for filtering)
        search_term = self.search_var.get().lower()
        if search_term:
            filtered_topics = [topic for topic in self.current_topics 
                              if search_term in topic['title'].lower() or 
                              search_term in topic['source'].lower()]
            topic = filtered_topics[topic_index]
        else:
            topic = self.current_topics[topic_index]
        
        # Generate script in separate thread
        self.make_script_btn.config(state=tk.DISABLED, text="Generating Script...")
        self.progress.start()
        
        thread = threading.Thread(target=self._generate_script, args=(topic,))
        thread.daemon = True
        thread.start()
    
    def _generate_script(self, topic):
        try:
            script = self.chatgpt.generate_script(topic, self.settings_manager)
            self.root.after(0, lambda: self._show_script(script, topic))
        except Exception as e:
            self.root.after(0, lambda: self._show_error(f"Error generating script: {str(e)}"))
        finally:
            self.root.after(0, self._script_generation_finished)
    
    def _generate_facebook_post(self, topic):
        try:
            post = self.chatgpt.generate_facebook_post(topic, self.settings_manager)
            self.root.after(0, lambda: self._show_facebook_post(post, topic))
        except Exception as e:
            self.root.after(0, lambda: self._show_error(f"Error generating Facebook post: {str(e)}"))
        finally:
            self.root.after(0, self._facebook_post_generation_finished)
    
    
    def _show_script(self, script, topic):
        # Create new window for script display
        script_window = tk.Toplevel(self.root)
        script_window.title(f"Script: {topic['title'][:50]}...")
        script_window.geometry("800x600")
        script_window.configure(bg='#2b2b2b')
        
        # Title
        title_label = tk.Label(script_window, text=topic['title'], 
                              font=('Arial', 14, 'bold'), 
                              fg='#ffffff', bg='#2b2b2b', wraplength=750)
        title_label.pack(pady=10)
        
        # Script content
        script_text = scrolledtext.ScrolledText(script_window, 
                                               font=('Arial', 11),
                                               bg='#3b3b3b', fg='#ffffff',
                                               wrap=tk.WORD)
        script_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        script_text.insert(tk.END, script)
        script_text.config(state=tk.DISABLED)
        
        # Save button
        save_btn = tk.Button(script_window, text="Save Script", 
                            command=lambda: self._save_script(script, topic),
                            bg='#4CAF50', fg='white', font=('Arial', 12))
        save_btn.pack(pady=10)
    
    def _save_script(self, script, topic):
        filename = f"script_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Topic: {topic['title']}\n")
                f.write(f"Source: {topic['source']}\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("-" * 50 + "\n\n")
                f.write(script)
            messagebox.showinfo("Saved", f"Script saved as {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save script: {str(e)}")
    
    def _script_generation_finished(self):
        self.make_script_btn.config(state=tk.NORMAL, text="Make TikTok Script")
        self.progress.stop()
    
    def _facebook_post_generation_finished(self):
        self.make_facebook_btn.config(state=tk.NORMAL, text="Make Facebook Post")
        self.progress.stop()
    
    def _show_facebook_post(self, post, topic):
        # Create new window for Facebook post display
        post_window = tk.Toplevel(self.root)
        post_window.title(f"Facebook Post: {topic['title'][:50]}...")
        post_window.geometry("600x500")
        post_window.configure(bg='#2b2b2b')
        
        # Title
        title_label = tk.Label(post_window, text=topic['title'], 
                              font=('Arial', 14, 'bold'), 
                              fg='#ffffff', bg='#2b2b2b', wraplength=550)
        title_label.pack(pady=10)
        
        # Post content
        post_text = scrolledtext.ScrolledText(post_window, 
                                              font=('Arial', 11),
                                              bg='#3b3b3b', fg='#ffffff',
                                              wrap=tk.WORD)
        post_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        post_text.insert(tk.END, post)
        post_text.config(state=tk.DISABLED)
        
        # Save button
        save_btn = tk.Button(post_window, text="Save Post", 
                            command=lambda: self._save_facebook_post(post, topic),
                            bg='#4267B2', fg='white', font=('Arial', 12))
        save_btn.pack(pady=10)
    
    def _save_facebook_post(self, post, topic):
        filename = f"facebook_post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Topic: {topic['title']}\n")
                f.write(f"Source: {topic['source']}\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("-" * 50 + "\n\n")
                f.write(post)
            messagebox.showinfo("Saved", f"Facebook post saved as {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save post: {str(e)}")
    
    def open_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("500x400")
        settings_window.configure(bg='#2b2b2b')
        
        # Application settings
        tk.Label(settings_window, text="Application Settings", 
                font=('Arial', 14, 'bold'), fg='#ffffff', bg='#2b2b2b').pack(pady=10)
        
        # Auto-save scripts
        auto_save_var = tk.BooleanVar(value=self.settings_manager.get_setting('auto_save_scripts', True))
        auto_save_check = tk.Checkbutton(settings_window, text="Auto-save generated scripts", 
                                        variable=auto_save_var, font=('Arial', 12),
                                        fg='#ffffff', bg='#2b2b2b', selectcolor='#3b3b3b')
        auto_save_check.pack(anchor=tk.W, padx=20, pady=10)
        
        # Script save location
        tk.Label(settings_window, text="Script Save Location:", 
                font=('Arial', 12), fg='#ffffff', bg='#2b2b2b').pack(anchor=tk.W, padx=20)
        location_entry = tk.Entry(settings_window, font=('Arial', 12), width=40)
        location_entry.pack(padx=20, pady=(0, 10))
        location_entry.insert(0, self.settings_manager.get_setting('script_save_location', './scripts'))
        
        # Max topics per search
        tk.Label(settings_window, text="Max Topics Per Search:", 
                font=('Arial', 12), fg='#ffffff', bg='#2b2b2b').pack(anchor=tk.W, padx=20)
        max_topics_var = tk.StringVar(value=str(self.settings_manager.get_setting('max_topics_per_search', 100)))
        max_topics_entry = tk.Entry(settings_window, textvariable=max_topics_var, font=('Arial', 12), width=10)
        max_topics_entry.pack(anchor=tk.W, padx=20, pady=(0, 20))
        
        # ChatGPT info
        tk.Label(settings_window, text="ChatGPT Integration", 
                font=('Arial', 14, 'bold'), fg='#ffffff', bg='#2b2b2b').pack(pady=(20, 10))
        
        info_text = """ChatGPT will open in your browser when generating scripts.
No login credentials are required - you'll handle login manually.
The prompt will be copied to your clipboard automatically."""
        
        info_label = tk.Label(settings_window, text=info_text, 
                             font=('Arial', 10), fg='#cccccc', bg='#2b2b2b',
                             justify=tk.LEFT, wraplength=450)
        info_label.pack(padx=20, pady=10)
        
        # Save button
        def save_settings():
            self.settings_manager.set_setting('auto_save_scripts', auto_save_var.get())
            self.settings_manager.set_setting('script_save_location', location_entry.get())
            try:
                max_topics = int(max_topics_var.get())
                self.settings_manager.set_setting('max_topics_per_search', max_topics)
            except ValueError:
                messagebox.showerror("Error", "Max topics must be a number")
                return
            
            messagebox.showinfo("Saved", "Settings saved successfully!")
            settings_window.destroy()
        
        save_btn = tk.Button(settings_window, text="Save Settings", 
                            command=save_settings,
                            bg='#4CAF50', fg='white', font=('Arial', 12))
        save_btn.pack(pady=20)
    
    def load_settings(self):
        # Load any saved settings
        pass

def main():
    root = tk.Tk()
    app = ScriptWriterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
