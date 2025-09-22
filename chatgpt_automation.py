from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import random
import webbrowser
import pyperclip

class ChatGPTAutomation:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.is_logged_in = False
    
    def setup_driver(self):
        """Setup Chrome driver with appropriate options"""
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        # Open in new tab instead of new window
        chrome_options.add_experimental_option("detach", True)
        
        # Keep browser visible so user can see what's happening
        # chrome_options.add_argument("--headless")  # Commented out for user visibility
        
        # Try multiple approaches to setup ChromeDriver
        approaches = [
            self._try_webdriver_manager,
            self._try_system_chromedriver,
            self._try_chromedriver_in_path,
            self._try_chromedriver_in_folder
        ]
        
        for approach in approaches:
            try:
                if approach(chrome_options):
                    self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                    self.wait = WebDriverWait(self.driver, 20)
                    return True
            except Exception as e:
                print(f"Approach failed: {e}")
                continue
        
        print("All ChromeDriver setup approaches failed")
        return False
    
    def _try_webdriver_manager(self, chrome_options):
        """Try using webdriver-manager"""
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            # Fix the WebDriver Manager initialization issue
            driver_path = ChromeDriverManager().install()
            self.driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
            return True
        except Exception as e:
            print(f"WebDriver Manager failed: {e}")
            return False
    
    def _try_system_chromedriver(self, chrome_options):
        """Try using system ChromeDriver"""
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            return True
        except Exception as e:
            print(f"System ChromeDriver failed: {e}")
            return False
    
    def _try_chromedriver_in_path(self, chrome_options):
        """Try using ChromeDriver in system PATH"""
        try:
            import os
            # Add current directory to PATH temporarily
            current_dir = os.getcwd()
            if current_dir not in os.environ['PATH']:
                os.environ['PATH'] = current_dir + os.pathsep + os.environ['PATH']
            
            self.driver = webdriver.Chrome(options=chrome_options)
            return True
        except Exception as e:
            print(f"ChromeDriver in PATH failed: {e}")
            return False
    
    def _try_chromedriver_in_folder(self, chrome_options):
        """Try using ChromeDriver in the application folder"""
        try:
            import os
            chromedriver_path = os.path.join(os.getcwd(), "chromedriver.exe")
            if os.path.exists(chromedriver_path):
                self.driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
                return True
            return False
        except Exception as e:
            print(f"ChromeDriver in folder failed: {e}")
            return False
    
    def login(self, email, password):
        """Login to ChatGPT using email and password"""
        if not self.driver:
            if not self.setup_driver():
                return False
        
        try:
            # Navigate to ChatGPT login page
            self.driver.get("https://chat.openai.com/auth/login")
            time.sleep(3)
            
            # Click login button
            login_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Log in')]"))
            )
            login_button.click()
            time.sleep(2)
            
            # Enter email
            email_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            email_input.clear()
            email_input.send_keys(email)
            time.sleep(1)
            
            # Click continue
            continue_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue')]"))
            )
            continue_button.click()
            time.sleep(2)
            
            # Enter password
            password_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "password"))
            )
            password_input.clear()
            password_input.send_keys(password)
            time.sleep(1)
            
            # Click continue
            continue_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue')]"))
            )
            continue_button.click()
            time.sleep(3)
            
            # Wait for successful login (look for chat interface)
            try:
                self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[placeholder*='Message']"))
                )
                self.is_logged_in = True
                return True
            except TimeoutException:
                # Check if there's a verification step
                if "verify" in self.driver.current_url.lower():
                    print("Verification required. Please complete verification manually.")
                    # Wait for user to complete verification
                    time.sleep(30)
                    try:
                        self.wait.until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[placeholder*='Message']"))
                        )
                        self.is_logged_in = True
                        return True
                    except TimeoutException:
                        return False
                return False
                
        except Exception as e:
            print(f"Error during login: {e}")
            return False
    
    def generate_script(self, topic, settings_manager):
        """Generate a comedy commentary script for the given topic"""
        try:
            # Create the prompt
            prompt = self._create_script_prompt(topic)
            
            # Use manual clipboard approach (simple and reliable)
            return self._generate_script_manual(topic, prompt)
            
        except Exception as e:
            raise Exception(f"Error generating script: {e}")
    
    def _generate_script_automated(self, topic, prompt):
        """Try to generate script using automated Chrome approach"""
        # Setup Chrome driver if not already done
        if not self.driver:
            if not self.setup_driver():
                raise Exception("Failed to setup Chrome driver")
        
        # Simply navigate to ChatGPT (don't try to manage tabs)
        self.driver.get("https://chat.openai.com")
        time.sleep(5)  # Give more time for page to load
        
        # Wait for the page to load and find the message input
        print("Looking for ChatGPT input field...")
        print(f"Current URL: {self.driver.current_url}")
        print(f"Page title: {self.driver.title}")
        
        # Try to find the input field with a simple approach
        message_input = None
        try:
            # Wait for the page to be ready
            self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            
            # Try the most common selectors first
            selectors = [
                "textarea[placeholder*='Message']",
                "textarea[data-id='root']",
                "#prompt-textarea",
                "textarea",
                "[contenteditable='true']"
            ]
            
            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            message_input = element
                            print(f"Found input field with selector: {selector}")
                            break
                    if message_input:
                        break
                except:
                    continue
            
            if not message_input:
                raise Exception("Could not find ChatGPT message input")
                
        except Exception as e:
            print(f"Error finding input field: {e}")
            raise Exception("Could not find ChatGPT message input. Please ensure you're logged in and try again.")
        
        # Scroll to the input field
        self.driver.execute_script("arguments[0].scrollIntoView(true);", message_input)
        time.sleep(1)
        
        # Click on the input field first
        message_input.click()
        time.sleep(1)
        
        # Clear and type the prompt
        message_input.clear()
        time.sleep(1)
        
        # Type the prompt
        message_input.send_keys(prompt)
        time.sleep(2)
        
        # Send the message
        message_input.send_keys(Keys.RETURN)
        time.sleep(3)
        
        print("Prompt sent to ChatGPT!")
        
        # Show instructions to user
        instructions = f"""
TikTok Script Generation

The prompt has been automatically posted to ChatGPT!

Instructions:
1. ChatGPT should now be generating your TikTok script
2. Wait for the response to complete
3. Copy the generated script from ChatGPT
4. Click 'OK' when you have the script ready

Topic: {topic['title'][:50]}...

The script will be optimized for TikTok with YourPalBones/Jon Stewart/John Oliver style.
"""
        
        # Show message box with instructions
        import tkinter as tk
        from tkinter import messagebox
        
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        result = messagebox.askokcancel("Script Generation", instructions)
        
        if result:
            # Get the script from clipboard
            script = pyperclip.paste()
            
            # Validate that we got a script (more lenient validation)
            if len(script) < 30 or script.strip() == "":
                raise Exception("Please copy the generated script from ChatGPT and try again")
            
            # Check if it's still the prompt (not the generated script)
            if "Write a TikTok script about:" in script and len(script) < 200:
                raise Exception("Please copy the generated script from ChatGPT and try again. Make sure you copied the script response, not the prompt.")
            
            return script
        else:
            raise Exception("Script generation cancelled by user")
    
    def _generate_script_manual(self, topic, prompt):
        """Fallback method using manual clipboard approach"""
        # Copy prompt to clipboard
        pyperclip.copy(prompt)
        
        # Open ChatGPT in browser
        webbrowser.open("https://chat.openai.com")
        
        # Show instructions to user
        instructions = f"""
TikTok Script Generation

The TikTok script prompt has been copied to your clipboard.

Instructions:
1. ChatGPT should now be open in your browser
2. If you're not logged in, please log in to ChatGPT
3. Paste the prompt (Ctrl+V) into the chat
4. Press Enter to submit
5. Wait for ChatGPT to generate the TikTok script
6. Copy the generated script (select all and Ctrl+C)
7. Click 'OK' when you have the script ready

Topic: {topic['title'][:50]}...

The script will be optimized for TikTok with YourPalBones/Jon Stewart/John Oliver style.

IMPORTANT: Make sure to copy the ENTIRE generated script before clicking OK!
"""
        
        # Show message box with instructions
        import tkinter as tk
        from tkinter import messagebox
        
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        result = messagebox.askokcancel("Script Generation (Manual Mode)", instructions)
        
        if result:
            # Get the script from clipboard
            script = pyperclip.paste()
            
            # Validate that we got a script (more lenient validation)
            if len(script) < 30 or script.strip() == "":
                raise Exception("Please copy the generated script from ChatGPT and try again")
            
            # Check if it's still the prompt (not the generated script)
            if "Write a TikTok script about:" in script and len(script) < 200:
                raise Exception("Please copy the generated script from ChatGPT and try again. Make sure you copied the script response, not the prompt.")
            
            return script
        else:
            raise Exception("Script generation cancelled by user")
    
    def _create_script_prompt(self, topic):
        """Create the TikTok comedy commentary script prompt"""
        # Clean up the topic title and summary
        title = topic['title'].strip()
        source = topic['source'].strip()
        summary = topic.get('summary', 'No summary available').strip()
        time_ago = topic.get('time_ago', 'Recently')
        
        # Truncate summary if too long
        if len(summary) > 300:
            summary = summary[:300] + "..."
        
        prompt = f"""Write a TikTok script about: {title}

Source: {source}
Summary: {summary}
Posted: {time_ago}

REQUIREMENTS:
- AT LEAST 1 minute 15 seconds when read at normal pace
- Style: Blend of YourPalBones, Jon Stewart, and John Oliver
- Must be informative, funny, and factually correct
- Perfect for TikTok comedy commentary

STYLE ELEMENTS:
- YourPalBones: Sarcastic, witty observations with sharp political commentary
- Jon Stewart: Conversational, relatable tone with perfect comedic timing
- John Oliver: Informative yet entertaining, builds to strong punchlines
- Include strategic [PAUSE] markers for comedic effect
- Use current events and cultural references
- Make it engaging and funny throughout

SCRIPT STRUCTURE:
1. Strong opening hook (10-15 seconds) - grab attention immediately
2. Main commentary with 3-4 well-timed jokes (45-50 seconds)
3. Strong closing punchline (10-15 seconds) - tie everything together
4. Strategic [PAUSE] markers throughout for comedic timing

CONTENT REQUIREMENTS:
- Be informative and factually accurate
- Include relevant context and background
- Use conversational language and relatable analogies
- Focus on the absurdity, hypocrisy, or comedic elements
- Make it shareable and engaging for TikTok audience
- Ensure it's at least 1:15 when read at normal speaking pace

Format as a clear, professional script ready for TikTok recording."""
        
        return prompt
    
    def _extract_response(self):
        """Extract the generated script from ChatGPT response"""
        try:
            # Wait for the response to appear
            time.sleep(10)
            
            # Look for the latest response
            response_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-message-author-role='assistant']")
            
            if response_elements:
                # Get the last (most recent) response
                latest_response = response_elements[-1]
                
                # Extract text content
                script = latest_response.text
                
                # Clean up the script
                script = self._clean_script(script)
                
                return script
            else:
                raise Exception("No response found from ChatGPT")
                
        except Exception as e:
            raise Exception(f"Error extracting response: {e}")
    
    def _clean_script(self, script):
        """Clean and format the generated script"""
        # Remove any ChatGPT-specific formatting
        lines = script.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('ChatGPT') and not line.startswith('Assistant'):
                cleaned_lines.append(line)
        
        # Join lines and ensure proper formatting
        script = '\n'.join(cleaned_lines)
        
        # Ensure it starts with a proper opening
        if not script.startswith(('Welcome', 'Well', 'Oh', 'So', 'Alright', 'Hey')):
            script = "Well, well, well... " + script
        
        return script
    
    def close(self):
        """Close the browser driver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            self.is_logged_in = False
    
    def __del__(self):
        """Cleanup when object is destroyed"""
        self.close()
