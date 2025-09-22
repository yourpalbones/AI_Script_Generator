# Configuration settings for ScriptWriter

# Application settings
APP_NAME = "ScriptWriter"
APP_VERSION = "1.0.0"
APP_AUTHOR = "ScriptWriter Team"

# UI Settings
DEFAULT_WINDOW_SIZE = "1200x800"
DARK_THEME = True

# Scraping settings
MAX_TOPICS_PER_SEARCH = 100
SEARCH_TIMEOUT = 30  # seconds
REQUEST_DELAY = 1  # seconds between requests
MAX_RETRIES = 3

# Time-based search windows (in hours)
TIME_WINDOWS = [2, 6, 12, 24]

# Reddit API settings
REDDIT_LIMIT = 25  # posts per subreddit
REDDIT_SORT = "hot"  # hot, new, top

# ChatGPT settings
CHATGPT_TIMEOUT = 60  # seconds
CHATGPT_RETRY_ATTEMPTS = 3
SCRIPT_TARGET_DURATION = 75  # seconds (1:15) - TikTok minimum
SCRIPT_PLATFORM = "TikTok"  # Target platform
SCRIPT_STYLE = "YourPalBones, Jon Stewart, John Oliver blend"

# File paths
SCRIPTS_DIR = "./scripts"
LOGS_DIR = "./logs"
SETTINGS_FILE = "settings.enc"
KEY_FILE = "key.key"

# Content filtering keywords
FUNNY_KEYWORDS = [
    'funny', 'hilarious', 'weird', 'strange', 'bizarre', 'odd',
    'unusual', 'crazy', 'silly', 'absurd', 'ridiculous', 'wacky',
    'quirky', 'eccentric', 'comical', 'laugh', 'joke', 'prank'
]

CRIME_KEYWORDS = [
    'arrested', 'arrest', 'crime', 'criminal', 'theft', 'robbery',
    'burglary', 'fraud', 'scam', 'police', 'officer', 'jail',
    'prison', 'court', 'trial', 'guilty', 'sentence', 'fine'
]

# News sources by category
NEWS_SOURCES = {
    'political': [
        'https://www.cnn.com/politics',
        'https://www.foxnews.com/politics',
        'https://www.nbcnews.com/politics'
    ],
    'ohio_political': [
        'https://www.cleveland.com/politics',
        'https://www.dispatch.com/politics'
    ],
    'local_ohio': [
        'https://www.wfmj.com',
        'https://www.vindy.com',
        'https://www.tribtoday.com'
    ],
    'weird_news': [
        'https://www.weirdnews.com',
        'https://www.odditycentral.com',
        'https://www.unexplained-mysteries.com'
    ],
    'crime_news': [
        'https://www.crimeonline.com',
        'https://www.crimestoppers.com'
    ]
}

# Reddit subreddits by category
REDDIT_SUBREDDITS = {
    'political': ['politics', 'Conservative'],
    'ohio': ['Ohio', 'YoungstownOhio'],
    'funny': ['funny', 'nottheonion', 'FloridaMan']
}

# Local government sites
LOCAL_GOVERNMENT_SITES = [
    'https://www.cityofyoungstownoh.com',
    'https://www.salemohio.org',
    'https://www.warren.org'
]

# User agent strings for web scraping
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'
]

# Chrome driver options
CHROME_OPTIONS = [
    '--no-sandbox',
    '--disable-dev-shm-usage',
    '--disable-blink-features=AutomationControlled',
    '--disable-extensions',
    '--disable-plugins',
    '--disable-images',  # Faster loading
    '--disable-javascript'  # For some sites
]

# Error messages
ERROR_MESSAGES = {
    'chrome_not_found': 'Google Chrome not found. Please install Chrome and try again.',
    'login_failed': 'Failed to login to ChatGPT. Please check your credentials.',
    'no_topics': 'No topics found. Please try a different category or check your internet connection.',
    'script_failed': 'Failed to generate script. Please try again.',
    'network_error': 'Network error. Please check your internet connection.',
    'timeout_error': 'Request timed out. Please try again.'
}

# Success messages
SUCCESS_MESSAGES = {
    'topics_generated': 'Topics generated successfully!',
    'script_generated': 'Script generated successfully!',
    'settings_saved': 'Settings saved successfully!',
    'script_saved': 'Script saved successfully!'
}
