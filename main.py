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
        # DATA_DIR set ho to us folder me save hoga, warna bot file ke same folder me
        # Note: Railway/Render par Total Users preserve karne ke liye persistent volume zaroori hai.
        data_dir = os.getenv("DATA_DIR")
        if data_dir:
            Path(data_dir).mkdir(parents=True, exist_ok=True)
            self.filename = str(Path(data_dir) / filename)
        else:
            self.filename = str(BASE_DIR / filename)

        self.total_users: Set[int] = set()
        self.daily_active: Set[int] = set()
        self.command_stats: Dict[str, int] = {}
        self.daily_downloads: Dict[str, int] = {}
        self.last_reset = str(date.today())
        self.lock = threading.Lock()
        self.load()
    
    def load(self):
        try:
            if not os.path.exists(self.filename):
                logger.info("Analytics file not found. Creating new analytics file.")
                self.save()
                return

            with open(self.filename, 'r', encoding='utf-8') as f:
                content = f.read().strip()

            if not content:
                logger.warning("Analytics file is empty. Not overwriting to prevent Total Users reset.")
                return

            data = json.loads(content)

            with self.lock:
                self.total_users = set(map(int, data.get('total_users', [])))
                self.daily_active = set(map(int, data.get('daily_active', [])))
                self.command_stats = data.get('command_stats', {})
                self.daily_downloads = data.get('daily_downloads', {})
                self.last_reset = data.get('last_reset', str(date.today()))

            logger.info(f"Analytics loaded successfully. Total users: {len(self.total_users)}")

        except Exception as e:
            logger.error(f"Error loading analytics: {e}")
            logger.error("Analytics file NOT overwritten, so Total Users will not reset due to load error.")
    
    def save(self):
        try:
            with self.lock:
                data = {
                    'total_users': sorted(list(map(int, self.total_users))),
                    'daily_active': sorted(list(map(int, self.daily_active))),
                    'command_stats': self.command_stats,
                    'daily_downloads': self.daily_downloads,
                    'last_reset': self.last_reset
                }

            temp_file = self.filename + '.tmp'
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)

            os.replace(temp_file, self.filename)

        except Exception as e:
            logger.error(f"Error saving analytics: {e}")
    
    def track_user(self, user_id: int, command: str = "start"):
        try:
            user_id = int(user_id)
            with self.lock:
                self.total_users.add(user_id)
                self.daily_active.add(user_id)
                self.command_stats[command] = self.command_stats.get(command, 0) + 1
            self.save()
        except Exception as e:
            logger.error(f"Error tracking user: {e}")
    
    def track_download(self, semester: str, branch: str):
        try:
            key = f"{semester}_{branch}"
            with self.lock:
                self.daily_downloads[key] = self.daily_downloads.get(key, 0) + 1
            self.save()
        except Exception as e:
            logger.error(f"Error tracking download: {e}")
    
    def reset_daily(self):
        try:
            with self.lock:
                # Total Users ko touch nahi karega
                self.daily_active.clear()
                self.daily_downloads.clear()
                self.last_reset = str(date.today())
            self.save()
            logger.info(f"Daily analytics reset completed. Total users preserved: {len(self.total_users)}")
        except Exception as e:
            logger.error(f"Error resetting daily analytics: {e}")

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
                f"📊 Downloads Today: {analytics.daily_downloads.get(f'{semester}_{branch}', 0)}",
                reply_markup=markup,
                parse_mode='Markdown'
            )
            
    except Exception as e:
        logger.error(f"Error in semester_after_branch: {e}")
        bot.send_message(message.chat.id, "⚠️ Error! Please try again.")

@bot.message_handler(func=lambda m: m.text == "🔙 Back to Branches")
def back_to_branches(message):
    try:
        if not is_member(message.chat.id):
            send_join_required(message)
            return
        
        user_session.set(message.chat.id, "selected_branch", None)
        user_session.set(message.chat.id, "step", "waiting_for_branch")
        
        branch_text = "🏗️ *अपनी Branch चुनें:*\n\n"
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

@bot.message_handler(func=lambda m: m.text == "🏠 Main Menu")
def back_to_main_menu(message):
    try:
        if not is_member(message.chat.id):
            send_join_required(message)
            return
        
        user_session.clear(message.chat.id)
        start(message)
    except Exception as e:
        logger.error(f"Error in back_to_main_menu: {e}")

@bot.message_handler(func=lambda m: m.text == "📊 Stats")
def show_stats(message):
    try:
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
                parts = sem_branch.split('_')
                if len(parts) == 2:
                    sem, branch = parts
                    stats_text += f"• {sem} - {branch}: {count}\n"
        else:
            stats_text += "• No downloads yet\n"
        
        stats_text += f"\n🕐 Last updated: {datetime.now().strftime('%H:%M:%S')}"
        
        bot.send_message(message.chat.id, stats_text, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Error in show_stats: {e}")

@bot.message_handler(func=lambda m: m.text == "ℹ️ Help")
def show_help(message):
    try:
        help_text = (
            "📚 *Help & Guide*\n\n"
            "*How to use:*\n"
            "1. Tap '📚 Syllabus'\n"
            "2. Choose your branch\n"
            "3. Select your semester\n"
            "4. Download or share PDF\n\n"
            
            "*Features:*\n"
            "• ⬇️ Download PDF - Save syllabus to device\n"
            "• 📤 Share - Share syllabus with friends\n\n"
            
            "*Commands:*\n"
            "/start - Restart bot\n"
            "/menu - Show main menu\n"
            
            "*Need Support?*\n"
            "Join our Telegram channel for updates!\n\n"
            
            "📢 *Channel:* @EngineersPathwayOfficial\n"
            "▶️ *YouTube:* Engineers Pathway Official\n"
            "👨‍💻 *Developer Contact:* [Click Here](https://www.linkedin.com/in/mdzafar864)"
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
    except Exception as e:
        logger.error(f"Error in show_help: {e}")

@bot.message_handler(func=lambda m: m.text == "⭐ Feedback")
def get_feedback(message):
    try:
        if not is_member(message.chat.id):
            send_join_required(message)
            return
        
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
    except Exception as e:
        logger.error(f"Error in get_feedback: {e}")

def process_feedback(message):
    try:
        feedback_content = message.text
        
        first_name = message.from_user.first_name or "N/A"
        last_name = message.from_user.last_name or "N/A"
        username = message.from_user.username or "N/A"
        user_id = message.from_user.id
        
        feedback_msg = (
            f"📝 *New Feedback Received!*\n\n"
            f"👤 *User Information:*\n"
            f"├ First Name: `{first_name}`\n"
            f"├ Last Name: `{last_name}`\n"
            f"├ Username: @{username}\n"
            f"└ User ID: `{user_id}`\n\n"
            f"💬 *Feedback Message:*\n"
            f"└ {feedback_content}\n\n"
            f"🕐 *Time:* {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        )
        
        bot.send_message(ADMIN_ID, feedback_msg, parse_mode='Markdown')
        
        bot.send_message(
            message.chat.id,
            "✅ *Thank you for your feedback!*\n\n"
            "Your message has been sent to the admin.\n\n"
            "🙏 Thanks for helping us improve!",
            reply_markup=MenuBuilder.main_menu(),
            parse_mode='Markdown'
        )
        
        logger.info(f"Feedback sent from user {user_id} (@{username})")
        
    except Exception as e:
        logger.error(f"Error in process_feedback: {e}")
        bot.send_message(
            message.chat.id,
            "⚠️ *Sorry!*\n\n"
            "There was an issue sending your feedback. Please try again later.",
            reply_markup=MenuBuilder.main_menu(),
            parse_mode='Markdown'
        )

@bot.message_handler(func=lambda m: m.text == "🔄 Reset")
def reset_session(message):
    try:
        if not is_member(message.chat.id):
            send_join_required(message)
            return
        
        user_session.clear(message.chat.id)
        bot.send_message(
            message.chat.id,
            "🔄 Session reset! You can start fresh now.",
            reply_markup=MenuBuilder.main_menu()
        )
    except Exception as e:
        logger.error(f"Error in reset_session: {e}")

@bot.message_handler(func=lambda m: True)
def handle_unknown(message):
    try:
        if not is_member(message.chat.id):
            send_join_required(message)
            return
        
        bot.send_message(
            message.chat.id,
            "❓ *Unknown Command*\n\n"
            "Please use the menu buttons below or type /start to restart.",
            reply_markup=MenuBuilder.main_menu(),
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Error in handle_unknown: {e}")

# ================== ADMIN COMMANDS ==================
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    try:
        if message.from_user.id != ADMIN_ID:
            bot.send_message(message.chat.id, "⛔ Unauthorized access!")
            return
        
        admin_text = (
            "👑 *Admin Panel*\n\n"
            f"📊 *Total Users:* {len(analytics.total_users)}\n"
            f"📅 *Active Today:* {len(analytics.daily_active)}\n"
            f"📚 *Total Downloads:* {sum(analytics.daily_downloads.values())}\n\n"
            "📈 *Top Downloads:*\n"
        )
        
        top_downloads = sorted(analytics.daily_downloads.items(), key=lambda x: x[1], reverse=True)[:10]
        for sem_branch, count in top_downloads:
            admin_text += f"• {sem_branch}: {count}\n"
        
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("📊 Full Stats", callback_data="full_stats"),
            InlineKeyboardButton("💾 Save Data", callback_data="save_data")
        )
        
        bot.send_message(message.chat.id, admin_text, parse_mode='Markdown', reply_markup=markup)
    except Exception as e:
        logger.error(f"Error in admin_panel: {e}")

@bot.callback_query_handler(func=lambda call: call.data in ["full_stats", "save_data"])
def admin_callbacks(call):
    try:
        if call.from_user.id != ADMIN_ID:
            bot.answer_callback_query(call.id, "⛔ Unauthorized!", show_alert=True)
            return
        
        if call.data == "full_stats":
            stats_file = analytics.filename
            if os.path.exists(stats_file):
                with open(stats_file, 'rb') as f:
                    bot.send_document(call.message.chat.id, f, caption="📊 Full analytics data")
            else:
                bot.send_message(call.message.chat.id, "No analytics data found!")
        
        elif call.data == "save_data":
            analytics.save()
            bot.answer_callback_query(call.id, "✅ Data saved successfully!")
    except Exception as e:
        logger.error(f"Error in admin_callbacks: {e}")

@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    try:
        if message.from_user.id != ADMIN_ID:
            bot.send_message(message.chat.id, "⛔ Unauthorized access!")
            return
        
        msg = message.text.replace('/broadcast', '').strip()
        if not msg:
            bot.send_message(message.chat.id, "⚠️ Usage: /broadcast <message>")
            return
        
        success = 0
        failed = 0
        
        status_msg = bot.send_message(message.chat.id, "📤 Sending broadcast...")
        
        for user_id in list(analytics.total_users):
            try:
                bot.send_message(user_id, f"📢 *Announcement*\n\n{msg}", parse_mode='Markdown')
                success += 1
            except:
                failed += 1
            time.sleep(0.1)
        
        bot.edit_message_text(
            f"✅ Broadcast completed!\n\n"
            f"✓ Success: {success}\n"
            f"✗ Failed: {failed}",
            message.chat.id,
            status_msg.message_id
        )
    except Exception as e:
        logger.error(f"Error in broadcast_message: {e}")

@bot.message_handler(commands=['stats'])
def user_stats(message):
    try:
        if message.from_user.id != ADMIN_ID:
            bot.send_message(message.chat.id, "⛔ Unauthorized access!")
            return
        
        stats_text = (
            "📊 *Detailed Statistics*\n\n"
            f"👥 *Total Users:* {len(analytics.total_users)}\n"
            f"📅 *Active Today:* {len(analytics.daily_active)}\n"
            f"📚 *Total Downloads:* {sum(analytics.daily_downloads.values())}\n\n"
            f"📈 *Command Usage:*\n"
        )
        
        for cmd, count in sorted(analytics.command_stats.items(), key=lambda x: x[1], reverse=True)[:10]:
            stats_text += f"• /{cmd}: {count}\n"
        
        bot.send_message(message.chat.id, stats_text, parse_mode='Markdown')
    except Exception as e:
        logger.error(f"Error in user_stats: {e}")

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

# ================== HEALTH CHECK FOR RAILWAY ==================
try:
    from flask import Flask, jsonify
    flask_app = Flask(__name__)
    
    @flask_app.route('/')
    def health():
        return "✅ BEU Syllabus Bot is running!", 200
    
    @flask_app.route('/health')
    def health_check():
        return jsonify({
            "status": "healthy",
            "users": len(analytics.total_users),
            "downloads": sum(analytics.daily_downloads.values())
        }), 200
    
    def run_web():
        port = int(os.environ.get('PORT', 8080))
        flask_app.run(host='0.0.0.0', port=port, debug=False)
    
    web_thread = threading.Thread(target=run_web, daemon=True)
    web_thread.start()
    logger.info("✅ Health check server started")
except ImportError:
    logger.warning("⚠️ Flask not installed. Install with: pip install flask")

# ================== AUTO RESTART ON ERROR ==================
def run_bot():
    while True:
        try:
            logger.info("🚀 Starting bot...")
            bot.infinity_polling(timeout=30, long_polling_timeout=30)
        except Exception as e:
            logger.error(f"Bot crashed: {e}")
            logger.info("Restarting bot in 10 seconds...")
            time.sleep(10)

# ================== BOT STARTUP ==================
if __name__ == "__main__":
    logger.info("🚀 BEU Syllabus Bot Starting on Railway!")
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
    logger.info(f"👑 Admin ID: {ADMIN_ID}")
    
    # Start daily reset thread
    try:
        reset_thread = threading.Thread(target=daily_reset, daemon=True)
        reset_thread.start()
        logger.info("✅ Daily reset scheduler started")
    except Exception as e:
        logger.warning(f"⚠️ Daily reset scheduler not started: {e}")
    
    # Start bot with auto-restart
    run_bot()
