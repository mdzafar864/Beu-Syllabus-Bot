import telebot
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
import os
import json
from datetime import datetime, date
import logging
from typing import Dict, Set, Optional

# ================== CONFIGURATION ==================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "@EngineersPathwayOfficial"
YOUTUBE_LINK = "https://youtube.com/@engineerspathwayofficial"

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
bot = telebot.TeleBot(TOKEN)

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
        self.filename = filename
        self.total_users: Set[int] = set()
        self.daily_active: Set[int] = set()
        self.command_stats: Dict[str, int] = {}
        self.daily_downloads: Dict[str, int] = {}
        self.load()
    
    def load(self):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.total_users = set(data.get('total_users', []))
                self.daily_active = set(data.get('daily_active', []))
                self.command_stats = data.get('command_stats', {})
                self.daily_downloads = data.get('daily_downloads', {})
        except FileNotFoundError:
            self.save()
    
    def save(self):
        with open(self.filename, 'w') as f:
            json.dump({
                'total_users': list(self.total_users),
                'daily_active': list(self.daily_active),
                'command_stats': self.command_stats,
                'daily_downloads': self.daily_downloads,
                'last_reset': str(date.today())
            }, f, indent=2)
    
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
        markup.add(*buttons, "🔙 Main Menu")
        return markup
    
    @staticmethod
    def branch_menu(semester: str) -> ReplyKeyboardMarkup:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        branches = SYLLABUS[semester].keys()
        buttons = [f"{BRANCH_EMOJIS.get(b, b)}" for b in branches]
        markup.add(*buttons, "🔙 Back", "🏠 Home")
        return markup
    
    @staticmethod
    def force_join_markup() -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("📢 Join Telegram Channel", url="https://t.me/EngineersPathwayOfficial"),
            InlineKeyboardButton("▶️ Subscribe YouTube", url=YOUTUBE_LINK),
            InlineKeyboardButton("✅ I've Joined & Subscribed", callback_data="check_join")
        )
        return markup

# ================== FORCE JOIN HANDLER ==================
def is_member(user_id: int) -> bool:
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        logger.error(f"Membership check failed for {user_id}: {e}")
        return False

def send_join_required(message):
    bot.send_message(
        message.chat.id,
        "🔒 *Access Restricted*\n\n"
        "To access the syllabus and all features, you must join our community:\n\n"
        "✅ Join Telegram Channel\n"
        "✅ Subscribe to YouTube\n\n"
        "After joining, click the button below to verify access.",
        reply_markup=MenuBuilder.force_join_markup(),
        parse_mode='Markdown'
    )

# ================== COMMAND HANDLERS ==================
@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def verify_join(call):
    if is_member(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ Access Granted! Welcome aboard!")
        bot.send_message(
            call.message.chat.id,
            "🎉 *Access Verified!* 🎉\n\n"
            "Welcome to BEU Syllabus Bot!\n"
            "Use the menu below to get started.",
            reply_markup=MenuBuilder.main_menu(),
            parse_mode='Markdown'
        )
        analytics.track_user(call.from_user.id, "verified")
    else:
        bot.answer_callback_query(
            call.id, 
            "❌ Please join the Telegram channel and subscribe to YouTube first!", 
            show_alert=True
        )

@bot.message_handler(commands=['start', 'menu'])
def start(message):
    if not is_member(message.chat.id):
        send_join_required(message)
        return
    
    analytics.track_user(message.chat.id, "start")
    
    welcome_text = (
        "🎓 *BEU Syllabus Bot* 🎓\n\n"
        "📚 *Available Features:*\n"
        "• Download semester-wise syllabus\n"
        "• Branch-wise syllabus access\n"
        "• Quick PDF downloads\n\n"
        "💡 *How to use:*\n"
        "1️⃣ Click '📚 Syllabus'\n"
        "2️⃣ Select your semester\n"
        "3️⃣ Choose your branch\n"
        "4️⃣ Download your syllabus!\n\n"
        "📊 Check stats to see bot usage!"
    )
    
    bot.send_message(
        message.chat.id,
        welcome_text,
        reply_markup=MenuBuilder.main_menu(),
        parse_mode='Markdown'
    )

@bot.message_handler(func=lambda m: m.text == "📚 Syllabus")
def show_semesters(message):
    if not is_member(message.chat.id):
        send_join_required(message)
        return
    
    sem_text = "📖 *Select Your Semester:*\n\n"
    for i, sem in enumerate(SYLLABUS.keys(), 1):
        sem_text += f"{i}. {sem}\n"
    
    bot.send_message(
        message.chat.id,
        sem_text,
        reply_markup=MenuBuilder.semester_menu(),
        parse_mode='Markdown'
    )

@bot.message_handler(func=lambda m: m.text.startswith("📖 "))
def semester_selected(message):
    if not is_member(message.chat.id):
        send_join_required(message)
        return
    
    semester = message.text.replace("📖 ", "")
    if semester in SYLLABUS:
        user_session.set(message.chat.id, "semester", semester)
        
        branches = SYLLABUS[semester].keys()
        branch_text = f"📚 *{semester} Semester*\n\n"
        branch_text += "Available Branches:\n"
        for branch in branches:
            branch_text += f"• {BRANCH_EMOJIS.get(branch, branch)}\n"
        
        bot.send_message(
            message.chat.id,
            branch_text,
            reply_markup=MenuBuilder.branch_menu(semester),
            parse_mode='Markdown'
        )

@bot.message_handler(func=lambda m: m.text in BRANCH_EMOJIS.values() or m.text in SYLLABUS.get(user_session.get(m.chat.id, {}).get("semester", ""), {}).keys())
def branch_selected(message):
    if not is_member(message.chat.id):
        send_join_required(message)
        return
    
    session = user_session.get(message.chat.id)
    if not session or "semester" not in session:
        bot.send_message(
            message.chat.id,
            "⚠️ Please select a semester first!",
            reply_markup=MenuBuilder.semester_menu()
        )
        return
    
    semester = session["semester"]
    
    # Handle both emoji and plain branch names
    selected = message.text
    branch = None
    for b, name in BRANCH_EMOJIS.items():
        if name == selected:
            branch = b
            break
    if not branch and selected in SYLLABUS[semester]:
        branch = selected
    
    if not branch or branch not in SYLLABUS[semester]:
        bot.send_message(message.chat.id, "❌ Invalid branch selection!")
        return
    
    file_url = SYLLABUS[semester][branch]
    analytics.track_download(semester, branch)
    
    # Send loading indicator
    bot.send_chat_action(message.chat.id, 'upload_document')
    
    try:
        bot.send_document(
            message.chat.id,
            file_url,
            caption=f"📄 *{semester} Semester - {BRANCH_EMOJIS.get(branch, branch)} Syllabus*\n\n"
                   f"📅 Downloaded: {datetime.now().strftime('%d/%m/%Y')}\n"
                   f"📊 Total downloads: {analytics.daily_downloads.get(f'{semester}_{branch}', 0)}",
            parse_mode='Markdown'
        )
        logger.info(f"Downloaded: {semester} - {branch} by user {message.chat.id}")
    except Exception as e:
        logger.error(f"Download failed: {e}")
        bot.send_message(
            message.chat.id,
            f"⚠️ Download failed!\n\n"
            f"📥 Direct Link:\n{file_url}\n\n"
            f"Click the link above to download manually.",
            disable_web_page_preview=True
        )

@bot.message_handler(func=lambda m: m.text == "📊 Stats")
def show_stats(message):
    if not is_member(message.chat.id):
        send_join_required(message)
        return
    
    stats_text = (
        "📊 *Bot Statistics*\n\n"
        f"👥 *Total Users:* {len(analytics.total_users):,}\n"
        f"📅 *Active Today:* {len(analytics.daily_active):,}\n"
        f"📚 *Total Downloads:* {sum(analytics.daily_downloads.values()):,}\n\n"
        "📈 *Popular Downloads:*\n"
    )
    
    top_downloads = sorted(analytics.daily_downloads.items(), key=lambda x: x[1], reverse=True)[:5]
    if top_downloads:
        for sem_branch, count in top_downloads:
            sem, branch = sem_branch.split('_')
            stats_text += f"• {sem} - {branch}: {count}\n"
    else:
        stats_text += "• No downloads yet\n"
    
    stats_text += f"\n🕐 Last updated: {datetime.now().strftime('%H:%M:%S')}"
    
    bot.send_message(message.chat.id, stats_text, parse_mode='Markdown')

@bot.message_handler(func=lambda m: m.text == "ℹ️ Help")
def show_help(message):
    help_text = (
        "📚 *Help & Guide*\n\n"
        "*How to use:*\n"
        "1. Tap '📚 Syllabus'\n"
        "2. Choose your semester\n"
        "3. Select your branch\n"
        "4. Download PDF\n\n"
        
        "*Commands:*\n"
        "/start - Restart bot\n"
        "/menu - Show main menu\n"
        
        "*Need Support?*\n"
        "Join our Telegram channel for updates and support!\n\n"
        
        "📢 *Channel:* @EngineersPathwayOfficial\n"
        "▶️ *YouTube:* Engineers Pathway Official"
    )
    
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("📢 Channel", url="https://t.me/EngineersPathwayOfficial"),
        InlineKeyboardButton("▶️ YouTube", url=YOUTUBE_LINK)
    )
    
    bot.send_message(
        message.chat.id,
        help_text,
        reply_markup=markup,
        parse_mode='Markdown'
    )

@bot.message_handler(func=lambda m: m.text == "⭐ Feedback")
def get_feedback(message):
    feedback_text = (
        "💬 *Send Feedback*\n\n"
        "We value your feedback! Please send your:\n"
        "• Suggestions for improvement\n"
        "• Bug reports\n"
        "• Feature requests\n\n"
        "Just type your message below, and it will be forwarded to the admin."
    )
    bot.send_message(message.chat.id, feedback_text, parse_mode='Markdown')
    bot.register_next_step_handler(message, process_feedback)

def process_feedback(message):
    feedback_content = message.text
    admin_id = os.getenv("ADMIN_ID")
    
    if admin_id:
        feedback_msg = (
            f"📝 *New Feedback*\n\n"
            f"👤 User: {message.from_user.first_name} (@{message.from_user.username})\n"
            f"🆔 ID: {message.chat.id}\n"
            f"💬 Message:\n{feedback_content}"
        )
        try:
            bot.send_message(admin_id, feedback_msg, parse_mode='Markdown')
            bot.send_message(
                message.chat.id,
                "✅ Thank you for your feedback! We'll review it soon.",
                reply_markup=MenuBuilder.main_menu()
            )
        except Exception as e:
            logger.error(f"Failed to send feedback to admin: {e}")
            bot.send_message(
                message.chat.id,
                "⚠️ Feedback sent! (Admin notification failed but we received it)",
                reply_markup=MenuBuilder.main_menu()
            )
    else:
        bot.send_message(
            message.chat.id,
            "✅ Feedback recorded! Thank you for helping us improve.",
            reply_markup=MenuBuilder.main_menu()
        )

@bot.message_handler(func=lambda m: m.text == "🔄 Reset")
def reset_session(message):
    user_session.clear(message.chat.id)
    bot.send_message(
        message.chat.id,
        "🔄 Session reset! You can start fresh now.",
        reply_markup=MenuBuilder.main_menu()
    )

@bot.message_handler(func=lambda m: m.text == "🔙 Back")
def go_back(message):
    show_semesters(message)

@bot.message_handler(func=lambda m: m.text == "🏠 Home")
def go_home(message):
    start(message)

@bot.message_handler(func=lambda m: m.text == "🔙 Main Menu")
def main_menu_back(message):
    start(message)

@bot.message_handler(func=lambda m: True)
def handle_unknown(message):
    bot.send_message(
        message.chat.id,
        "❓ *Unknown Command*\n\n"
        "Please use the menu buttons below or type /start to restart.",
        reply_markup=MenuBuilder.main_menu(),
        parse_mode='Markdown'
    )

# ================== ERROR HANDLER ==================
@bot.message_handler(content_types=['text'])
def handle_errors(message):
    try:
        bot.send_message(
            message.chat.id,
            "⚠️ Something went wrong. Please try again or use /start to restart.",
            reply_markup=MenuBuilder.main_menu()
        )
    except Exception as e:
        logger.error(f"Error handler failed: {e}")

# ================== DAILY RESET SCHEDULER ==================
import threading
import time

def daily_reset():
    while True:
        now = datetime.now()
        # Reset at midnight
        next_reset = datetime(now.year, now.month, now.day) + timedelta(days=1)
        time.sleep((next_reset - now).total_seconds())
        analytics.reset_daily()
        logger.info("Daily analytics reset completed")

# Start daily reset thread if needed
try:
    from datetime import timedelta
    reset_thread = threading.Thread(target=daily_reset, daemon=True)
    reset_thread.start()
except Exception as e:
    logger.warning(f"Daily reset scheduler not started: {e}")

# ================== BOT STARTUP ==================
if __name__ == "__main__":
    logger.info("🚀 BEU Syllabus Bot Started!")
    logger.info(f"Bot Username: @{bot.get_me().username}")
    logger.info(f"Total Semesters: {len(SYLLABUS)}")
    
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
        raise
