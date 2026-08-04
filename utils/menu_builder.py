from typing import List
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from data.constants import BRANCH_EMOJIS, MENU_BUTTONS


class MenuBuilder:

    @staticmethod
    def main_menu() -> ReplyKeyboardMarkup:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(
            MENU_BUTTONS["SYLLABUS"],
            MENU_BUTTONS["STATS"],
            MENU_BUTTONS["HELP"],
            MENU_BUTTONS["FEEDBACK"],
            MENU_BUTTONS["RESET"],
        )
        return markup

    @staticmethod
    def branch_first_menu() -> ReplyKeyboardMarkup:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        branch_buttons = [f"{emoji}" for emoji in BRANCH_EMOJIS.values()]
        markup.add(*branch_buttons)
        markup.add(MENU_BUTTONS["MAIN_MENU"])
        return markup

    @staticmethod
    def semester_for_branch_menu(
        branch: str, available_semesters: List[str]
    ) -> ReplyKeyboardMarkup:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        sem_buttons = [f"📖 {sem}" for sem in available_semesters]
        markup.add(*sem_buttons)
        markup.row(
            MENU_BUTTONS["BACK_TO_BRANCHES"], MENU_BUTTONS["MAIN_MENU"]
        )
        return markup

    @staticmethod
    def force_join_markup() -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton(
                "📢 Join Telegram Channel",
                url="https://t.me/EngineersPathwayOfficial",
            ),
            InlineKeyboardButton(
                "✅ I've Joined", callback_data="check_join"
            ),
        )
        return markup

    @staticmethod
    def download_markup(
        download_url: str, semester: str, branch: str
    ) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("⬇️ Download PDF", url=download_url),
            InlineKeyboardButton(
                "📤 Share Syllabus",
                switch_inline_query=f"{semester} {branch} Syllabus",
            ),
        )
        return markup

    @staticmethod
    def admin_markup() -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("📊 Full Stats", callback_data="full_stats"),
            InlineKeyboardButton("💾 Save Data", callback_data="save_data"),
        )
        return markup
