import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install required Python packages"""
    print("Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing dependencies: {e}")
        return False

def check_chrome():
    """Check if Google Chrome is installed"""
    print("Checking for Google Chrome...")
    
    # Common Chrome installation paths on Windows
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            print("✓ Google Chrome found")
            return True
    
    print("✗ Google Chrome not found")
    print("Please install Google Chrome from: https://www.google.com/chrome/")
    return False

def download_chromedriver():
    """Download ChromeDriver if needed"""
    print("Checking for ChromeDriver...")
    
    if os.path.exists("chromedriver.exe"):
        print("✓ ChromeDriver found")
        return True
    
    print("ChromeDriver not found. Downloading...")
    try:
        subprocess.check_call([sys.executable, "download_chromedriver.py"])
        if os.path.exists("chromedriver.exe"):
            print("✓ ChromeDriver downloaded successfully")
            return True
        else:
            print("✗ ChromeDriver download failed")
            return False
    except subprocess.CalledProcessError as e:
        print(f"✗ Error downloading ChromeDriver: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("Creating directories...")
    
    directories = ["scripts", "logs"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ Created {directory}/ directory")

def check_python_version():
    """Check if Python version is compatible"""
    print("Checking Python version...")
    
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} is not compatible")
        print("Please install Python 3.8 or higher from: https://www.python.org/downloads/")
        return False

def main():
    """Main setup function"""
    print("ScriptWriter Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        input("Press Enter to exit...")
        return
    
    # Check Chrome
    chrome_ok = check_chrome()
    
    # Install requirements
    if not install_requirements():
        input("Press Enter to exit...")
        return
    
    # Download ChromeDriver if Chrome is available
    chromedriver_ok = True
    if chrome_ok:
        chromedriver_ok = download_chromedriver()
    
    # Create directories
    create_directories()
    
    print("\n" + "=" * 50)
    print("Setup Complete!")
    print("=" * 50)
    
    if chrome_ok and chromedriver_ok:
        print("✓ All requirements met")
        print("\nTo run ScriptWriter:")
        print("  python main.py")
    elif chrome_ok and not chromedriver_ok:
        print("⚠ ChromeDriver download failed")
        print("ScriptWriter will use manual mode (clipboard)")
        print("\nTo run ScriptWriter:")
        print("  python main.py")
    else:
        print("⚠ Chrome installation required")
        print("Please install Google Chrome and run setup again")
    
    print("\nFor help, see README.md")
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
