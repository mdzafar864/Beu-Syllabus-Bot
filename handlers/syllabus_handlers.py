import logging
from datetime import datetime
from telebot import TeleBot
from data.syllabus import SYLLABUS
from data.constants import BRANCH_EMOJIS, MENU_BUTTONS
from utils.menu_builder import MenuBuilder
from utils.helpers import get_download_link, format_branch_text, format_semester_text
from utils.validators import check_join_required
from models.analytics import Analytics
from models.user_session import UserSession

logger = logging.getLogger(__name__)

def register_syllabus_handlers(bot: TeleBot, analytics: Analytics, user_session: UserSession):
    
    @bot.message_handler(func=lambda m: m.text == MENU_BUTTONS["SYLLABUS"])
    def show_branches_first(message):
        try:
            if check_join_required(bot, message):
                return
            
            user_session.set(message.chat.id, "step", "waiting_for_branch")
            bot.send_message(
                message.chat.id,
                format_branch_text(),
                reply_markup=MenuBuilder.branch_first_menu(),
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Error in show_branches_first: {e}")
    
    @bot.message_handler(func=lambda m: m.text in list(BRANCH_EMOJIS.values()))
    def branch_selected_first(message):
        try:
            if check_join_required(bot, message):
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
            
            bot.send_message(
                message.chat.id,
                format_semester_text(selected_branch, available_semesters),
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
    
    @bot.message_handler(func=lambda m: user_session.get(m.chat.id, {}).get("step") == "waiting_for_semester")
    def semester_after_branch(message):
        try:
            if check_join_required(bot, message):
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
            
            # Create download markup
            markup = MenuBuilder.download_markup(download_url, semester, branch)
            
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
    
    @bot.message_handler(func=lambda m: m.text == MENU_BUTTONS["BACK_TO_BRANCHES"])
    def back_to_branches(message):
        try:
            if check_join_required(bot, message):
                return
            
            user_session.set(message.chat.id, "selected_branch", None)
            user_session.set(message.chat.id, "step", "waiting_for_branch")
            
            bot.send_message(
                message.chat.id,
                format_branch_text(),
                reply_markup=MenuBuilder.branch_first_menu(),
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Error in back_to_branches: {e}")                                      
