import logging
import time
from telebot import TeleBot
from utils.menu_builder import MenuBuilder
from models.analytics import Analytics
from config import ADMIN_ID

logger = logging.getLogger(__name__)

def register_admin_handlers(bot: TeleBot, analytics: Analytics):
    
    @bot.message_handler(commands=['admin'])
    def admin_panel(message):
        try:
            if message.from_user.id != ADMIN_ID:
                bot.send_message(message.chat.id, "⛔ Unauthorized access!")
                return
            
            total_users = analytics.get_total_users_count()
            active_today = analytics.get_active_today_count()
            total_downloads = analytics.get_total_downloads()

            admin_text = (
                "👑 *Admin Panel*\n\n"
                f"👥 *Total Users:* {total_users}\n"
                f"📅 *Active Today:* {active_today}\n"
                f"📚 *Total Downloads:* {total_downloads}\n\n"
                "📈 *Top Downloads:*\n"
            )
            
            top_downloads = analytics.get_top_downloads(10)
            if top_downloads:
                for sem_branch, count in top_downloads:
                    admin_text += f"• {sem_branch}: {count}\n"
            else:
                admin_text += "• No downloads logged yet.\n"
            
            markup = MenuBuilder.admin_markup()
            
            bot.send_message(message.chat.id, admin_text, parse_mode='Markdown', reply_markup=markup)
        except Exception as e:
            logger.error(f"Error in admin_panel: {e}")
    
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
            
            # Fetch all user IDs from analytics/database
            user_ids = analytics.get_all_user_ids()
            
            for user_id in user_ids:
                try:
                    bot.send_message(user_id, f"📢 *Announcement*\n\n{msg}", parse_mode='Markdown')
                    success += 1
                except Exception:
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
            # Accessible to Admin or Stats check
            total_users = analytics.get_total_users_count()
            active_today = analytics.get_active_today_count()
            total_downloads = analytics.get_total_downloads()

            stats_text = (
                "📊 *Bot Statistics*\n\n"
                f"👥 *Total Users:* {total_users}\n"
                f"📅 *Active Today:* {active_today}\n"
                f"📚 *Total Downloads:* {total_downloads}\n\n"
                f"🕒 *Last Updated:* {time.strftime('%H:%M:%S')}\n"
            )
            
            bot.send_message(message.chat.id, stats_text, parse_mode='Markdown')
        except Exception as e:
            logger.error(f"Error in user_stats: {e}")
