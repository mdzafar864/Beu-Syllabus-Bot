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
    
    # Debug: Log syllabus structure when handlers are registered
    logger.info("📚 ===== SYLLABUS DATA STRUCTURE =====")
    logger.info(f"📚 Total semesters in SYLLABUS: {len(SYLLABUS)}")
    if SYLLABUS:
        for sem, branches in SYLLABUS.items():
            logger.info(f"  📖 Semester {sem}: {list(branches.keys()) if isinstance(branches, dict) else 'INVALID STRUCTURE'}")
    else:
        logger.error("❌ SYLLABUS IS EMPTY OR NOT LOADED!")
    logger.info("📚 ====================================")
    
    @bot.message_handler(func=lambda m: m.text == MENU_BUTTONS["SYLLABUS"])
    def show_branches_first(message):
        try:
            if check_join_required(bot, message):
                return
            
            # Log the user action
            logger.info(f"📚 User {message.chat.id} accessed syllabus menu")
            
            # Check if SYLLABUS has data
            if not SYLLABUS:
                bot.send_message(
                    message.chat.id,
                    "❌ Syllabus data is currently not available. Please contact admin.",
                    reply_markup=MenuBuilder.main_menu()
                )
                return
            
            user_session.set(message.chat.id, "step", "waiting_for_branch")
            
            # Send branch selection menu
            branch_text = format_branch_text()
            branch_markup = MenuBuilder.branch_first_menu()
            
            bot.send_message(
                message.chat.id,
                branch_text,
                reply_markup=branch_markup,
                parse_mode='Markdown'
            )
            logger.info(f"✅ Branch menu shown to user {message.chat.id}")
            
        except Exception as e:
            logger.error(f"❌ Error in show_branches_first: {e}", exc_info=True)
            bot.send_message(
                message.chat.id,
                "⚠️ Error loading syllabus menu. Please try again later.",
                reply_markup=MenuBuilder.main_menu()
            )
    
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
                bot.send_message(message.chat.id, "❌ Invalid branch! Please select from the menu.")
                return
            
            logger.info(f"📚 User {message.chat.id} selected branch: {selected_branch}")
            
            # Store selected branch in session
            user_session.set(message.chat.id, "selected_branch", selected_branch)
            user_session.set(message.chat.id, "step", "waiting_for_semester")
            
            # Find which semesters have this branch
            available_semesters = []
            for sem, branches in SYLLABUS.items():
                if isinstance(branches, dict) and selected_branch in branches:
                    available_semesters.append(sem)
                elif isinstance(branches, dict):
                    # Debug: Log available branches for each semester
                    logger.debug(f"  Semester {sem} has branches: {list(branches.keys())}")
            
            if not available_semesters:
                bot.send_message(
                    message.chat.id,
                    f"❌ {BRANCH_EMOJIS.get(selected_branch, selected_branch)} branch का कोई syllabus उपलब्ध नहीं है।\n\n"
                    f"Available semesters: {list(SYLLABUS.keys())}\n"
                    f"Available branches per semester may vary.",
                    reply_markup=MenuBuilder.main_menu()
                )
                logger.warning(f"⚠️ No syllabus found for branch {selected_branch}")
                return
            
            # Sort semesters properly (as numbers)
            available_semesters.sort(key=lambda x: int(x) if x.isdigit() else 999)
            
            semester_text = format_semester_text(selected_branch, available_semesters)
            semester_markup = MenuBuilder.semester_for_branch_menu(selected_branch, available_semesters)
            
            bot.send_message(
                message.chat.id,
                semester_text,
                reply_markup=semester_markup,
                parse_mode='Markdown'
            )
            logger.info(f"✅ Semester menu shown to user {message.chat.id} for branch {selected_branch}")
            
        except Exception as e:
            logger.error(f"❌ Error in branch_selected_first: {e}", exc_info=True)
            bot.send_message(
                message.chat.id,
                "⚠️ Error! Please try again.",
                reply_markup=MenuBuilder.main_menu()
            )
    
    @bot.message_handler(func=lambda m: m.text and m.text.startswith("📖 "))
    def semester_after_branch(message):
        try:
            if check_join_required(bot, message):
                return
            
            semester = message.text.replace("📖 ", "").strip()
            logger.info(f"📚 User {message.chat.id} selected semester: {semester}")
            
            session = user_session.get(message.chat.id)
            
            if not session or not session.get("selected_branch"):
                bot.send_message(
                    message.chat.id,
                    "⚠️ पहले Branch चुनें!",
                    reply_markup=MenuBuilder.branch_first_menu()
                )
                return
            
            branch = session["selected_branch"]
            logger.info(f"📚 Retrieving syllabus for Branch: {branch}, Semester: {semester}")
            
            # Check if syllabus exists for this branch and semester
            if semester not in SYLLABUS:
                bot.send_message(
                    message.chat.id,
                    f"❌ Semester {semester} का syllabus उपलब्ध नहीं है।\n\n"
                    f"Available semesters: {', '.join(list(SYLLABUS.keys()))}",
                    reply_markup=MenuBuilder.main_menu()
                )
                return
            
            semester_data = SYLLABUS[semester]
            
            if not isinstance(semester_data, dict):
                bot.send_message(
                    message.chat.id,
                    f"❌ Data format error for semester {semester}. Please contact admin.",
                    reply_markup=MenuBuilder.main_menu()
                )
                logger.error(f"❌ Semester data is not a dict: {type(semester_data)}")
                return
            
            if branch not in semester_data:
                bot.send_message(
                    message.chat.id,
                    f"❌ {BRANCH_EMOJIS.get(branch, branch)} branch का {semester} semester का syllabus उपलब्ध नहीं है।\n\n"
                    f"Available branches for semester {semester}: {', '.join(list(semester_data.keys()))}",
                    reply_markup=MenuBuilder.main_menu()
                )
                logger.warning(f"⚠️ Branch {branch} not found in semester {semester}")
                return
            
            original_url = semester_data[branch]
            download_url = get_download_link(original_url)
            
            # Track download
            analytics.track_download(semester, branch)
            logger.info(f"📊 Download tracked: {semester} - {branch}")
            
            # Create download markup
            markup = MenuBuilder.download_markup(download_url, semester, branch)
            
            bot.send_chat_action(message.chat.id, 'typing')
            
            # Send the syllabus file
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
                logger.info(f"✅ Syllabus sent: {semester} - {branch} to user {message.chat.id}")
                
            except Exception as doc_error:
                logger.error(f"❌ Document send failed: {doc_error}", exc_info=True)
                
                # Try sending as link instead
                bot.send_message(
                    message.chat.id,
                    f"📚 *{semester} Semester - {BRANCH_EMOJIS.get(branch, branch)} Syllabus*\n\n"
                    f"✅ Syllabus ready! Click the button below to download.\n\n"
                    f"📊 Downloads Today: {analytics.daily_downloads.get(f'{semester}_{branch}', 0)}",
                    reply_markup=markup,
                    parse_mode='Markdown'
                )
                
        except Exception as e:
            logger.error(f"❌ Error in semester_after_branch: {e}", exc_info=True)
            bot.send_message(
                message.chat.id,
                "⚠️ Error loading syllabus. Please try again.",
                reply_markup=MenuBuilder.main_menu()
            )
    
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
            logger.info(f"✅ User {message.chat.id} returned to branches menu")
            
        except Exception as e:
            logger.error(f"❌ Error in back_to_branches: {e}", exc_info=True)
