#!/usr/bin/env python3
"""
ChromeDriver Downloader for ScriptWriter
This script helps download and setup ChromeDriver automatically
"""

import os
import sys
import requests
import zipfile
import platform
from pathlib import Path

def get_chrome_version():
    """Get the installed Chrome version"""
    try:
        if platform.system() == "Windows":
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon")
            version, _ = winreg.QueryValueEx(key, "version")
            return version
        else:
            # For other platforms, try to get version from command line
            import subprocess
            result = subprocess.run(['google-chrome', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip().split()[-1]
    except Exception as e:
        print(f"Could not detect Chrome version: {e}")
        return None

def download_chromedriver(version=None):
    """Download ChromeDriver for the specified Chrome version"""
    if not version:
        version = get_chrome_version()
        if not version:
            print("Could not detect Chrome version. Using latest stable version.")
            version = "latest"
    
    print(f"Downloading ChromeDriver for Chrome version: {version}")
    
    # ChromeDriver download URL
    if version == "latest":
        url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
        try:
            response = requests.get(url)
            version = response.text.strip()
        except Exception as e:
            print(f"Could not get latest version: {e}")
            version = "114.0.5735.90"  # Fallback version
    
    # Determine the major version for the download URL
    major_version = version.split('.')[0]
    
    # New ChromeDriver download URL format (for Chrome 115+)
    if int(major_version) >= 115:
        download_url = f"https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/{version}/win64/chromedriver-win64.zip"
    else:
        # Old format for older Chrome versions
        download_url = f"https://chromedriver.storage.googleapis.com/{version}/chromedriver_win32.zip"
    
    print(f"Downloading from: {download_url}")
    
    try:
        response = requests.get(download_url, stream=True)
        response.raise_for_status()
        
        # Save the zip file
        zip_path = "chromedriver.zip"
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print("Download completed. Extracting...")
        
        # Extract the zip file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(".")
        
        # Find the chromedriver.exe file
        for root, dirs, files in os.walk("."):
            for file in files:
                if file == "chromedriver.exe":
                    src_path = os.path.join(root, file)
                    dst_path = "chromedriver.exe"
                    
                    # Move to current directory
                    if src_path != dst_path:
                        if os.path.exists(dst_path):
                            os.remove(dst_path)
                        os.rename(src_path, dst_path)
                    
                    print(f"ChromeDriver extracted to: {os.path.abspath(dst_path)}")
                    break
        
        # Clean up
        os.remove(zip_path)
        
        # Remove any extracted directories
        for item in os.listdir("."):
            if os.path.isdir(item) and "chromedriver" in item.lower():
                import shutil
                shutil.rmtree(item)
        
        print("ChromeDriver setup completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error downloading ChromeDriver: {e}")
        return False

def main():
    """Main function"""
    print("ScriptWriter ChromeDriver Downloader")
    print("=" * 40)
    
    # Check if ChromeDriver already exists
    if os.path.exists("chromedriver.exe"):
        print("ChromeDriver already exists in current directory.")
        response = input("Do you want to download a new version? (y/n): ")
        if response.lower() != 'y':
            print("Keeping existing ChromeDriver.")
            return
    
    # Download ChromeDriver
    if download_chromedriver():
        print("\nChromeDriver is ready to use!")
        print("You can now run ScriptWriter with: python main.py")
    else:
        print("\nFailed to download ChromeDriver.")
        print("Please download manually from: https://chromedriver.chromium.org/")
        print("Place chromedriver.exe in the ScriptWriter folder.")

if __name__ == "__main__":
    main()
