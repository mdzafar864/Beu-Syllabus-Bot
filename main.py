import telebot
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import os
import json
from datetime import datetime
import logging

# ================== LOGGING ==================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ================== TOKEN ==================
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# ================== FORCE JOIN SETTINGS ==================
CHANNEL_USERNAME = "@EngineersPathwayOfficial"
YOUTUBE_LINK = "https://youtube.com/@engineerspathwayofficial"

def check_membership(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print("Join Check Error:", e)
        return False

def send_force_join(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📢 Join Telegram", url="https://t.me/EngineersPathwayOfficial"))
    markup.add(InlineKeyboardButton("▶️ Subscribe YouTube", url=YOUTUBE_LINK))
    markup.add(InlineKeyboardButton("✅ I Joined", callback_data="check_join"))

    bot.send_message(
        message.chat.id,
        "🚫 *Access Denied!*\n\n"
        "🔥 Free Syllabus + Notes + Updates\n\n"
        "1️⃣ Telegram channel join karo\n"
        "2️⃣ YouTube subscribe karo\n\n"
        "👇 Join karke 'I Joined' dabao",
        reply_markup=markup,
        parse_mode='Markdown'
    )

@bot.callback_query_handler(func=lambda call: call.data == "check_join")
def check_join_callback(call):
    if check_membership(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ Verified!")
        start(call.message)
    else:
        bot.answer_callback_query(call.id, "❌ Pehle join karo!", show_alert=True)

# ================== USER DATA ==================
user_data = {}

user_analytics = {
    "total_users": set(),
    "daily_users": set(),
    "commands_used": {}
}

ANALYTICS_FILE = "user_analytics.json"

def load_analytics():
    global user_analytics
    try:
        with open(ANALYTICS_FILE, 'r') as f:
            loaded = json.load(f)
            loaded["total_users"] = set(loaded.get("total_users", []))
            loaded["daily_users"] = set(loaded.get("daily_users", []))
            user_analytics = loaded
    except:
        save_analytics()

def save_analytics():
    to_save = {
        "total_users": list(user_analytics["total_users"]),
        "daily_users": list(user_analytics["daily_users"]),
        "commands_used": user_analytics["commands_used"]
    }
    with open(ANALYTICS_FILE, 'w') as f:
        json.dump(to_save, f)

def track_user(user_id, command="start"):
    user_analytics["total_users"].add(user_id)
    user_analytics["daily_users"].add(user_id)
    user_analytics["commands_used"][command] = user_analytics["commands_used"].get(command, 0) + 1
    save_analytics()

load_analytics()

# ================== SYLLABUS ==================
# ===== SYLLABUS DATABASE WITH WORKING LINKS =====
syllabus = {
    "1stNew": {
        "CE": "https://drive.google.com/uc?export=download&id=1Qd3X732fBWyEax1GTudkBWn7fpe57CgA",
        "CS": "https://drive.google.com/uc?export=download&id=1Zp-UAEgj72UstczPS_wSIBtlPU48USal",
        "EE": "https://drive.google.com/uc?export=download&id=1dZCtmM7w3H9dRpsWMlDhhJZNvFOiA1up",
        "ECE": "https://drive.google.com/uc?export=download&id=14cLD5aiYQp_2U3qKN16pa7U4fowBMg3J",
        "ME": "https://drive.google.com/uc?export=download&id=1yYB-UOYnpkOCYspJeZv83o7Rjy3wfcB8"
    },
    "1stOld": {
        "CE": "https://drive.google.com/uc?export=download&id=1iRWghHRyCP6WPZ3Xoc0DdScIytir3xRn",
        "CS": "https://drive.google.com/uc?export=download&id=1EHpLPUo0_7086gFmk2WRZv2fMw93Jcdb",
        "EE": "https://drive.google.com/uc?export=download&id=1BtS61CEIOidszDe5FLBVQUake_8RQZlK",
        "ECE": "https://drive.google.com/uc?export=download&id=1t57gqcXtYajz6p5q6FXtcBVPb-mUgX1m",
        "ME": "https://drive.google.com/uc?export=download&id=1gyWaJKhhcZNmSF9WlWfqRXfnTeA87hvY"
    },
    "2ndNew": {
        "CE": "https://drive.google.com/uc?export=download&id=13q_AFXP9e2AWyHHtHWp_Fm4bRgtME3qv",
        "CS": "https://drive.google.com/uc?export=download&id=15Y2Vsq8xe3Cl2Sc4BcXtL4XQMsqwKIFh",
        "EE": "https://drive.google.com/uc?export=download&id=1wgmEj8RSBWleYUZ1JjzD7tICuiQgJEDW",
        "ECE": "https://drive.google.com/uc?export=download&id=1THqchJygHP7BVVQjj-kf4YmMHBrjfA_x",
        "ME": "https://drive.google.com/uc?export=download&id=1hhAgOvC2LvbBRv6f7n1MSHPxD9MBVgsy"
    },
    "2ndOld": {
        "CE": "https://drive.google.com/uc?export=download&id=1jW97lTtufHT26vkRP6KISUiKWSYe6F3o",
        "CS": "https://drive.google.com/uc?export=download&id=16JynS8hA5JtsSlIc3-HBUPqI9o1F2ziN",
        "EE": "https://drive.google.com/uc?export=download&id=1CrAHd-0bwzESjiLtb-AQwOeKtopyiJm9",
        "ECE": "https://drive.google.com/uc?export=download&id=1eJQJy3I853QoqfNzOT5XFUgncJKxbnv6",
        "ME": "https://drive.google.com/uc?export=download&id=1xwhvlJIQJRCqKLCPTKeOOdjzkUgr8S5U"
    },
    "3rdNew": {
        "CE": "https://drive.google.com/uc?export=download&id=1GzMwwCkUrHPmc5fgyWOxOSsPof9dQZO8",
        "CS": "https://drive.google.com/uc?export=download&id=18tjQnI2qGtbSzRWEp08KqKY4gDvE25em",
        "IOT": "https://drive.google.com/uc?export=download&id=1DyoqlnntdtG-RA0ET1wH4FrR-DOB3mtF",
        "EE": "https://drive.google.com/uc?export=download&id=1nKpL1rXXa7EGJqbvDkmEem1uh74QWjOU",
        "ECE": "https://drive.google.com/uc?export=download&id=1kWy1_zhggLM9U4jrkTzGWNdLcE-4QXMr",
        "ME": "https://drive.google.com/uc?export=download&id=14yS8pyf83vIA1vs-_DbAvWbYpF8y6gc9"
    },
    "3rdOld": {
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

# ================== MENU ==================
def get_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📚 Syllabus")
    markup.add("📈 Statistics", "ℹ️ Help", "⭐ Feedback")
    return markup

# ================== START ==================
@bot.message_handler(commands=['start'])
def start(message):
    if not check_membership(message.chat.id):
        send_force_join(message)
        return

    track_user(message.chat.id, "start")

    bot.send_message(
        message.chat.id,
        "🎓 *Welcome to BEU Syllabus Bot* 🎓",
        reply_markup=get_main_menu(),
        parse_mode='Markdown'
    )

# ================== SYLLABUS MENU ==================
@bot.message_handler(func=lambda m: m.text == "📚 Syllabus")
def syllabus_menu(message):
    if not check_membership(message.chat.id):
        send_force_join(message)
        return

    track_user(message.chat.id, "syllabus")

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for sem in syllabus.keys():
        markup.add(sem)
    markup.add("🔙 Main Menu")

    bot.send_message(message.chat.id, "Select Semester:", reply_markup=markup)

# ================== SEM ==================
@bot.message_handler(func=lambda m: m.text in syllabus.keys())
def sem_select(message):
    if not check_membership(message.chat.id):
        send_force_join(message)
        return

    user_data[message.chat.id] = message.text

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for branch in syllabus[message.text].keys():
        markup.add(branch)
    markup.add("🔙 Main Menu")

    bot.send_message(message.chat.id, "Select Branch:", reply_markup=markup)

# ================== PDF ==================
@bot.message_handler(func=lambda m: m.text in ["CE"])
def send_pdf(message):
    if not check_membership(message.chat.id):
        send_force_join(message)
        return

    sem = user_data.get(message.chat.id)

    if not sem:
        bot.send_message(message.chat.id, "❌ Pehle semester select karo")
        return

    file_url = syllabus[sem][message.text]

    bot.send_document(
        message.chat.id,
        file_url,
        caption=f"{sem} - {message.text} Syllabus"
    )

# ================== STATS ==================
@bot.message_handler(func=lambda m: m.text == "📈 Statistics")
def stats(message):
    if not check_membership(message.chat.id):
        send_force_join(message)
        return

    bot.send_message(
        message.chat.id,
        f"👥 Total Users: {len(user_analytics['total_users'])}\n"
        f"📅 Today Users: {len(user_analytics['daily_users'])}"
    )

# ================== HELP ==================
@bot.message_handler(func=lambda m: m.text == "ℹ️ Help")
def help_msg(message):
    if not check_membership(message.chat.id):
        send_force_join(message)
        return

    bot.send_message(message.chat.id, "Use 📚 Syllabus")

# ================== FEEDBACK ==================
@bot.message_handler(func=lambda m: m.text == "⭐ Feedback")
def feedback(message):
    if not check_membership(message.chat.id):
        send_force_join(message)
        return

    bot.send_message(message.chat.id, "Send your feedback")

# ================== BACK ==================
@bot.message_handler(func=lambda m: m.text == "🔙 Main Menu")
def back(message):
    start(message)

# ================== DEFAULT ==================
@bot.message_handler(func=lambda m: True)
def default(message):
    bot.send_message(message.chat.id, "Use menu buttons")

# ================== RUN ==================
print("🚀 Bot Running...")
bot.infinity_polling()
