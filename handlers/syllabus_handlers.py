# handlers/syllabus_handlers.py

from utils.menu_builder import MenuBuilder
from services.database import DatabaseService  # आपकी डेटाबेस फाइल

@bot.message_handler(func=lambda message: message.text.startswith("📖"))
def handle_semester_select(message):
    user_id = message.from_user.id
    
    # 1. इमोजी "📖 " को हटाकर केवल शुद्ध सेमेस्टर नेम (जैसे "Semester 1" या "1") निकालें
    clean_semester = message.text.replace("📖", "").strip()
    
    # 2. यूज़र की चुनी हुई ब्रांच प्राप्त करें (जैसे "EE", "CSE")
    user_branch = UserSession.get_branch(user_id) 

    # 3. Supabase से क्लीन डेटा भेजकर PDF सर्च करें
    pdf_url = DatabaseService.get_syllabus_pdf(user_branch, clean_semester)

    if pdf_url:
        markup = MenuBuilder.download_markup(pdf_url, clean_semester, user_branch)
        bot.send_message(
            message.chat.id, 
            f"📚 *{user_branch} - {clean_semester} Syllabus*\n\nनीचे दिए गए बटन से PDF डाउनलोड करें:",
            reply_markup=markup,
            parse_mode="Markdown"
        )
    else:
        bot.send_message(message.chat.id, "❌ इस सेमेस्टर का सिलेबस डेटाबेस में नहीं मिला।")
        
