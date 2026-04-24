import telebot
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import os
import json
from datetime import datetime, date, timedelta
import logging
from typing import Dict, Set, Optional
import threading
import time
from pathlib import Path
from flask import Flask, request

# ================== CONFIGURATION ==================
BASE_DIR = Path(__file__).parent

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(BASE_DIR / 'bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "@EngineersPathwayOfficial"
YOUTUBE_LINK = "https://youtube.com/@engineerspathwayofficial"
ADMIN_ID = 5861904079  # Your Telegram ID

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

# ================== HELPER FUNCTIONS ==================
def get_download_link(drive_url):
    """Extract download link from Google Drive URL"""
    try:
        if "id=" in drive_url:
            file_id = drive_url.split("id=")[-1]
        elif "/d/" in drive_url:
            file_id = drive_url.split("/d/")[1].split("/")[0]
        else:
            return drive_url
        
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    except:
        return drive_url

# ================== BOT INITIALIZATION ==================
bot = telebot.TeleBot(TOKEN)

# ================== USER DATA MANAGEMENT ==================
class UserSession:
    def __init__(self):
        self.data: Dict[int, Dict] = {}
        self.lock = threading.Lock()
    
    def get(self, user_id: int) -> Optional[Dict]:
        with self.lock:
            return self.data.get(user_id)
    
    def set(self, user_id: int, key: str, value: any):
        with self.lock:
            if user_id not in self.data:
                self.data[user_id] = {}
            self.data[user_id][key] = value
    
    def clear(self, user_id: int):
        with self.lock:
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
        self.lock = threading.Lock()
        self.load()
    
    def load(self):
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    with self.lock:
                        self.total_users = set(data.get('total_users', []))
                        self.daily_active = set(data.get('daily_active', []))
                        self.command_stats = data.get('command_stats', {})
                        self.daily_downloads = data.get('daily_downloads', {})
                    logger.info("Analytics loaded successfully")
        except Exception as e:
            logger.error(f"Error loading analytics: {e}")
            self.save()
    
    def save(self):
        try:
            with self.lock:
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
        with self.lock:
            self.total_users.add(user_id)
            self.daily_active.add(user_id)
            self.command_stats[command] = self.command_stats.get(command, 0) + 1
        self.save()
    
    def track_download(self, semester: str, branch: str):
        key = f"{semester}_{branch}"
        with self.lock:
            self.daily_downloads[key] = self.daily_downloads.get(key, 0) + 1
        self.save()
    
    def reset_daily(self):
        with self.lock:
            self.daily_active.clear()
            self.daily_downloads.clear()
        self.save()
        logger.info("Daily analytics reset completed")

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
    def branch_first_menu() -> ReplyKeyboardMarkup:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        buttons = [f"{BRANCH_EMOJIS.get(b, b)}" for b in BRANCH_EMOJIS.keys()]
        markup.add(*buttons)
        markup.add("🏠 Main Menu")
        return markup
    
    @staticmethod
    def semester_for_branch_menu(branch: str, available_semesters: list) -> ReplyKeyboardMarkup:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        buttons = [f"📖 {sem}" for sem in available_semesters]
        markup.add(*buttons)
        markup.add("🔙 Back to Branches", "🏠 Main Menu")
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
    try:
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
    except Exception as e:
        logger.error(f"Error sending join required message: {e}")

# ================== COMMAND HANDLERS ==================
@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def verify_join(call):
    try:
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
    except Exception as e:
        logger.error(f"Error in verify_join: {e}")

@bot.message_handler(commands=['start', 'menu'])
def start(message):
    try:
        if not is_member(message.chat.id):
            send_join_required(message)
            return
        
        analytics.track_user(message.chat.id, "start")
        user_session.clear(message.chat.id)
        
        welcome_text = (
            "🎓 *BEU Syllabus Bot* 🎓\n\n"
            "📚 *Available Features:*\n"
            "• Download semester-wise syllabus\n"
            "• Branch-wise syllabus access\n"
            "• Share syllabus with friends\n\n"
            "💡 *How to use:*\n"
            "1️⃣ Click '📚 Syllabus'\n"
            "2️⃣ Select your branch\n"
            "3️⃣ Choose your semester\n"
            "4️⃣ Download or share your syllabus!\n\n"
            "📊 Check stats to see bot usage!"
        )
        
        bot.send_message(
            message.chat.id,
            welcome_text,
            reply_markup=MenuBuilder.main_menu(),
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Error in start: {e}")

@bot.message_handler(func=lambda m: m.text == "📚 Syllabus")
def show_branches_first(message):
    try:
        if not is_member(message.chat.id):
            send_join_required(message)
            return
        
        user_session.set(message.chat.id, "step", "waiting_for_branch")
        
        branch_text = "🏗️ *पहले अपनी Branch चुनें:*\n\n"
        for branch, emoji_name in BRANCH_EMOJIS.items():
            branch_text += f"• {emoji_name}\n"
        
        branch_text += "\n💡 *Branch चुनने के बाद Semester select करेंगे*"
        
        bot.send_message(
            message.chat.id,
            branch_text,
            reply_markup=MenuBuilder.branch_first_menu(),
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Error in show_branches_first: {e}")

@bot.message_handler(func=lambda m: m.text in list(BRANCH_EMOJIS.values()))
def branch_selected_first(message):
    try:
        if not is_member(message.chat.id):
            send_join_required(message)
            return
        
        # Find which branch was selected
        selected_branch = None
        for b, name in BRANCH_EMOJIS.items():
            if name == message.text:
                selected_branch = b
                break
        
        if not selected_branch:
            bot.send_message(message.chat.id, "❌ Invalid branch!")
            return
        
        # Store selected branch in session
        user_session.set(message.chat.id, "selected_branch", selected_branch)
        user_session.set(message.chat.id, "step", "waiting_for_semester")
        
        # Find which semesters have this branch
        available_semesters = []
        for sem, branches in SYLLABUS.items():
            if selected_branch in branches:
                available_semesters.append(sem)
        
        if not available_semesters:
            bot.send_message(
                message.chat.id,
                f"❌ {BRANCH_EMOJIS.get(selected_branch, selected_branch)} branch का कोई syllabus उपलब्ध नहीं है।"
            )
            return
        
        # Show semester options
        sem_text = f"📚 *{BRANCH_EMOJIS.get(selected_branch, selected_branch)} Branch*\n\n"
        sem_text += "अब अपना *Semester* चुनें:\n\n"
        for i, sem in enumerate(available_semesters, 1):
            sem_text += f"{i}. {sem}\n"
        
        bot.send_message(
            message.chat.id,
            sem_text,
            reply_markup=MenuBuilder.semester_for_branch_menu(selected_branch, available_semesters),
            parse_mode='Markdown'
        )
        
    except Exception as e:
        logger.error(f"Error in branch_selected_first: {e}")
        bot.send_message(
            message.chat.id,
            "⚠️ Error! Please try again.",
            reply_markup=MenuBuilder.main_menu()
        )

@bot.message_handler(func=lambda m: m.text and m.text.startswith("📖 "))
def semester_after_branch(message):
    try:
        if not is_member(message.chat.id):
            send_join_required(message)
            return
        
        semester = message.text.replace("📖 ", "")
        session = user_session.get(message.chat.id)
        
        if not session or not session.get("selected_branch"):
            bot.send_message(
                message.chat.id,
                "⚠️ पहले Branch चुनें!",
                reply_markup=MenuBuilder.branch_first_menu()
            )
            return
        
        branch = session["selected_branch"]
        
        # Check if syllabus exists for this branch and semester
        if semester not in SYLLABUS or branch not in SYLLABUS[semester]:
            bot.send_message(
                message.chat.id,
                f"❌ {BRANCH_EMOJIS.get(branch, branch)} branch का {semester} semester का syllabus उपलब्ध नहीं है।"
            )
            return
        
        original_url = SYLLABUS[semester][branch]
        download_url = get_download_link(original_url)
        
        analytics.track_download(semester, branch)
        
        # Create download markup - ONLY DOWNLOAD AND SHARE BUTTONS
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("⬇️ Download PDF", url=download_url),
            InlineKeyboardButton("📤 Share Syllabus", switch_inline_query=f"{semester} {branch} Syllabus")
        )
        
        bot.send_chat_action(message.chat.id, 'typing')
        
        try:
            bot.send_document(
                message.chat.id,
                download_url,
                caption=f"📚 *{semester} Semester - {BRANCH_EMOJIS.get(branch, branch)} Syllabus*\n\n"
                       f"📅 *Requested:* {datetime.now().strftime('%d %b %Y, %I:%M %p')}\n"
                       f"📊 *Downloads Today:* {analytics.daily_downloads.get(f'{semester}_{branch}', 0)}",
                reply_markup=markup,
                parse_mode='Markdown'
            )
            logger.info(f"Syllabus sent: {semester} - {branch} to user {message.chat.id}")
        except Exception as doc_error:
            logger.error(f"Document send failed: {doc_error}")
            bot.send_message(
                message.chat.id,
                f"📚 *{semester} Semester - {BRANCH_EMOJIS.get(branch, branch)} Syllabus*\n\n"
                f"✅ Syllabus ready!\n\n"
                f"📥 [Click here to download]({download_url})",
                reply_markup=markup,
                parse_mode='Markdown'
            )
        
    except Exception as e:
        logger.error(f"Error in semester_after_branch: {e}")
        bot.send_message(
            message.chat.id,
            "⚠️ Error! Please try again.",
            reply_markup=MenuBuilder.main_menu()
        )

@bot.message_handler(func=lambda m: m.text == "📊 Stats")
def show_stats(message):
    try:
        if not is_member(message.chat.id):
            send_join_required(message)
            return
        
        stats_text = (
            "📊 *Bot Statistics* 📊\n\n"
            f"👥 *Total Users:* {len(analytics.total_users)}\n"
            f"📱 *Active Today:* {len(analytics.daily_active)}\n"
            f"📥 *Total Downloads:* {sum(analytics.daily_downloads.values())}\n\n"
            "📈 *Popular Semesters:*\n"
        )
        
        # Top 5 downloaded
        top_downloads = sorted(analytics.daily_downloads.items(), key=lambda x: x[1], reverse=True)[:5]
        if top_downloads:
            for key, count in top_downloads:
                parts = key.split('_')
                if len(parts) == 2:
                    sem, branch = parts
                    stats_text += f"• {sem} - {BRANCH_EMOJIS.get(branch, branch)}: {count} downloads\n"
        else:
            stats_text += "• No downloads yet\n"
        
        stats_text += f"\n⏰ *Last Updated:* {datetime.now().strftime('%d %b %Y, %I:%M %p')}"
        
        bot.send_message(
            message.chat.id,
            stats_text,
            parse_mode='Markdown',
            reply_markup=MenuBuilder.main_menu()
        )
    except Exception as e:
        logger.error(f"Error in show_stats: {e}")

@bot.message_handler(func=lambda m: m.text == "ℹ️ Help")
def help_command(message):
    try:
        help_text = (
            "ℹ️ *Help & Guide* ℹ️\n\n"
            "📚 *How to get Syllabus:*\n"
            "1. Click '📚 Syllabus'\n"
            "2. Select your branch\n"
            "3. Choose your semester\n"
            "4. Download PDF\n\n"
            "📊 *Stats:* View bot usage statistics\n"
            "🔄 *Reset:* Clear your current selection\n\n"
            "❓ *Common Issues:*\n"
            "• Make sure you've joined our channel\n"
            "• Check your internet connection\n"
            "• If PDF doesn't download, try again\n\n"
            "📢 *Contact:* @EngineersPathwayOfficial"
        )
        bot.send_message(
            message.chat.id,
            help_text,
            parse_mode='Markdown',
            reply_markup=MenuBuilder.main_menu()
        )
    except Exception as e:
        logger.error(f"Error in help_command: {e}")

@bot.message_handler(func=lambda m: m.text == "⭐ Feedback")
def feedback_command(message):
    try:
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("📝 Send Feedback", url=f"https://t.me/EngineersPathwayOfficial"),
            InlineKeyboardButton("⭐ Rate Us", url="https://t.me/EngineersPathwayOfficial")
        )
        bot.send_message(
            message.chat.id,
            "⭐ *We value your feedback!* ⭐\n\n"
            "Share your experience or suggestions with us.\n"
            "Click below to send feedback or rate our bot:",
            reply_markup=markup,
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Error in feedback_command: {e}")

@bot.message_handler(func=lambda m: m.text == "🔄 Reset")
def reset_command(message):
    try:
        user_session.clear(message.chat.id)
        bot.send_message(
            message.chat.id,
            "✅ *Reset Successful!*\n\nYour session has been cleared.\nUse '📚 Syllabus' to start fresh.",
            parse_mode='Markdown',
            reply_markup=MenuBuilder.main_menu()
        )
    except Exception as e:
        logger.error(f"Error in reset_command: {e}")

@bot.message_handler(func=lambda m: m.text == "🏠 Main Menu")
def main_menu_command(message):
    try:
        user_session.clear(message.chat.id)
        bot.send_message(
            message.chat.id,
            "🏠 *Main Menu*\n\nChoose an option below:",
            reply_markup=MenuBuilder.main_menu(),
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Error in main_menu_command: {e}")

@bot.message_handler(func=lambda m: m.text == "🔙 Back to Branches")
def back_to_branches(message):
    try:
        user_session.set(message.chat.id, "step", "waiting_for_branch")
        branch_text = "🏗️ *पहले अपनी Branch चुनें:*\n\n"
        for branch, emoji_name in BRANCH_EMOJIS.items():
            branch_text += f"• {emoji_name}\n"
        
        bot.send_message(
            message.chat.id,
            branch_text,
            reply_markup=MenuBuilder.branch_first_menu(),
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Error in back_to_branches: {e}")

# ================== FLASK WEBHOOK SERVER FOR RENDER ==================
app = Flask(__name__)

@app.route(f'/webhook/{TOKEN}', methods=['POST'])
def webhook():
    """Handle Telegram webhook requests"""
    if request.headers.get('content-type') == 'application/json':
        try:
            json_string = request.get_data().decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return 'OK', 200
        except Exception as e:
            logger.error(f"Webhook error: {e}")
            return 'Error', 500
    return 'Bad Request', 400

@app.route('/')
def health_check():
    """Health check endpoint for Render"""
    return {
        'status': 'running',
        'bot': 'BEU Syllabus Bot',
        'timestamp': datetime.now().isoformat()
    }, 200

@app.route('/health')
def health():
    """Alternative health check"""
    return 'OK', 200

def setup_webhook():
    """Setup webhook for the bot"""
    try:
        bot.remove_webhook()
        time.sleep(1)
        
        # Get Render's external hostname
        render_hostname = os.getenv('RENDER_EXTERNAL_HOSTNAME')
        if not render_hostname:
            logger.error("RENDER_EXTERNAL_HOSTNAME not set")
            return False
        
        webhook_url = f"https://{render_hostname}/webhook/{TOKEN}"
        bot.set_webhook(url=webhook_url)
        logger.info(f"✅ Webhook set successfully to {webhook_url}")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to set webhook: {e}")
        return False

# ================== MAIN ENTRY POINT ==================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    # Check if running on Render
    if os.getenv('RENDER'):
        logger.info("🚀 Starting bot on Render with webhook...")
        
        # Setup webhook
        if setup_webhook():
            # Start Flask server
            app.run(host='0.0.0.0', port=port, debug=False)
        else:
            logger.error("Webhook setup failed, falling back to polling...")
            # Fallback to polling if webhook fails
            bot.infinity_polling(timeout=10)
    else:
        # Local development - use long polling
        logger.info("🖥️ Starting bot locally with polling...")
        bot.infinity_polling(timeout=10, long_polling_timeout=5)