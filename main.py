import logging
import os
import threading
import time
from datetime import datetime, timedelta

from flask import Flask, request, jsonify
import telebot

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

# Register Handlers
register_base_handlers(bot, analytics, user_session)
register_syllabus_handlers(bot, analytics, user_session)
register_admin_handlers(bot, analytics)
register_callback_handlers(bot, analytics)

# ================== FLASK WEB SERVER & WEBHOOK ROUTE ==================
flask_app = Flask(__name__)

# Render URL Environment Variable से उठाएगा (उदा. https://your-app.onrender.com)
RENDER_EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL")

@flask_app.route('/')
def health():
    return "✅ BEU Syllabus Bot is running via Webhook!", 200

@flask_app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "users": len(analytics.total_users),
        "downloads": analytics.get_total_downloads()
    }), 200

# Telegram Webhook Endpoint
@flask_app.route(f'/{TOKEN}', methods=['POST'])
def telegram_webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'OK', 200
    else:
        return 'Invalid Content-Type', 403

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
        except Exception as e:
            logger.error(f"Error in daily_reset: {e}")
            time.sleep(3600)

# ================== WEBHOOK SETUP ==================
def setup_webhook():
    if not RENDER_EXTERNAL_URL:
        logger.error("❌ RENDER_EXTERNAL_URL environment variable is missing!")
        return

    webhook_url = f"{RENDER_EXTERNAL_URL.rstrip('/')}/{TOKEN}"
    try:
        # पुरानी पेंडिंग रिक्वेस्ट हटाएं और नया वेबहुक सेट करें
        bot.remove_webhook()
        time.sleep(1)
        bot.set_webhook(url=webhook_url)
        logger.info(f"✅ Webhook successfully set to: {webhook_url}")
    except Exception as e:
        logger.error(f"❌ Failed to set webhook: {e}")

# ================== MAIN ENTRY POINT ==================
if __name__ == "__main__":
    logger.info("🚀 BEU Syllabus Bot Starting on Render (Webhook Mode)!")
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
    
    # Setup Webhook
    setup_webhook()
    
    # Run Flask Web Server (Render इसी पोर्ट पर ट्रैफिक भेजेगा)
    flask_app.run(host='0.0.0.0', port=int(WEB_PORT), debug=False)
