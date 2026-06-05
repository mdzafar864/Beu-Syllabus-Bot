import telebot
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import os
import json
from datetime import datetime, date
import logging
from typing import Dict, Set, Optional
import threading
from pathlib import Path
import time

# ================== CONFIGURATION ==================
BASE_DIR = Path(__file__).parent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(BASE_DIR / "bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "@EngineersPathwayOfficial"
YOUTUBE_LINK = "https://youtube.com/@engineerspathwayofficial"
DEVELOPER_LINK = "https://www.linkedin.com/in/mdzafar864"
ADMIN_ID = 5861904079

if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable not found. Please set BOT_TOKEN first.")

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
bot = telebot.TeleBot(TOKEN, parse_mode=None)

# ================== HELPER FUNCTIONS ==================
def get_download_link(drive_url: str) -> str:
    try:
        if "id=" in drive_url:
            file_id = drive_url.split("id=")[-1].split("&")[0]
        elif "/d/" in drive_url:
            file_id = drive_url.split("/d/")[1].split("/")[0]
        else:
            return drive_url

        return f"https://drive.google.com/uc?export=download&id={file_id}"
    except Exception:
        return drive_url


def html_link(url: str, text: str = "Click Here") -> str:
    return f"<a href='{url}'>{text}</a>"


# ================== USER SESSION ==================
class UserSession:
    def __init__(self):
        self.data: Dict[int, Dict] = {}
        self.lock = threading.Lock()

    def get(self, user_id: int) -> Optional[Dict]:
        with self.lock:
            return self.data.get(int(user_id))

    def set(self, user_id: int, key: str, value):
        with self.lock:
            user_id = int(user_id)
            if user_id not in self.data:
                self.data[user_id] = {}
            self.data[user_id][key] = value

    def clear(self, user_id: int):
        with self.lock:
            user_id = int(user_id)
            if user_id in self.data:
                del self.data[user_id]


user_session = UserSession()

# ================== ANALYTICS SYSTEM - TOTAL USERS RESET FIXED ==================
class Analytics:
    def __init__(self, filename: str = "analytics.json"):
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
                logger.info("Analytics file not found. Creating new file.")
                self.save()
                return

            with open(self.filename, "r", encoding="utf-8") as f:
                content = f.read().strip()

            if not content:
                logger.warning("Analytics file is empty. Not overwriting old data in memory.")
                self.save()
                return

            data = json.loads(content)

            with self.lock:
                self.total_users = set(map(int, data.get("total_users", [])))
                self.daily_active = set(map(int, data.get("daily_active", [])))
                self.command_stats = data.get("command_stats", {})
                self.daily_downloads = data.get("daily_downloads", {})
                self.last_reset = data.get("last_reset", str(date.today()))

            logger.info(f"Analytics loaded successfully. Total users: {len(self.total_users)}")

        except Exception as e:
            logger.error(f"Error loading analytics: {e}")
            logger.error("Analytics file not overwritten to prevent total users reset.")

    def save(self):
        try:
            with self.lock:
                data = {
                    "total_users": sorted(list(self.total_users)),
                    "daily_active": sorted(list(self.daily_active)),
                    "command_stats": self.command_stats,
                    "daily_downloads": self.daily_downloads,
                    "last_reset": self.last_reset
                }

            temp_file = self.filename + ".tmp"

            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            os.replace(temp_file, self.filename)

        except Exception as e:
            logger.error(f"Error saving analytics: {e}")

    def auto_reset_daily_if_needed(self):
        try:
            today = str(date.today())

            with self.lock:
                if self.last_reset == today:
                    return

                self.daily_active.clear()
                self.daily_downloads.clear()
                self.last_reset = today

            self.save()
            logger.info("Auto daily reset completed. Total users preserved.")

        except Exception as e:
            logger.error(f"Error in auto daily reset: {e}")

    def track_user(self, user_id: int, command: str = "start"):
        try:
            self.auto_reset_daily_if_needed()
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
            self.auto_reset_daily_if_needed()
            key = f"{semester}_{branch}"

            with self.lock:
                self.daily_downloads[key] = self.daily_downloads.get(key, 0) + 1

            self.save()

        except Exception as e:
            logger.error(f"Error tracking download: {e}")

    def reset_daily(self):
        try:
            with self.lock:
                self.daily_active.clear()
                self.daily_downloads.clear()
                self.last_reset = str(date.today())

            self.save()
            logger.info("Daily analytics reset completed. Total users preserved.")

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
        buttons = list(BRANCH_EMOJIS.values())
        markup.add(*buttons)
        markup.add("🏠 Main Menu")
        return markup

    @staticmethod
    def semester_for_branch_menu(available_semesters: list) -> ReplyKeyboardMarkup:
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
        member = bot.get_chat_member(CHANNEL_USERNAME, int(user_id))
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        logger.error(f"Membership check failed for {user_id}: {e}")
        return False


def send_join_required(message):
    try:
        bot.send_message(
            message.chat.id,
            "🔒 <b>Access Restricted</b>\n\n"
            "To access the syllabus and all features, you must join our community:\n\n"
            "✅ Join Telegram Channel\n"
            "✅ Subscribe to YouTube\n\n"
            "After joining, click the button below to verify access.",
            reply_markup=MenuBuilder.force_join_markup(),
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Error sending join required message: {e}")


# ================== CALLBACK HANDLER ==================
@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def verify_join(call):
    try:
        if is_member(call.from_user.id):
            bot.answer_callback_query(call.id, "✅ Access Granted! Welcome aboard!")
            analytics.track_user(call.from_user.id, "verified")

            bot.send_message(
                call.message.chat.id,
                "🎉 <b>Access Verified!</b>\n\n"
                "Welcome to BEU Syllabus Bot!\n"
                "Use the menu below to get started.",
                reply_markup=MenuBuilder.main_menu(),
                parse_mode="HTML"
            )
        else:
            bot.answer_callback_query(
                call.id,
                "❌ Please join Telegram channel first!",
                show_alert=True
            )

    except Exception as e:
        logger.error(f"Error in verify_join: {e}")


# ================== START / MENU ==================
@bot.message_handler(commands=["start", "menu"])
def start(message):
    try:
        if not is_member(message.chat.id):
            send_join_required(message)
            return

        analytics.track_user(message.chat.id, "start")
        user_session.clear(message.chat.id)

        welcome_text = (
            "🎓 <b>BEU Syllabus Bot</b> 🎓\n\n"
            "📚 <b>Available Features:</b>\n"
            "• Download semester-wise syllabus\n"
            "• Branch-wise syllabus access\n"
            "• Share syllabus with friends\n\n"
            "💡 <b>How to use:</b>\n"
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
            parse_mode="HTML"
        )

    except Exception as e:
        logger.error(f"Error in start: {e}")
        bot.send_message(message.chat.id, "⚠️ Something went wrong. Please try /start")


@bot.message_handler(func=lambda m: m.text == "🏠 Main Menu")
def main_menu_button(message):
    start(message)


# ================== SYLLABUS FLOW ==================
@bot.message_handler(func=lambda m: m.text == "📚 Syllabus")
def show_branches_first(message):
    try:
        if not is_member(message.chat.id):
            send_join_required(message)
            return

        analytics.track_user(message.chat.id, "syllabus")
        user_session.set(message.chat.id, "step", "waiting_for_branch")

        branch_text = "🏗️ <b>पहले अपनी Branch चुनें:</b>\n\n"

        for emoji_name in BRANCH_EMOJIS.values():
            branch_text += f"• {emoji_name}\n"

        branch_text += "\n💡 Branch चुनने के बाद Semester select करेंगे"

        bot.send_message(
            message.chat.id,
            branch_text,
            reply_markup=MenuBuilder.branch_first_menu(),
            parse_mode="HTML"
        )

    except Exception as e:
        logger.error(f"Error in show_branches_first: {e}")
        bot.send_message(message.chat.id, "⚠️ Error. Please try again.")


@bot.message_handler(func=lambda m: m.text == "🔙 Back to Branches")
def back_to_branches(message):
    show_branches_first(message)


@bot.message_handler(func=lambda m: m.text in list(BRANCH_EMOJIS.values()))
def branch_selected_first(message):
    try:
        if not is_member(message.chat.id):
            send_join_required(message)
            return

        selected_branch = None

        for branch_code, branch_name in BRANCH_EMOJIS.items():
            if branch_name == message.text:
                selected_branch = branch_code
                break

        if not selected_branch:
            bot.send_message(message.chat.id, "❌ Invalid branch!")
            return

        user_session.set(message.chat.id, "selected_branch", selected_branch)
        user_session.set(message.chat.id, "step", "waiting_for_semester")

        available_semesters = []

        for sem, branches in SYLLABUS.items():
            if selected_branch in branches:
                available_semesters.append(sem)

        if not available_semesters:
            bot.send_message(
                message.chat.id,
                f"❌ {BRANCH_EMOJIS.get(selected_branch, selected_branch)} branch का syllabus उपलब्ध नहीं है।"
            )
            return

        sem_text = f"📚 <b>{BRANCH_EMOJIS.get(selected_branch, selected_branch)} Branch</b>\n\n"
        sem_text += "अब अपना <b>Semester</b> चुनें:\n\n"

        for i, sem in enumerate(available_semesters, 1):
            sem_text += f"{i}. {sem}\n"

        bot.send_message(
            message.chat.id,
            sem_text,
            reply_markup=MenuBuilder.semester_for_branch_menu(available_semesters),
            parse_mode="HTML"
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

        semester = message.text.replace("📖 ", "").strip()
        session = user_session.get(message.chat.id)

        if not session or not session.get("selected_branch"):
            bot.send_message(
                message.chat.id,
                "⚠️ पहले Branch चुनें!",
                reply_markup=MenuBuilder.branch_first_menu()
            )
            return

        branch = session["selected_branch"]

        if semester not in SYLLABUS or branch not in SYLLABUS[semester]:
            bot.send_message(
                message.chat.id,
                f"❌ {BRANCH_EMOJIS.get(branch, branch)} branch का {semester} semester का syllabus उपलब्ध नहीं है।"
            )
            return

        download_url = get_download_link(SYLLABUS[semester][branch])
        analytics.track_download(semester, branch)

        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("⬇️ Download PDF", url=download_url),
            InlineKeyboardButton("📤 Share Syllabus", switch_inline_query=f"{semester} {branch} Syllabus")
        )

        caption = (
            f"📚 <b>{semester} Semester - {BRANCH_EMOJIS.get(branch, branch)} Syllabus</b>\n\n"
            f"📅 <b>Requested:</b> {datetime.now().strftime('%d %b %Y, %I:%M %p')}\n"
            f"📊 <b>Downloads Today:</b> {analytics.daily_downloads.get(f'{semester}_{branch}', 0)}"
        )

        bot.send_chat_action(message.chat.id, "typing")

        try:
            bot.send_document(
                message.chat.id,
                download_url,
                caption=caption,
                reply_markup=markup,
                parse_mode="HTML"
            )

            logger.info(f"Syllabus sent: {semester} - {branch} to user {message.chat.id}")

        except Exception as doc_error:
            logger.error(f"Document send failed: {doc_error}")

            bot.send_message(
                message.chat.id,
                f"📚 <b>{semester} Semester - {BRANCH_EMOJIS.get(branch, branch)} Syllabus</b>\n\n"
                f"✅ Syllabus ready!\n\n"
                f"Click below to download PDF:",
                reply_markup=markup,
                parse_mode="HTML"
            )

    except Exception as e:
        logger.error(f"Error in semester_after_branch: {e}")
        bot.send_message(
            message.chat.id,
            "⚠️ Error while sending syllabus. Please try again.",
            reply_markup=MenuBuilder.main_menu()
        )


# ================== STATS ==================
@bot.message_handler(func=lambda m: m.text == "📊 Stats")
def show_stats(message):
    try:
        if not is_member(message.chat.id):
            send_join_required(message)
            return

        analytics.track_user(message.chat.id, "stats")

        total_downloads = sum(analytics.daily_downloads.values())

        stats_text = (
            "📊 <b>Bot Statistics</b>\n\n"
            f"👥 <b>Total Users:</b> {len(analytics.total_users)}\n"
            f"🟢 <b>Daily Active Users:</b> {len(analytics.daily_active)}\n"
            f"⬇️ <b>Downloads Today:</b> {total_downloads}\n\n"
            "🔥 <b>Popular Downloads Today:</b>\n"
        )

        if analytics.daily_downloads:
            sorted_downloads = sorted(
                analytics.daily_downloads.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]

            for key, count in sorted_downloads:
                stats_text += f"• {key.replace('_', ' - ')}: {count}\n"
        else:
            stats_text += "• No downloads yet today\n"

        if message.chat.id == ADMIN_ID:
            stats_text += "\n👑 <b>Admin Commands:</b>\n/admin - Full admin stats\n/resetdaily - Reset daily stats"

        bot.send_message(
            message.chat.id,
            stats_text,
            reply_markup=MenuBuilder.main_menu(),
            parse_mode="HTML"
        )

    except Exception as e:
        logger.error(f"Error in show_stats: {e}")
        bot.send_message(message.chat.id, "⚠️ Stats loading error. Please try again.")


# ================== HELP ==================
@bot.message_handler(func=lambda m: m.text == "ℹ️ Help")
def help_guide(message):
    try:
        if not is_member(message.chat.id):
            send_join_required(message)
            return

        analytics.track_user(message.chat.id, "help")

        help_text = (
            "📚 <b>Help & Guide</b>\n\n"
            "<b>How to use:</b>\n"
            "1. Tap '📚 Syllabus'\n"
            "2. Choose your branch\n"
            "3. Select your semester\n"
            "4. Download or share PDF\n\n"
            "<b>Features:</b>\n"
            "• ⬇️ Download PDF - Save syllabus to device\n"
            "• 📤 Share - Share syllabus with friends\n\n"
            "<b>Commands:</b>\n"
            "/start - Restart bot\n"
            "/menu - Show main menu\n\n"
            "<b>Need Support?</b>\n"
            "Join our Telegram channel for updates!\n\n"
            "📢 Channel: @EngineersPathwayOfficial\n"
            "▶️ YouTube: Engineers Pathway Official\n"
            f"👨‍💻 Developer Contact: {html_link(DEVELOPER_LINK)}"
        )

        bot.send_message(
            message.chat.id,
            help_text,
            reply_markup=MenuBuilder.main_menu(),
            parse_mode="HTML",
            disable_web_page_preview=True
        )

    except Exception as e:
        logger.error(f"Error in help_guide: {e}")
        bot.send_message(message.chat.id, "⚠️ Help loading error. Please try again.")


# ================== FEEDBACK ==================
@bot.message_handler(func=lambda m: m.text == "⭐ Feedback")
def feedback(message):
    try:
        if not is_member(message.chat.id):
            send_join_required(message)
            return

        analytics.track_user(message.chat.id, "feedback")

        feedback_text = (
            "⭐ <b>Feedback</b>\n\n"
            "Aap apna feedback Telegram channel par share kar sakte hain.\n\n"
            "📢 Channel: @EngineersPathwayOfficial\n"
            f"👨‍💻 Developer Contact: {html_link(DEVELOPER_LINK)}"
        )

        bot.send_message(
            message.chat.id,
            feedback_text,
            reply_markup=MenuBuilder.main_menu(),
            parse_mode="HTML",
            disable_web_page_preview=True
        )

    except Exception as e:
        logger.error(f"Error in feedback: {e}")
        bot.send_message(message.chat.id, "⚠️ Feedback loading error. Please try again.")


# ================== RESET ==================
@bot.message_handler(func=lambda m: m.text == "🔄 Reset")
def reset_user(message):
    try:
        user_session.clear(message.chat.id)

        bot.send_message(
            message.chat.id,
            "🔄 Reset completed!\n\nUse menu below to start again.",
            reply_markup=MenuBuilder.main_menu()
        )

    except Exception as e:
        logger.error(f"Error in reset_user: {e}")


# ================== ADMIN COMMANDS ==================
@bot.message_handler(commands=["admin"])
def admin_stats(message):
    try:
        if message.chat.id != ADMIN_ID:
            bot.send_message(message.chat.id, "❌ You are not authorized.")
            return

        stats = (
            "👑 <b>Admin Dashboard</b>\n\n"
            f"👥 Total Users: {len(analytics.total_users)}\n"
            f"🟢 Daily Active: {len(analytics.daily_active)}\n"
            f"⬇️ Downloads Today: {sum(analytics.daily_downloads.values())}\n\n"
            "<b>Command Stats:</b>\n"
        )

        if analytics.command_stats:
            for cmd, count in analytics.command_stats.items():
                stats += f"• {cmd}: {count}\n"
        else:
            stats += "No command stats yet.\n"

        stats += "\n<b>Daily Downloads:</b>\n"

        if analytics.daily_downloads:
            for key, count in analytics.daily_downloads.items():
                stats += f"• {key}: {count}\n"
        else:
            stats += "No downloads today.\n"

        bot.send_message(message.chat.id, stats, parse_mode="HTML")

    except Exception as e:
        logger.error(f"Error in admin_stats: {e}")


@bot.message_handler(commands=["resetdaily"])
def reset_daily_admin(message):
    try:
        if message.chat.id != ADMIN_ID:
            bot.send_message(message.chat.id, "❌ You are not authorized.")
            return

        analytics.reset_daily()
        bot.send_message(message.chat.id, "✅ Daily analytics reset successfully. Total users preserved.")

    except Exception as e:
        logger.error(f"Error in reset_daily_admin: {e}")


# ================== FALLBACK ==================
@bot.message_handler(func=lambda m: True)
def fallback(message):
    try:
        if not is_member(message.chat.id):
            send_join_required(message)
            return

        bot.send_message(
            message.chat.id,
            "⚠️ Please use the menu buttons below.",
            reply_markup=MenuBuilder.main_menu()
        )

    except Exception as e:
        logger.error(f"Error in fallback: {e}")


# ================== RUN BOT ==================
if __name__ == "__main__":
    logger.info("BEU Syllabus Bot is starting...")

    while True:
        try:
            bot.infinity_polling(
                timeout=60,
                long_polling_timeout=60,
                skip_pending=True
            )

        except Exception as e:
            logger.error(f"Bot polling error: {e}")
            logger.info("Restarting bot in 5 seconds...")
            time.sleep(5)
