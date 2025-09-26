# ScriptWriter - Comedy Commentary Generator

A Windows desktop application for finding and generating comedy/commentary scripts from news topics using ChatGPT automation.

## Features

- **8 Topic Categories**: US Political, Ohio Political, Local Ohio News, Funny Stories, and Criminal Stories
- **100 Topics Per Search**: Generates up to 100 relevant topics per category
- **Time-Based Filtering**: Shows post time with "time ago" and actual timestamps
- **ChatGPT Integration**: Automated script generation with comedy commentary style
- **TikTok Script Length**: Optimized for AT LEAST 1 minute 15 seconds of content
- **Local Storage**: Encrypted settings and script history
- **Smart Filtering**: Category-specific content filtering and prioritization

## Installation

### Prerequisites

1. **Python 3.8 or higher** - Download from [python.org](https://www.python.org/downloads/)
2. **ChatGPT Account** - For script generation (free account works)
3. **Internet Connection** - For news scraping and ChatGPT access

### Setup Instructions

1. **Clone or Download** the ScriptWriter files to your computer

2. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **No additional setup required** - The application uses your browser directly

4. **Run the Application**:
   ```bash
   python main.py
   ```

## Usage

### First Time Setup

1. **Launch the Application**: Run `python main.py`

2. **Login to ChatGPT**: Make sure you're logged into ChatGPT in your browser

3. **Select a Category**: Choose from the dropdown menu:
   - US Political News
   - Ohio Political News
   - Local Ohio News (Columbiana, Trumbull, Mahoning Counties)
   - Funny Stories (US National)
   - Local Funny Stories (Columbiana, Trumbull, Mahoning Counties)
   - Funny Criminal Stories (US National)
   - Funny Criminal Stories (Ohio Statewide)
   - Funny Criminal Stories (Columbiana, Mahoning, Trumbull Counties)

### Generating Topics

1. **Click "Generate Topics"** to search for current news topics
2. **Wait for Results** - The application will scrape various sources
3. **Browse Topics** - View up to 100 topics with timestamps and sources
4. **Search/Filter** - Use the search box to find specific topics

### Creating Scripts

1. **Select a Topic** from the list (click to highlight)
2. **Click "Make Script"** or double-click the topic
3. **ChatGPT Opens** - Your browser will open ChatGPT automatically
4. **Paste Prompt** - The TikTok script prompt is copied to your clipboard (Ctrl+V)
5. **Press Enter** - Submit the prompt to ChatGPT
6. **Generate Script** - Wait for ChatGPT to create the TikTok comedy commentary script
7. **Copy Script** - Copy the generated script from ChatGPT
8. **Click OK** - Return to the application to view and save the script

## Topic Categories & Sources

### Political News
- **Reddit**: r/politics, r/Conservative, r/Ohio, r/YoungstownOhio
- **News Sites**: CNN Politics, Fox News Politics, NBC Politics
- **Government**: Ohio.gov news releases

### Local Ohio News
- **Local Sites**: WFMJ.com, Vindy.com, Tribune Chronicle
- **Government**: City websites (Youngstown, Salem, Warren)
- **Social Media**: Local government Facebook pages

### Funny Stories
- **Reddit**: r/funny, r/nottheonion, r/FloridaMan
- **Weird News**: WeirdNews.com, OddityCentral.com
- **Local Sources**: Police department social media

### Criminal Stories
- **Reddit**: r/FloridaMan, r/nottheonion
- **Crime Sites**: CrimeOnline.com, CrimeStoppers.com
- **Local Police**: Department social media posts

## TikTok Script Style

Scripts are generated specifically for TikTok in the style of:
- **YourPalBones**: Sarcastic, witty observations with sharp political commentary
- **Jon Stewart**: Conversational, relatable tone with perfect comedic timing
- **John Oliver**: Informative yet entertaining, builds to strong punchlines

TikTok Features:
- AT LEAST 1 minute 15 seconds duration (TikTok minimum)
- [PAUSE] markers for comedic timing
- Strong opening hook to grab attention immediately
- Main commentary with 3-4 well-timed jokes
- Strong closing punchline
- Informative, funny, and factually correct
- Optimized for TikTok's algorithm and audience

## Settings

Access settings by clicking the "Settings" button:

- **Auto-save Scripts**: Automatically save generated scripts
- **Script Location**: Where to save generated scripts
- **Max Topics Per Search**: Number of topics to generate (1-1000)
- **ChatGPT Integration**: Information about the browser-based approach

## Troubleshooting

### Common Issues

1. **No Topics Generated**:
   - Check your internet connection
   - Some sources may be temporarily unavailable
   - Try a different category

2. **Script Generation Failed**:
   - Make sure you're logged into ChatGPT in your browser
   - Check if ChatGPT is accessible
   - Ensure you copied the generated script before clicking OK
   - Try again after a few minutes

3. **ChatGPT Not Opening**:
   - Check your default browser settings
   - Try manually opening chat.openai.com
   - Ensure you have a ChatGPT account

### Error Messages

- **"Please copy the generated script"**: Make sure you copied the script from ChatGPT before clicking OK
- **"Script generation cancelled"**: You cancelled the process, try again
- **"No topics found"**: Check your internet connection or try a different category

## File Structure

```
ScriptWriter/
├── main.py                 # Main application
├── scrapers.py            # News scraping logic
├── chatgpt_automation.py  # ChatGPT integration
├── settings_manager.py    # Settings and encryption
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── settings.enc          # Encrypted settings (created automatically)
├── key.key               # Encryption key (created automatically)
└── scripts/              # Generated scripts folder (created automatically)
```

## Security

- **No Credentials Stored**: No ChatGPT credentials are stored or required
- **No Data Collection**: The app doesn't send your data anywhere
- **Local Storage**: All scripts and settings are stored locally
- **Browser-Based**: ChatGPT interaction happens in your own browser

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Ensure all dependencies are installed correctly
3. Verify your ChatGPT account is working in a browser
4. Make sure you have a stable internet connection

## Legal Notice

This application is for educational and personal use. Please respect the terms of service of all websites being scraped and ChatGPT's usage policies. The application is designed to be respectful of rate limits and website resources.
