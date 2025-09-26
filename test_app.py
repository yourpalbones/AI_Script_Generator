#!/usr/bin/env python3
"""
Test script for ScriptWriter application
Run this to verify all components are working correctly
"""

import sys
import os
from datetime import datetime

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import tkinter as tk
        print("✓ tkinter imported successfully")
    except ImportError as e:
        print(f"✗ tkinter import failed: {e}")
        return False
    
    try:
        import requests
        print("✓ requests imported successfully")
    except ImportError as e:
        print(f"✗ requests import failed: {e}")
        return False
    
    try:
        from bs4 import BeautifulSoup
        print("✓ BeautifulSoup imported successfully")
    except ImportError as e:
        print(f"✗ BeautifulSoup import failed: {e}")
        return False
    
    try:
        from selenium import webdriver
        print("✓ selenium imported successfully")
    except ImportError as e:
        print(f"✗ selenium import failed: {e}")
        return False
    
    try:
        from cryptography.fernet import Fernet
        print("✓ cryptography imported successfully")
    except ImportError as e:
        print(f"✗ cryptography import failed: {e}")
        return False
    
    return True

def test_local_modules():
    """Test if local modules can be imported"""
    print("\nTesting local modules...")
    
    try:
        from scrapers import NewsScraper
        print("✓ NewsScraper imported successfully")
    except ImportError as e:
        print(f"✗ NewsScraper import failed: {e}")
        return False
    
    try:
        from chatgpt_automation import ChatGPTAutomation
        print("✓ ChatGPTAutomation imported successfully")
    except ImportError as e:
        print(f"✗ ChatGPTAutomation import failed: {e}")
        return False
    
    try:
        from settings_manager import SettingsManager
        print("✓ SettingsManager imported successfully")
    except ImportError as e:
        print(f"✗ SettingsManager import failed: {e}")
        return False
    
    try:
        import config
        print("✓ config imported successfully")
    except ImportError as e:
        print(f"✗ config import failed: {e}")
        return False
    
    return True

def test_news_scraper():
    """Test NewsScraper functionality"""
    print("\nTesting NewsScraper...")
    
    try:
        from scrapers import NewsScraper
        scraper = NewsScraper()
        
        # Test a simple scraping operation
        print("Testing Reddit scraping...")
        topics = scraper._scrape_reddit_subreddit('funny')
        
        if topics:
            print(f"✓ Successfully scraped {len(topics)} topics from Reddit")
            print(f"  Sample topic: {topics[0]['title'][:50]}...")
        else:
            print("⚠ No topics scraped (this might be normal if Reddit is down)")
        
        return True
        
    except Exception as e:
        print(f"✗ NewsScraper test failed: {e}")
        return False

def test_settings_manager():
    """Test SettingsManager functionality"""
    print("\nTesting SettingsManager...")
    
    try:
        from settings_manager import SettingsManager
        settings = SettingsManager()
        
        # Test setting and getting a value
        test_key = "test_setting"
        test_value = "test_value"
        
        settings.set_setting(test_key, test_value)
        retrieved_value = settings.get_setting(test_key)
        
        if retrieved_value == test_value:
            print("✓ SettingsManager working correctly")
            # Clean up test setting
            settings.settings.pop(test_key, None)
            return True
        else:
            print("✗ SettingsManager value mismatch")
            return False
            
    except Exception as e:
        print(f"✗ SettingsManager test failed: {e}")
        return False

def test_chrome_driver():
    """Test if Chrome driver can be initialized"""
    print("\nTesting Chrome driver...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run headless for testing
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://www.google.com")
        
        if "Google" in driver.title:
            print("✓ Chrome driver working correctly")
            driver.quit()
            return True
        else:
            print("✗ Chrome driver failed to load page")
            driver.quit()
            return False
            
    except Exception as e:
        print(f"✗ Chrome driver test failed: {e}")
        print("  Make sure Chrome and ChromeDriver are installed")
        return False

def test_directories():
    """Test if required directories exist or can be created"""
    print("\nTesting directories...")
    
    directories = ['scripts', 'logs']
    
    for directory in directories:
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
                print(f"✓ Created {directory}/ directory")
            except Exception as e:
                print(f"✗ Failed to create {directory}/ directory: {e}")
                return False
        else:
            print(f"✓ {directory}/ directory exists")
    
    return True

def main():
    """Run all tests"""
    print("ScriptWriter Application Test")
    print("=" * 50)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Import Tests", test_imports),
        ("Local Module Tests", test_local_modules),
        ("Directory Tests", test_directories),
        ("Settings Manager Tests", test_settings_manager),
        ("News Scraper Tests", test_news_scraper),
        ("Chrome Driver Tests", test_chrome_driver)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}")
        print("-" * len(test_name))
        
        try:
            if test_func():
                passed += 1
                print(f"✓ {test_name} PASSED")
            else:
                print(f"✗ {test_name} FAILED")
        except Exception as e:
            print(f"✗ {test_name} FAILED with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! ScriptWriter is ready to use.")
        print("\nTo run the application:")
        print("  python main.py")
    else:
        print("⚠ Some tests failed. Please check the errors above.")
        print("\nCommon solutions:")
        print("  1. Install missing dependencies: pip install -r requirements.txt")
        print("  2. Install Google Chrome")
        print("  3. Install ChromeDriver")
        print("  4. Check your internet connection")
    
    print(f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
