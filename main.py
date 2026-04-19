@bot.message_handler(func=lambda m: m.text == "⭐ Feedback")
def get_feedback(message):
    if not is_member(message.chat.id):
        send_join_required(message)
        return
    
    feedback_text = (
        "💬 *Send Feedback*\n\n"
        "We value your feedback! Please send your:\n"
        "• Suggestions for improvement\n"
        "• Bug reports\n"
        "• Feature requests\n\n"
        "Just type your message below, and it will be forwarded to the admin."
    )
    bot.send_message(message.chat.id, feedback_text, parse_mode='Markdown')
    bot.register_next_step_handler(message, process_feedback)

def process_feedback(message):
    feedback_content = message.text
    ADMIN_ID = 5861904079  # Your Telegram ID
    
    # Get complete user information
    first_name = message.from_user.first_name or "N/A"
    last_name = message.from_user.last_name or "N/A"
    username = message.from_user.username or "N/A"
    user_id = message.from_user.id
    
    # Create detailed feedback message
    feedback_msg = (
        f"📝 *New Feedback Received!*\n\n"
        f"👤 *User Information:*\n"
        f"├ First Name: `{first_name}`\n"
        f"├ Last Name: `{last_name}`\n"
        f"├ Username: @{username}\n"
        f"└ User ID: `{user_id}`\n\n"
        f"💬 *Feedback Message:*\n"
        f"└ {feedback_content}\n\n"
        f"🕐 *Time:* {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
    )
    
    try:
        # Send feedback to admin
        bot.send_message(ADMIN_ID, feedback_msg, parse_mode='Markdown')
        
        # Send confirmation to user
        bot.send_message(
            message.chat.id,
            "✅ *Thank you for your feedback!*\n\n"
            "Your message has been sent to the admin. We'll review it and get back to you if needed.\n\n"
            "🙏 Thanks for helping us improve!",
            reply_markup=MenuBuilder.main_menu(),
            parse_mode='Markdown'
        )
        
        logger.info(f"Feedback sent from user {user_id} (@{username})")
        
    except Exception as e:
        logger.error(f"Failed to send feedback to admin: {e}")
        bot.send_message(
            message.chat.id,
            "⚠️ *Sorry!*\n\n"
            "There was an issue sending your feedback. Please try again later or contact support directly.\n\n"
            "📢 Join our channel for support: @EngineersPathwayOfficial",
            reply_markup=MenuBuilder.main_menu(),
            parse_mode='Markdown'
        )