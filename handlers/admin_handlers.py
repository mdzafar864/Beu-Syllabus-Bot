import logging
import time
import html

from telebot import TeleBot
from utils.menu_builder import MenuBuilder
from models.analytics import Analytics
from config import ADMIN_ID

logger = logging.getLogger(**name**)

def register_admin_handlers(bot: TeleBot, analytics: Analytics):

```
# ------------------ ADMIN PANEL COMMAND ------------------ #
@bot.message_handler(commands=["admin"])
def admin_panel(message):
    try:
        if message.from_user.id != ADMIN_ID:
            bot.send_message(
                message.chat.id,
                "🔐 Admin Access Required\n\n"
                "You don't have permission to access this section."
            )
            return

        total_users_count = len(
            getattr(analytics, "total_users", [])
        )

        daily_active_count = len(
            getattr(analytics, "daily_active", [])
        )

        daily_downloads_dict = (
            getattr(analytics, "daily_downloads", {}) or {}
        )

        total_downloads_count = (
            sum(daily_downloads_dict.values())
            if daily_downloads_dict
            else 0
        )

        admin_text = (
            "📊 <b>Admin Panel</b>\n"
            "<i>Access verified successfully. Welcome, Admin!</i>\n\n"
            f"👥 <b>Total Users:</b> {total_users_count}\n"
            f"📅 <b>Active Today:</b> {daily_active_count}\n"
            f"📚 <b>Total Downloads:</b> {total_downloads_count}\n\n"
            "📈 <b>Top Downloads:</b>\n"
        )

        top_downloads = (
            analytics.get_top_downloads(10)
            if hasattr(analytics, "get_top_downloads")
            else []
        )

        if top_downloads:
            for sem_branch, count in top_downloads:
                safe_sem_branch = html.escape(str(sem_branch))
                admin_text += (
                    f"• {safe_sem_branch}: {count}\n"
                )
        else:
            admin_text += "<i>No download data available.</i>\n"

        markup = MenuBuilder.admin_markup()

        bot.send_message(
            message.chat.id,
            admin_text,
            parse_mode="HTML",
            reply_markup=markup
        )

    except Exception as e:
        logger.exception("Error in admin_panel")

        bot.send_message(
            message.chat.id,
            "⚠️ Error loading admin panel:\n"
            f"<code>{html.escape(str(e))}</code>",
            parse_mode="HTML"
        )

# ------------------ BROADCAST COMMAND ------------------ #
@bot.message_handler(commands=["broadcast"])
def broadcast_message(message):
    try:
        if message.from_user.id != ADMIN_ID:
            bot.send_message(
                message.chat.id,
                "🔐 Admin Access Required\n\n"
                "You don't have permission to access this section."
            )
            return

        msg = message.text.replace("/broadcast", "", 1).strip()

        if not msg:
            bot.send_message(
                message.chat.id,
                "⚠️ Usage: /broadcast <message>"
            )
            return

        success = 0
        failed = 0

        status_msg = bot.send_message(
            message.chat.id,
            "📤 Sending broadcast..."
        )

        user_list = list(
            getattr(analytics, "total_users", [])
        )

        for user_id in user_list:
            try:
                bot.send_message(
                    user_id,
                    "📢 <b>Announcement</b>\n\n"
                    f"{html.escape(msg)}",
                    parse_mode="HTML"
                )
                success += 1

            except Exception:
                failed += 1

            # Small delay to reduce Telegram rate-limit risk
            time.sleep(0.1)

        bot.edit_message_text(
            "✅ <b>Broadcast completed!</b>\n\n"
            f"✓ Success: {success}\n"
            f"✗ Failed: {failed}",
            message.chat.id,
            status_msg.message_id,
            parse_mode="HTML"
        )

    except Exception as e:
        logger.exception("Error in broadcast_message")

        bot.send_message(
            message.chat.id,
            "⚠️ Broadcast error:\n"
            f"<code>{html.escape(str(e))}</code>",
            parse_mode="HTML"
        )

# ------------------ HELPER FUNCTION FOR STATS ------------------ #
def build_stats_text():
    total_users_count = len(
        getattr(analytics, "total_users", [])
    )

    daily_active_count = len(
        getattr(analytics, "daily_active", [])
    )

    daily_downloads_dict = (
        getattr(analytics, "daily_downloads", {}) or {}
    )

    total_downloads_count = (
        sum(daily_downloads_dict.values())
        if daily_downloads_dict
        else 0
    )

    cmd_stats_dict = (
        getattr(analytics, "command_stats", {}) or {}
    )

    stats_text = (
        "📊 <b>Detailed Statistics</b>\n\n"
        f"👥 <b>Total Users:</b> {total_users_count}\n"
        f"📅 <b>Active Today:</b> {daily_active_count}\n"
        f"📚 <b>Total Downloads:</b> {total_downloads_count}\n\n"
        "📈 <b>Command Usage:</b>\n"
    )

    if cmd_stats_dict:
        sorted_cmds = sorted(
            cmd_stats_dict.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]

        for cmd, count in sorted_cmds:
            safe_cmd = html.escape(str(cmd))
            stats_text += f"• /{safe_cmd}: {count}\n"

    else:
        stats_text += (
            "<i>No command stats recorded yet.</i>\n"
        )

    return stats_text

# ------------------ /stats TEXT COMMAND ------------------ #
@bot.message_handler(commands=["stats"])
def user_stats(message):
    try:
        if message.from_user.id != ADMIN_ID:
            bot.send_message(
                message.chat.id,
                "🔐 Admin Access Required\n\n"
                "You don't have permission to access this section."
            )
            return

        stats_text = build_stats_text()

        bot.send_message(
            message.chat.id,
            stats_text,
            parse_mode="HTML"
        )

    except Exception as e:
        logger.exception("Error in user_stats")

        bot.send_message(
            message.chat.id,
            "⚠️ Error fetching stats:\n"
            f"<code>{html.escape(str(e))}</code>",
            parse_mode="HTML"
        )

# ------------------ INLINE BUTTON CALLBACK HANDLER ------------------ #
@bot.callback_query_handler(
    func=lambda call: call.data in [
        "stats",
        "admin_stats",
        "📊 stats"
    ]
)
def stats_callback(call):
    try:
        if call.from_user.id != ADMIN_ID:
            bot.answer_callback_query(
                call.id,
                "🔐 Admin Access Required",
                show_alert=True
            )
            return

        stats_text = build_stats_text()

        bot.edit_message_text(
            stats_text,
            call.message.chat.id,
            call.message.message_id,
            parse_mode="HTML"
        )

        bot.answer_callback_query(call.id)

    except Exception as e:
        logger.exception("Error in stats_callback")

        bot.answer_callback_query(
            call.id,
            "⚠️ Could not load stats.",
            show_alert=True
        )
