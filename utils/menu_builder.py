# In utils/menu_builder.py

@staticmethod
def semester_for_branch_menu(branch, semesters):
    """Create menu for semester selection"""
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    buttons = []
    
    for sem in semesters:
        # Display semester as is (e.g., "1st New", "2nd Old", "4th")
        buttons.append(types.KeyboardButton(f"📖 {sem}"))
    
    # Add buttons in rows of 3
    for i in range(0, len(buttons), 3):
        row = buttons[i:i+3]
        markup.row(*row)
    
    # Add back button
    markup.row(types.KeyboardButton(MENU_BUTTONS["BACK_TO_BRANCHES"]))
    markup.row(types.KeyboardButton(MENU_BUTTONS["MAIN_MENU"]))
    
    return markup
