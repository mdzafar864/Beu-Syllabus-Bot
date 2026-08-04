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
    
    # Debug: Log syllabus structure
    logger.info("📚 ===== SYLLABUS DATA STRUCTURE =====")
    logger.info(f"📚 Total semesters: {len(SYLLABUS)}")
    if SYLLABUS:
        for sem, branches in SYLLABUS.items():
            logger.info(f"  📖 {sem}: {list(branches.keys()) if isinstance(branches, dict) else 'INVALID'}")
    logger.info("📚 ====================================")
    
    @bot.message_handler(func=lambda m: m.text == MENU_BUTTONS["SYLLABUS"])
    def show_branches_first(message):
        try:
            if check_join_required(bot, message):
                return
            
            if not SYLLABUS:
                bot.send_message(
                    message.chat.id,
                    "❌ Syllabus data is currently not available. Please contact admin.",
                    reply_markup=MenuBuilder.main_menu()
                )
                return
            
            user_session.set(message.chat.id, "step", "waiting_for_branch")
            
            bot.send_message(
                message.chat.id,
                format_branch_text(),
                reply_markup=MenuBuilder.branch_first_menu(),
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
                bot.send_message(message.chat.id, "❌ Invalid branch!")
                return
            
            logger.info(f"📚 User {message.chat.id} selected branch: {selected_branch}")
            
            # Store selected branch in session
            user_session.set(message.chat.id, "selected_branch", selected_branch)
            user_session.set(message.chat.id, "step", "waiting_for_semester")
            
            # Find which semesters have this branch
            available_semesters = []
            semester_display_names = {}  # Map display name to actual key
            
            for sem_key, branches in SYLLABUS.items():
                if isinstance(branches, dict) and selected_branch in branches:
                    # Create a clean display name
                    if "New" in sem_key or "Old" in sem_key:
                        # For "1st New", show as "1st New"
                        display_name = sem_key
                    else:
                        # For "4th", show as "4"
                        display_name = sem_key.replace("th", "").replace("st", "").replace("nd", "").replace("rd", "")
                    
                    available_semesters.append(display_name)
                    semester_display_names[display_name] = sem_key  # Map display to actual
            
            if not available_semesters:
                bot.send_message(
                    message.chat.id,
                    f"❌ {BRANCH_EMOJIS.get(selected_branch, selected_branch)} branch का कोई syllabus उपलब्ध नहीं है।",
                    reply_markup=MenuBuilder.main_menu()
                )
                return
            
            # Sort semesters properly
            def sort_key(s):
                # Extract number from display name
                import re
                numbers = re.findall(r'\d+', s)
                return int(numbers[0]) if numbers else 999
            
            available_semesters.sort(key=sort_key)
            
            # Store the mapping in session for later use
            user_session.set(message.chat.id, "semester_mapping", semester_display_names)
            
            bot.send_message(
                message.chat.id,
                format_semester_text(selected_branch, available_semesters),
                reply_markup=MenuBuilder.semester_for_branch_menu(selected_branch, available_semesters),
                parse_mode='Markdown'
            )
            logger.info(f"✅ Semester menu shown for branch {selected_branch}")
            
        except Exception as e:
            logger.error(f"❌ Error in branch_selected_first: {e}", exc_info=True)
            bot.send_message(
                message.chat.id,
                "⚠️ Error! Please try again.",
                reply_markup=MenuBuilder.main_menu()
            )
    
    @bot.message_handler(func=lambda m: m.text and (m.text.startswith("📖 ") or m.text.startswith("📚 ")))
    def semester_after_branch(message):
        try:
            if check_join_required(bot, message):
                return
            
            # Extract semester from message (remove emoji and space)
            semester_display = message.text.split(" ", 1)[-1].strip()
            logger.info(f"📚 User {message.chat.id} selected semester display: {semester_display}")
            
            session = user_session.get(message.chat.id)
            
            if not session or not session.get("selected_branch"):
                bot.send_message(
                    message.chat.id,
                    "⚠️ पहले Branch चुनें!",
                    reply_markup=MenuBuilder.branch_first_menu()
                )
                return
            
            branch = session["selected_branch"]
            
            # Get the actual semester key from mapping or use display name directly
            semester_mapping = session.get("semester_mapping", {})
            
            # Try to find the actual key
            actual_semester_key = None
            
            # Check if display is directly in SYLLABUS
            if semester_display in SYLLABUS:
                actual_semester_key = semester_display
            # Check if display is in mapping
            elif semester_display in semester_mapping:
                actual_semester_key = semester_mapping[semester_display]
            # Try to match by number (e.g., "1" matches "1st New" or "1st Old")
            else:
                # Extract number from display
                import re
                display_num = re.findall(r'\d+', semester_display)
                if display_num:
                    num = display_num[0]
                    # Find all semesters with this number
                    matching_keys = [k for k in SYLLABUS.keys() if k.startswith(num)]
                    if matching_keys:
                        # If multiple (New and Old), ask user which one
                        if len(matching_keys) > 1:
                            # Create inline keyboard for New/Old selection
                            from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
                            markup = InlineKeyboardMarkup(row_width=2)
                            for key in matching_keys:
                                markup.add(InlineKeyboardButton(
                                    text=key,
                                    callback_data=f"sem_{key}_{branch}"
                                ))
                            bot.send_message(
                                message.chat.id,
                                f"⚠️ Multiple versions found for Semester {num}. Please select one:",
                                reply_markup=markup
                            )
                            return
                        else:
                            actual_semester_key = matching_keys[0]
            
            if not actual_semester_key:
                bot.send_message(
                    message.chat.id,
                    f"❌ Semester '{semester_display}' not found.\n\n"
                    f"Available semesters: {', '.join(list(SYLLABUS.keys()))}",
                    reply_markup=MenuBuilder.main_menu()
                )
                return
            
            # Check if branch exists in this semester
            semester_data = SYLLABUS[actual_semester_key]
            
            if not isinstance(semester_data, dict):
                bot.send_message(
                    message.chat.id,
                    f"❌ Data format error for {actual_semester_key}. Please contact admin.",
                    reply_markup=MenuBuilder.main_menu()
                )
                return
            
            if branch not in semester_data:
                bot.send_message(
                    message.chat.id,
                    f"❌ {BRANCH_EMOJIS.get(branch, branch)} branch का {actual_semester_key} semester का syllabus उपलब्ध नहीं है।\n\n"
                    f"Available branches: {', '.join(list(semester_data.keys()))}",
                    reply_markup=MenuBuilder.main_menu()
                )
                return
            
            original_url = semester_data[branch]
            download_url = get_download_link(original_url)
            
            analytics.track_download(actual_semester_key, branch)
            
            markup = MenuBuilder.download_markup(download_url, actual_semester_key, branch)
            
            bot.send_chat_action(message.chat.id, 'typing')
            
            try:
                bot.send_document(
                    message.chat.id,
                    download_url,
                    caption=f"📚 *{actual_semester_key} Semester - {BRANCH_EMOJIS.get(branch, branch)} Syllabus*\n\n"
                           f"📅 *Requested:* {datetime.now().strftime('%d %b %Y, %I:%M %p')}\n"
                           f"📊 *Downloads Today:* {analytics.daily_downloads.get(f'{actual_semester_key}_{branch}', 0)}",
                    reply_markup=markup,
                    parse_mode='Markdown'
                )
                logger.info(f"✅ Syllabus sent: {actual_semester_key} - {branch}")
                
            except Exception as doc_error:
                logger.error(f"❌ Document send failed: {doc_error}")
                bot.send_message(
                    message.chat.id,
                    f"📚 *{actual_semester_key} Semester - {BRANCH_EMOJIS.get(branch, branch)} Syllabus*\n\n"
                    f"✅ Syllabus ready! Click the button below to download.\n\n"
                    f"📊 Downloads Today: {analytics.daily_downloads.get(f'{actual_semester_key}_{branch}', 0)}",
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
        except Exception as e:
            logger.error(f"❌ Error in back_to_branches: {e}", exc_info=True)
