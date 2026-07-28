import os
from pathlib import Path

# Base Directory
BASE_DIR = Path(__file__).parent

# Bot Configuration
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "@EngineersPathwayOfficial"
ADMIN_ID = 5861904079  # Your Telegram ID

# File Paths
LOG_FILE = BASE_DIR / 'bot.log'
ANALYTICS_FILE = BASE_DIR / 'analytics.json'

# Flask Web Server
WEB_PORT = int(os.environ.get('PORT', 8080))

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")