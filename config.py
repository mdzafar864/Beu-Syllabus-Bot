import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "@EngineersPathwayOfficial"
ADMIN_ID = 5861904079  # Your Telegram ID

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL")

# File Paths
LOG_FILE = BASE_DIR / "bot.log"
ANALYTICS_FILE = BASE_DIR / "analytics.json"

# Flask Web Server
WEB_PORT = int(os.environ.get("PORT", 8080))

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
