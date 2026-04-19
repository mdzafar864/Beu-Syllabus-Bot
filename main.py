import telebot
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import os
import json
from datetime import datetime, date, timedelta
import logging
from typing import Dict, Set, Optional
import threading
import time
import signal
import sys
from pathlib import Path

# ================== CONFIGURATION ==================
BASE_DIR = Path(__file__).parent

# Setup logging with rotation
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "@EngineersPathwayOfficial"
YOUTUBE_LINK = "https://youtube.com/@engineerspathwayofficial"
ADMIN_ID = 5861904079

# Railway specific settings
PORT = int(os.environ.get('PORT', 8080))

# ================== SYLLABUS DATABASE ==================
SYLLABUS = {
    "1st New": {
        "CE": "https://drive.google.com/uc?export=download&id=1Qd3X732fBWyEax1GTudkBWn7fpe57CgA",
        "CS": "https://drive.google.com/uc?export=download&id=1Zp-UAEgj72UstczPS_wSIBtlPU48USal",
        "EE": "https://drive.google.com/uc?export=download&id=1dZCtmM7w3H9dRpsWMlDhhJZNvFOiA1up",
        "ECE": "https://drive.google.com/uc?export=download&id=14cLD5aiYQp_2U3qKN16pa7U4fowBMg3J",
        "ME": "https://drive.google.com/uc?export=download&id=1yYB-UOYnpkOCYspJeZv83o7Rjy3wfcB8"
    },
    "1st Old": {
        "CE": "https://drive.google.com/uc?export=download&id=1iRWghHRyCP6WPZ3Xoc0DdScIytir3xRn",
        "CS": "https://drive.google.com/uc?export=download&id=1EHpLPUo0_7086gFmk2WRZv2fMw93Jcdb",
        "EE": "https://drive.google.com/uc?export=download&id=1BtS61CEIOidszDe5FLBVQUake_8RQZlK",
        "ECE": "https://drive.google.com/uc?export=download&id=1t57gqcXtYajz6p5q6FXtcBVPb-mUgX1m",
        "ME": "https://drive.google.com/uc?export=download&id=1gyWaJKhhcZNmSF9WlWfqRXfnTeA87hvY"
    },
    "2nd New": {
        "CE": "https://drive.google.com/uc?export=download&id=13q_AFXP9e2AWyHHtHWp_Fm4bRgtME3qv",
        "CS": "https://drive.google.com/uc?export=download&id=15Y2Vsq8xe3Cl2Sc4BcXtL4XQMsqwKIFh",
        "EE": "https://drive.google.com/uc?export=download&id=1wgmEj8RSBWleYUZ1JjzD7tICuiQgJEDW",
        "ECE": "https://drive.google.com/uc?export=download&id=1THqchJygHP7BVVQjj-kf4YmMHBrjfA_x",
        "ME": "https://drive.google.com/uc?export=download&id=1hhAgOvC2LvbBRv6f7n1MSHPxD9MBVgsy"
    },
    "2nd Old": {
        "CE": "https://drive.google.com/uc?export=download&id=1jW97lTtufHT26vkRP6KISUiKWSYe6F3o",
        "CS": "https://drive.google.com/uc?export=download&id=16JynS8hA5JtsSlIc3-HBUPqI9o1F2ziN",
        "EE": "https://drive.google.com/uc?export=download&id=1CrAHd-0bwzESjiLtb-AQwOeKtopyiJm9",
        "ECE": "https://drive.google.com/uc?export=download&id=1eJQJy3I853QoqfNzOT5XFUgncJKxbnv6",
        "ME": "https://drive.google.com/uc?export=download&id=1xwhvlJIQJRCqKLCPTKeOOdjzkUgr8S5U"
    },
    "3rd New": {
        "CE": "https://drive.google.com/uc?export=download&id=1GzMwwCkUrHPmc5fgyWOxOSsPof9dQZO8",
        "CS": "https://drive.google.com/uc?export=download&id=18tjQnI2qGtbSzRWEp08KqKY4gDvE25em",
        "IOT": "https://drive.google.com/uc?export=download&id=1DyoqlnntdtG-RA0ET1wH4FrR-DOB3mtF",
        "EE": "https://drive.google.com/uc?export=download&id=1nKpL1rXXa7EGJqbvDkmEem1uh74QWjOU",
        "ECE": "https://drive.google.com/uc?export=download&id=1kWy1_zhggLM9U4jrkTzGWNdLcE-4QXMr",
        "ME": "https://drive.google.com/uc?export=download&id=14yS8pyf83vIA1vs-_DbAvWbYpF8y6gc9"
    },
    "3rd Old": {
        "CE": "https://drive.google.com/uc?export=download&id=1IS4EV9JvOfoLW3cYRW7U-qBkXyRAvFlD",
        "CS": "https://drive.google.com/uc?export=download&id=1ZlU22NFGirTuV01jKYiG9zdSU_IO29-t",
        "EE": "https://drive.google.com/uc?export=download&id=1D2gAZlW299s9f60wcdicGSZK7DpZVXkc",
        "ECE": "https://drive.google.com/uc?export=download&id=1auOpeh5UX4E23rnxIQo1K9TdFrqSXrm0",
        "ME": "https://drive.google.com/uc?export=download&id=1XE_l1tfHGZHMDIxU6KNlcjlqiKxKN-ZW"
    },
    "4th": {
        "CE": "https://drive.google.com/uc?export=download&id=17w5zTFNaWUOg7S_vUrqW_AxtMyf7bPdU",
        "CS": "https://drive.google.com/uc?export=download&id=1ODCj6Omx6dUuHR-Cmwh4iu37TaMQyTLn",
        "EE": "https://drive.google.com/uc?export=download&id=1G-cJOckwjZRoaDz0Nnw-CphpqBcZztA7",
        "ECE": "https://drive.google.com/uc?export=download&id=1nkfp0xRno6_ybJSWqZ6_ryiwI4aNsjXh",
        "ME": "https://drive.google.com/uc?export=download&id=1jVvYbUmth-RIbhLBXbDf3ooB8zgz8fSc"
    },
    "5th": {
        "CE": "https://drive.google.com/uc?export=download&id=1tGXDItZ5g-AsnsXN0KmMifbA36vgxA0C",
        "CS": "https://drive.google.com/uc?export=download&id=1SZdAT8a1vrIfrMPYjl0Q-0cc3hBba3z3",
        "EE": "https://drive.google.com/uc?export=download&id=1MA_tDBF7Fuvg8OGgn8bzg4mHSUTmQ-dC",
        "ECE": "https://drive.google.com/uc?export=download&id=1dJV_E7tPdhmmA7IutIDeaDMz3rxYb9XR",
        "ME": "https://drive.google.com/uc?export=download&id=1FW1-YDLvthfdG52szzsLzTIU9DOI03bc"
    },
    "6th": {
        "CE": "https://drive.google.com/uc?export=download&id=1MxzSoTSdMgCvgCPiDFsDjVuu4QaJCQge",
        "CS": "https://drive.google.com/uc?export=download&id=1ckXxGY5kdHmxlAIGsq-NfDskA4Mj_xQj",
        "EE": "https://drive.google.com/uc?export=download&id=1obhgEQmyRzDg1XPG7Gc6u5SyMugXN9bn",
        "ECE": "https://drive.google.com/uc?export=download&id=1reUmWqura-4UnEx7tpjv6wANADxvW_lc",
        "ME": "https://drive.google.com/uc?export=download&id=19UDBkvdYqgMqRzV_Fgre8vq8utOapy2q"
    },
    "7th": {
        "CE": "https://drive.google.com/uc?export=download&id=1Qy64E3CCdfhQvD8PaihwPDFVz2FwDqGr",
        "CS": "https://drive.google.com/uc?export=download&id=1uW4HVIaLErhWIyj36Lday4JMH1ZfuLEp",
        "EE": "https://drive.google.com/uc?export=download&id=1ey1jhsveL-eO0gc0FgwlNs7U05qRQHp5",
        "ECE": "https://drive.google.com/uc?export=download&id=1aDSSzOz8kWsmO0oJV7Z5CZ2lnCXReEqq",
        "ME": "https://drive.google.com/uc?export=download&id=1kMv43ZFJMctH_iRYbI230GCNN4UkZYud"
    },
    "8th": {
        "EE": "https://drive.google.com/uc?export=download&id=1BwL_f3KCmWzuEulEth3G3hQw5sxLvBOy",
        "ME": "https://drive.google.com/uc?export=download&id=1PPkfTohITDMkIFNuw836gSOSUjCFtt3n"
    }
}

BRANCH_EMOJIS = {
    "CE": "🏗️ Civil",
    "CS": "💻 Computer Science",
    "EE": "⚡ Electrical",
    "ECE": "📡 Electronics",
    "ME": "🔧 Mechanical",
    "IOT": "🌐 IoT"
}

# ================== BOT INITIALIZATION ==================
bot = telebot.TeleBot(TOKEN, parse_mode='Markdown')

# ================== USER DATA MANAGEMENT ==================
class UserSession:
    def __init__(self):
        self.data: Dict[int, Dict] = {}
    
    def get(self, user_id: int) -> Optional[Dict]:
        return self.data.get(user_id)
    
    def set(self, user_id: int, key: str, value: any):
        if user_id not in self.data:
            self.data[user_id] = {}
        self.data[user_id][key] = value
    
    def clear(self, user_id: int):
        if user_id in self.data:
            del self.data[user_id]

user_session = UserSession()

# ================== ANALYTICS SYSTEM ==================
class Analytics:
    def __init__(self, filename: str = "analytics.json"):
        self.filename = str(BASE_DIR / filename)
        self.total_users: Set[int] = set()
        self.daily_active: Set[int] = set()
        self.command_stats: Dict[str, int] = {}
        self.daily_downloads: Dict[str, int] = {}
        self.load()
    
    def load(self):
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    self.total_users = set(data.get('total_users', []))
                    self.daily_active = set(data.get('daily_active', []))
                    self.command_stats = data.get('command_stats', {})
                    self.daily_downloads = data.get('daily_downloads', {})
                    logger.info("Analytics loaded")
        except Exception as e:
            logger.error(f"Error loading analytics: {e}")
            self.save()
    
    def save(self):
        try:
            with open(self.filename, 'w') as f:
                json.dump({
                    'total_users': list(self.total_users),
                    'daily_active': list(self.daily_active),
                    'command_stats': self.command_stats,
                    'daily_downloads': self.daily_downloads,
                    'last_reset': str(date.today())
                }, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving analytics: {e}")
    
    def track_user(self, user_id: int, command: str = "start"):
        self.total_users.add(user_id)
        self.daily_active.add(user_id)
        self.command_stats[command] = self.command_stats.get(command, 0) + 1
        self.save()
    
    def track_download(self, semester: str, branch: str):
        key = f"{semester}_{branch}"
        self.daily_downloads[key] = self.daily_downloads.get(key, 0) + 1
        self.save()
    
    def reset_daily(self):
        self.daily_active.clear()
        self.daily_downloads.clear()
        self.save()
        logger.info("Daily analytics reset")

analytics = Analytics()

# ================== UI COMPONENTS ==================
class MenuBuilder:
    @staticmethod
    def main_menu() -> ReplyKeyboardMarkup:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        buttons = ["📚 Syllabus", "📊 Stats", "ℹ️ Help", "⭐ Feedback", "🔄 Reset"]
        markup.add(*buttons)
        return markup
    
    @staticmethod
    def semester_menu() -> ReplyKeyboardMarkup:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        semesters = list(SYLLABUS.keys())
        buttons = [f"📖 {sem}" for sem in semesters]
        markup.add(*buttons)
        markup.add("🏠 Main Menu")
        return markup
    
    @staticmethod
    def branch_menu(semester: str) -> ReplyKeyboardMarkup:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        branches = SYLLABUS[semester].keys()
        buttons = [f"{BRANCH_EMOJIS.get(b, b)}" for b in branches]
        markup.add(*buttons)
        markup.add("🔙 Back to Semesters", "🏠 Main Menu")
        return markup
    
    @staticmethod
    def force_join_markup() -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("📢 Join Channel", url="https://t.me/EngineersPathwayOfficial"),
            InlineKeyboardButton("▶️ Subscribe YouTube", url=YOUTUBE_LINK),
            InlineKeyboardButton("✅ I've Joined", callback_data="check_join")
        )
        return markup

# ================== FORCE JOIN HANDLER ==================
def is_member(user_id: int) -> bool:
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        return False

# ================== COMMAND HANDLERS ==================
@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def verify_join(call):
    try:
        bot.answer_callback_query(call.id)
        
        if is_member(call.from_user.id):
            bot.edit_message_text(
                "✅ Access Granted! Welcome!",
                call.message.chat.id,
                call.message.message_id
            )
            bot.send_message(
                call.message.chat.id,
                "🎉 Welcome to BEU Syllabus Bot!\nUse the menu below.",
                reply_markup=MenuBuilder.main_menu()
            )
            analytics.track_user(call.from_user.id, "verified")
        else:
            bot.answer_callback_query(call.id, "❌ Please join channel first!", show_alert=True)
    except Exception as e:
        logger.error(f"Verify join error: {e}")

@bot.message_handler(commands=['start', 'menu'])
def start(message):
    try:
        if not is_member(message.chat.id):
            bot.send_message(
                message.chat.id,
                "🔒 Please join our channel first: @EngineersPathwayOfficial",
                reply_markup=MenuBuilder.force_join_markup()
            )
            return
        
        analytics.track_user(message.chat.id, "start")
        user_session.clear(message.chat.id)
        
        bot.send_message(
            message.chat.id,
            "🎓 *BEU Syllabus Bot*\n\n"
            "📚 Select 'Syllabus' to download\n"
            "📊 Check stats for usage\n"
            "⭐ Send feedback to improve",
            reply_markup=MenuBuilder.main_menu()
        )
    except Exception as e:
        logger.error(f"Start error: {e}")

@bot.message_handler(func=lambda m: m.text == "📚 Syllabus")
def show_semesters(message):
    try:
        if not is_member(message.chat.id):
            return
        
        sem_text = "📖 *Select Semester:*\n\n"
        for i, sem in enumerate(SYLLABUS.keys(), 1):
            sem_text += f"{i}. {sem}\n"
        
        bot.send_message(
            message.chat.id,
            sem_text,
            reply_markup=MenuBuilder.semester_menu()
        )
    except Exception as e:
        logger.error(f"Show semesters error: {e}")

@bot.message_handler(func=lambda m: m.text and m.text.startswith("📖 "))
def semester_selected(message):
    try:
        if not is_member(message.chat.id):
            return
        
        semester = message.text.replace("📖 ", "")
        if semester in SYLLABUS:
            user_session.set(message.chat.id, "semester", semester)
            
            branch_text = f"📚 *{semester} Semester*\n\nBranches:\n"
            for branch in SYLLABUS[semester].keys():
                branch_text += f"• {BRANCH_EMOJIS.get(branch, branch)}\n"
            
            bot.send_message(
                message.chat.id,
                branch_text,
                reply_markup=MenuBuilder.branch_menu(semester)
            )
    except Exception as e:
        logger.error(f"Semester select error: {e}")

@bot.message_handler(func=lambda m: m.text in ["🔙 Back to Semesters", "🏠 Main Menu"])
def handle_navigation(message):
    try:
        if message.text == "🔙 Back to Semesters":
            show_semesters(message)
        else:
            start(message)
    except Exception as e:
        logger.error(f"Navigation error: {e}")

@bot.message_handler(func=lambda m: m.text in list(BRANCH_EMOJIS.values()))
def branch_selected(message):
    try:
        if not is_member(message.chat.id):
            return
        
        session = user_session.get(message.chat.id)
        if not session or not session.get("semester"):
            bot.send_message(message.chat.id, "⚠️ Select semester first!")
            return
        
        semester = session["semester"]
        
        branch = None
        for b, name in BRANCH_EMOJIS.items():
            if name == message.text:
                branch = b
                break
        
        if not branch:
            return
        
        file_url = SYLLABUS[semester][branch]
        analytics.track_download(semester, branch)
        
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("⬇️ Download", url=file_url),
            InlineKeyboardButton("📤 Share", switch_inline_query=f"{semester} {branch}")
        )
        
        bot.send_document(
            message.chat.id,
            file_url,
            caption=f"📚 *{semester} - {BRANCH_EMOJIS.get(branch)}*\n📊 Downloads: {analytics.daily_downloads.get(f'{semester}_{branch}', 0)}",
            reply_markup=markup
        )
    except Exception as e:
        logger.error(f"Branch select error: {e}")
        bot.send_message(message.chat.id, "⚠️ Error! Please try again.")

@bot.message_handler(func=lambda m: m.text == "📊 Stats")
def show_stats(message):
    try:
        stats_text = (
            f"📊 *Statistics*\n\n"
            f"👥 Users: {len(analytics.total_users)}\n"
            f"📅 Active: {len(analytics.daily_active)}\n"
            f"📚 Downloads: {sum(analytics.daily_downloads.values())}"
        )
        bot.send_message(message.chat.id, stats_text)
    except Exception as e:
        logger.error(f"Stats error: {e}")

@bot.message_handler(func=lambda m: m.text == "ℹ️ Help")
def show_help(message):
    try:
        help_text = (
            "📚 *Help*\n\n"
            "1. Click 'Syllabus'\n"
            "2. Select semester\n"
            "3. Choose branch\n"
            "4. Download PDF\n\n"
            "Commands: /start, /menu"
        )
        bot.send_message(message.chat.id, help_text)
    except Exception as e:
        logger.error(f"Help error: {e}")

@bot.message_handler(func=lambda m: m.text == "⭐ Feedback")
def get_feedback(message):
    try:
        msg = bot.send_message(message.chat.id, "💬 Send your feedback:")
        bot.register_next_step_handler(msg, process_feedback)
    except Exception as e:
        logger.error(f"Feedback error: {e}")

def process_feedback(message):
    try:
        user = message.from_user
        feedback_msg = (
            f"📝 *Feedback*\n"
            f"User: {user.first_name}\n"
            f"ID: `{user.id}`\n"
            f"Msg: {message.text}"
        )
        bot.send_message(ADMIN_ID, feedback_msg)
        bot.send_message(message.chat.id, "✅ Thanks for your feedback!")
    except Exception as e:
        logger.error(f"Process feedback error: {e}")

@bot.message_handler(func=lambda m: m.text == "🔄 Reset")
def reset_session(message):
    try:
        user_session.clear(message.chat.id)
        bot.send_message(message.chat.id, "🔄 Reset done! Start fresh with /start")
    except Exception as e:
        logger.error(f"Reset error: {e}")

@bot.message_handler(func=lambda m: True)
def unknown(message):
    try:
        bot.send_message(message.chat.id, "❓ Use menu buttons or /start")
    except:
        pass

# ================== HEALTH CHECK SERVER ==================
def run_health_server():
    try:
        from flask import Flask, jsonify
        app = Flask(__name__)
        
        @app.route('/')
        @app.route('/health')
        def health():
            return jsonify({
                "status": "alive",
                "users": len(analytics.total_users),
                "downloads": sum(analytics.daily_downloads.values()),
                "uptime": "running"
            }), 200
        
        app.run(host='0.0.0.0', port=PORT)
    except Exception as e:
        logger.warning(f"Health server: {e}")

# ================== MAIN WITH AUTO RESTART ==================
def main():
    # Start health server
    threading.Thread(target=run_health_server, daemon=True).start()
    
    # Start bot with auto-restart
    while True:
        try:
            logger.info("🚀 Bot started!")
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            logger.error(f"Bot error: {e}")
            logger.info("Restarting in 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    # Graceful shutdown
    def signal_handler(sig, frame):
        logger.info("Shutting down...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    if not TOKEN:
        logger.error("BOT_TOKEN not set!")
        sys.exit(1)
    
    logger.info(f"Bot token: {TOKEN[:10]}...")
    main()