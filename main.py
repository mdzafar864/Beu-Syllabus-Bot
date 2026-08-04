import logging
import threading
import time
from datetime import datetime, timedelta
import requests

import telebot
from flask import Flask, request, jsonify

from config import TOKEN, LOG_FILE, BASE_DIR, WEB_PORT
from models.user_session import UserSession
from models.analytics import Analytics
from handlers import (
    register_base_handlers,
    register_syllabus_handlers,
    register_admin_handlers,
    register_callback_handlers
)
from data.syllabus import SYLLABUS

# ================== LOGGING SETUP ==================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ================== BOT INITIALIZATION ==================
bot = telebot.TeleBot(TOKEN)
user_session = UserSession()
analytics = Analytics()

# ================== REGISTER HANDLERS ==================
register_base_handlers(bot, analytics, user_session)
register_syllabus_handlers(bot, analytics, user_session)
register_admin_handlers(bot, analytics)
register_callback_handlers(bot, analytics)

# ================== FLASK APP FOR RENDER ==================
flask_app = Flask(__name__)

@flask_app.route('/')
def health():
    return "✅ BEU Syllabus Bot is running!", 200

@flask_app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "users": len(analytics.total_users),
        "downloads": analytics.get_total_downloads()
    }), 200

@flask_app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming Telegram updates via webhook"""
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'OK', 200
    return 'Bad Request', 400

# ================== SET WEBHOOK ==================
def set_webhook():
    """Set webhook for Render deployment"""
    try:
        # Remove any existing webhook first
        bot.remove_webhook()
        time.sleep(1)
        
        # Get Render URL from environment
        render_url = "https://beu-syllabus-bot.onrender.com"  # Your Render URL
        
        # Set webhook
        webhook_url = f"{render_url}/webhook"
        bot.set_webhook(url=webhook_url)
        
        logger.info(f"✅ Webhook set successfully: {webhook_url}")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to set webhook: {e}")
        return False

# ================== DAILY RESET SCHEDULER ==================
def daily_reset():
    while True:
        try:
            now = datetime.now()
            next_reset = datetime(now.year, now.month, now.day) + timedelta(days=1)
            sleep_seconds = (next_reset - now).total_seconds()
            if sleep_seconds > 0:
                time.sleep(sleep_seconds)
                analytics.reset_daily()
                logger.info("✅ Daily analytics reset completed")
        except Exception as e:
            logger.error(f"Error in daily_reset: {e}")
            time.sleep(3600)

# ================== RUN BOT WITH WEBHOOK ==================
def run_bot_with_webhook():
    """Run bot using webhook (for Render)"""
    try:
        # Set webhook
        if not set_webhook():
            logger.error("❌ Failed to set webhook. Exiting.")
            return
        
        logger.info(f"🚀 Bot is running in webhook mode on Render!")
        logger.info(f"📡 Webhook URL: https://beu-syllabus-bot.onrender.com/webhook")
        
        # Start Flask server (this will keep the bot running)
        flask_app.run(host='0.0.0.0', port=WEB_PORT, debug=False)
        
    except Exception as e:
        logger.error(f"❌ Bot failed: {e}")
        raise

# ================== MAIN ENTRY POINT ==================
if __name__ == "__main__":
    logger.info("🚀 BEU Syllabus Bot Starting on Render!")
    logger.info(f"Base Directory: {BASE_DIR}")
    
    if not TOKEN:
        logger.error("❌ BOT_TOKEN environment variable not set!")
        raise ValueError("BOT_TOKEN is required")
    
    try:
        bot_info = bot.get_me()
        logger.info(f"✅ Bot Username: @{bot_info.username}")
        logger.info(f"✅ Bot ID: {bot_info.id}")
    except Exception as e:
        logger.error(f"❌ Failed to get bot info: {e}")
        raise
    
    logger.info(f"📚 Total Semesters: {len(SYLLABUS)}")
    
    # Start daily reset thread
    try:
        reset_thread = threading.Thread(target=daily_reset, daemon=True)
        reset_thread.start()
        logger.info("✅ Daily reset scheduler started")
    except Exception as e:
        logger.warning(f"⚠️ Daily reset scheduler not started: {e}")
    
    # Run bot with webhook (this will block)
    run_bot_with_webhook()