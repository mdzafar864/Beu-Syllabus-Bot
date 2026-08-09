```python
import logging
import time

from telebot import TeleBot
from models.analytics import Analytics
from utils.menu_builder import MenuBuilder
from config import ADMIN_ID


logger = logging.getLogger(__name__)


def register_admin_handlers(bot: TeleBot, analytics: Analytics):

    # =========================================================
    # ADMIN ACCESS CHECK
    # =========================================================
    def is_admin(message):
        return message.from_user.id == ADMIN_ID

    # =========================================================
    # UNAUTHORIZED MESSAGE
    # =========================================================
    def send_access_denied(message):
        bot.send_message(
            message.chat.id,
            "🔐 Admin Access Required\n\n"
            "You don't have permission to access this section."
        )

    # =========================================================
    # /admin
    # =========================================================
    @bot.message_handler(commands=["admin"])
    def admin_panel(message):
        try:
            if not is_admin(message):
                send_access_denied(message)
                return

            total_users = getattr(
                analytics,
                "total_users",
                set()
            )

            daily_active = getattr(
                analytics,
                "daily_active",
                set()
            )

            daily_downloads = getattr(
                analytics,
                "daily_downloads",
                {}
            )

            try:
                total_downloads = sum(
                    daily_downloads.values()
                )
            except Exception:
                total_downloads = 0

            admin_text = (
                "📊 *Admin Panel*\n"
                "_Access verified successfully. Welcome, Admin!_\n\n"
                f"👥 *Total Users:* {len(total_users)}\n"
                f"📅 *Active Today:* {len(daily_active)}\n"
                f"📚 *Total Downloads:* {total_downloads}\n\n"
                "📈 *Top Downloads:*\n"
            )

            try:
                top_downloads = analytics.get_top_downloads(10)

                if top_downloads:
                    for sem_branch, count in top_downloads:
                        admin_text += (
                            f"• {sem_branch}: {count}\n"
                        )
                else:
                    admin_text += (
                        "• No download data available.\n"
                    )

            except Exception as e:
                logger.error(
                    f"Error getting top downloads: {e}"
                )

                admin_text += (
                    "• No download data available.\n"
                )

            markup = MenuBuilder.admin_markup()

            bot.send_message(
                message.chat.id,
                admin_text,
                parse_mode="Markdown",
                reply_markup=markup
            )

        except Exception as e:
            logger.exception(
                f"Error in admin_panel: {e}"
            )

            bot.send_message(
                message.chat.id,
                "⚠️ Admin panel load karte waqt error aa gaya."
            )

    # =========================================================
    # /broadcast
    # =========================================================
    @bot.message_handler(commands=["broadcast"])
    def broadcast_message(message):
        try:
            if not is_admin(message):
                send_access_denied(message)
                return

            # Remove /broadcast command
            msg = message.text[
                len("/broadcast"):
            ].strip()

            if not msg:
                bot.send_message(
                    message.chat.id,
                    "⚠️ *Usage:*\n\n"
                    "`/broadcast Your message here`",
                    parse_mode="Markdown"
                )
                return

            total_users = getattr(
                analytics,
                "total_users",
                set()
            )

            success = 0
            failed = 0

            status_msg = bot.send_message(
                message.chat.id,
                "📤 *Sending broadcast...*\n\n"
                "Please wait.",
                parse_mode="Markdown"
            )

            for user_id in list(total_users):

                try:
                    bot.send_message(
                        user_id,
                        f"📢 *Announcement*\n\n{msg}",
                        parse_mode="Markdown"
                    )

                    success += 1

                except Exception as e:
                    failed += 1

                    logger.warning(
                        f"Broadcast failed for user "
                        f"{user_id}: {e}"
                    )

                # Telegram rate-limit protection
                time.sleep(0.1)

            result_text = (
                "✅ *Broadcast Completed!*\n\n"
                f"✓ Success: {success}\n"
                f"✗ Failed: {failed}\n"
                f"👥 Total: {success + failed}"
            )

            bot.edit_message_text(
                result_text,
                message.chat.id,
                status_msg.message_id,
                parse_mode="Markdown"
            )

        except Exception as e:
            logger.exception(
                f"Error in broadcast_message: {e}"
            )

            bot.send_message(
                message.chat.id,
                "❌ Broadcast complete nahi ho saka."
            )

    # =========================================================
    # /stats
    # =========================================================
    @bot.message_handler(commands=["stats"])
    def user_stats(message):
        try:
            if not is_admin(message):
                send_access_denied(message)
                return

            # -------------------------------------------------
            # GET ANALYTICS DATA SAFELY
            # -------------------------------------------------
            total_users = getattr(
                analytics,
                "total_users",
                set()
            )

            daily_active = getattr(
                analytics,
                "daily_active",
                set()
            )

            daily_downloads = getattr(
                analytics,
                "daily_downloads",
                {}
            )

            command_stats = getattr(
                analytics,
                "command_stats",
                {}
            )

            # -------------------------------------------------
            # TOTAL DOWNLOADS
            # -------------------------------------------------
            try:
                total_downloads = sum(
                    daily_downloads.values()
                )
            except Exception:
                total_downloads = 0

            # -------------------------------------------------
            # BASIC STATISTICS
            # -------------------------------------------------
            stats_text = (
                "📊 *Detailed Statistics*\n\n"
                f"👥 *Total Users:* {len(total_users)}\n"
                f"📅 *Active Today:* {len(daily_active)}\n"
                f"📚 *Total Downloads:* {total_downloads}\n\n"
                "📈 *Command Usage:*\n"
            )

            # -------------------------------------------------
            # COMMAND USAGE
            # -------------------------------------------------
            if (
                isinstance(command_stats, dict)
                and command_stats
            ):
                try:
                    sorted_commands = sorted(
                        command_stats.items(),
                        key=lambda x: x[1],
                        reverse=True
                    )[:10]

                    for cmd, count in sorted_commands:

                        cmd_name = str(cmd)

                        if not cmd_name.startswith("/"):
                            cmd_name = "/" + cmd_name

                        stats_text += (
                            f"• `{cmd_name}` — {count}\n"
                        )

                except Exception as e:
                    logger.error(
                        f"Error sorting command stats: {e}"
                    )

                    stats_text += (
                        "• Unable to load command usage.\n"
                    )

            else:
                stats_text += (
                    "• No command usage data available.\n"
                )

            # -------------------------------------------------
            # SEND STATISTICS
            # -------------------------------------------------
            bot.send_message(
                message.chat.id,
                stats_text,
                parse_mode="Markdown"
            )

            logger.info(
                f"Admin stats viewed by "
                f"user {message.from_user.id}"
            )

        except Exception as e:
            logger.exception(
                f"Error in user_stats: {e}"
            )

            bot.send_message(
                message.chat.id,
                "❌ Statistics load karte waqt "
                "error aa gaya.\n\n"
                "Please check bot logs."
            )

    # =========================================================
    # ADMIN HANDLERS REGISTERED
    # =========================================================
    logger.info(
        "✅ Admin handlers registered successfully"
    )
```           
