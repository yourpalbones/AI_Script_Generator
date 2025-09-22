# ScriptWriter Installation Guide

## Quick Start (Recommended)

1. **Download ScriptWriter** to your computer
2. **Double-click `install.bat`** to automatically install everything
3. **Double-click `run.bat`** to start the application

## Manual Installation

### Step 1: Install Python

1. Go to [python.org](https://www.python.org/downloads/)
2. Download Python 3.8 or higher
3. **IMPORTANT**: During installation, check "Add Python to PATH"
4. Verify installation by opening Command Prompt and typing: `python --version`

### Step 2: Install Google Chrome

1. Go to [google.com/chrome](https://www.google.com/chrome/)
2. Download and install Chrome
3. This is required for ChatGPT automation

### Step 3: Create ChatGPT Account (if needed)

1. Go to [chat.openai.com](https://chat.openai.com)
2. Sign up for a free account
3. Verify your email address
4. This is required for script generation

### Step 4: Install Dependencies

1. Open Command Prompt in the ScriptWriter folder
2. Run: `pip install -r requirements.txt`

### Step 5: Test Installation

1. Run: `python test_app.py`
2. All tests should pass
3. If tests fail, see troubleshooting below

### Step 6: Run Application

1. Run: `python main.py`
2. Or double-click `run.bat`

## First Time Setup

### 1. Test ChatGPT Access

1. Open your web browser
2. Go to [chat.openai.com](https://chat.openai.com)
3. Log in to your ChatGPT account
4. Make sure you can access the chat interface

### 2. Test Topic Generation

1. Select a category from the dropdown
2. Click "Generate Topics"
3. Wait for topics to load
4. You should see up to 100 topics with timestamps

### 3. Generate Your First Script

1. Click on a topic to select it
2. Click "Make Script"
3. ChatGPT will open in your browser
4. The TikTok script prompt will be automatically posted
5. Copy the generated TikTok script
6. Click "OK" in the application
7. Review and save the script

## Troubleshooting

### "Python not found" Error

**Solution**: Python is not in your PATH
1. Reinstall Python and check "Add Python to PATH"
2. Or manually add Python to PATH:
   - Search "Environment Variables" in Windows
   - Edit PATH variable
   - Add Python installation directory

### "ChromeDriver not found" Error

**Solution**: ChromeDriver is missing
1. The app tries to download it automatically
2. If it fails, download manually:
   - Go to [chromedriver.chromium.org](https://chromedriver.chromium.org/)
   - Download version matching your Chrome
   - Place `chromedriver.exe` in ScriptWriter folder

### "ChatGPT not opening" Error

**Solution**: Browser issues
1. Check your default browser settings
2. Try manually opening chat.openai.com
3. Make sure you're logged into ChatGPT
4. Check if pop-ups are blocked

### "No module named 'selenium'" Error

**Solution**: Dependencies not installed
1. Open Command Prompt in ScriptWriter folder
2. Run: `pip install -r requirements.txt`
3. If that fails, try: `python -m pip install --upgrade pip`

### "Script generation failed" Error

**Solutions**:
1. Make sure you're logged into ChatGPT in your browser
2. Check if ChatGPT is accessible
3. Ensure you copied the generated script before clicking OK
4. Try again after a few minutes

### "No topics generated" Error

**Solutions**:
1. Check your internet connection
2. Some news sources may be temporarily down
3. Try a different category
4. Wait a few minutes and try again

### Application Crashes or Freezes

**Solutions**:
1. Close and restart the application
2. Check your internet connection
3. Restart your computer
4. Run `python test_app.py` to check for issues

### Slow Performance

**Solutions**:
1. Close other applications
2. Check your internet connection
3. Some sources may be slow to respond
4. Try generating fewer topics at once

## Advanced Configuration

### Custom Script Length

Edit `config.py` and change:
```python
SCRIPT_TARGET_DURATION = 75  # seconds (1:15)
```

### Custom News Sources

Edit `config.py` and modify the `NEWS_SOURCES` dictionary to add your own sources.

### Custom Script Length

To change the target TikTok script duration, edit `config.py` and modify:
```python
SCRIPT_TARGET_DURATION = 75  # seconds (1:15) - TikTok minimum
```

## File Structure

After installation, your ScriptWriter folder should contain:

```
ScriptWriter/
├── main.py                 # Main application
├── scrapers.py            # News scraping
├── chatgpt_automation.py  # ChatGPT integration
├── settings_manager.py    # Settings management
├── config.py              # Configuration
├── test_app.py           # Test script
├── requirements.txt      # Dependencies
├── install.bat          # Windows installer
├── run.bat              # Windows launcher
├── setup.py             # Python setup
├── README.md            # Documentation
├── INSTALLATION_GUIDE.md # This file
├── settings.enc         # Your encrypted settings (created automatically)
├── key.key              # Encryption key (created automatically)
├── scripts/             # Generated scripts (created automatically)
└── logs/                # Log files (created automatically)
```

## Security Notes

- No ChatGPT credentials are stored or required
- The app doesn't send your data anywhere
- All scripts are saved locally on your computer
- ChatGPT interaction happens in your own browser

## Getting Help

If you're still having issues:

1. **Run the test script**: `python test_app.py`
2. **Check the logs**: Look in the `logs/` folder for error messages
3. **Verify requirements**: Make sure all dependencies are installed
4. **Check internet**: Ensure you have a stable internet connection
5. **Try different categories**: Some sources may be temporarily unavailable

## System Requirements

- **Operating System**: Windows 10 or higher
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 500MB free space
- **Internet**: Stable broadband connection
- **Browser**: Google Chrome (required for automation)

## Uninstallation

To remove ScriptWriter:

1. Delete the ScriptWriter folder
2. Your scripts and settings will be deleted
3. No system files are modified during installation

## Updates

To update ScriptWriter:

1. Download the new version
2. Replace the old files
3. Run `pip install -r requirements.txt` to update dependencies
4. Your settings will be preserved
