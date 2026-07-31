# BEU Syllabus Bot

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://t.me/EngineersPathwayOfficial)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A Telegram bot designed to help engineering students under **Bihar Engineering University (BEU)** access semester-wise syllabus instantly.

> **Live Bot:** [@BEUSyllabusBot](https://t.me/beu_syllabuss_bot)

---

## 📚 About the Bot

The BEU Syllabus Bot simplifies academic life by providing instant access to B.Tech semester syllabus for multiple branches. Built with a modular architecture for better maintainability and scalability.

### ✨ Features

- 📖 **Instant Syllabus Access** - Download semester-wise syllabus PDFs
- 🏗️ **Branch Support** - CE, CS, EE, ECE, ME, IoT
- 📊 **Analytics Dashboard** - Track bot usage and popular downloads
- 📤 **Share Syllabus** - Share syllabus with friends directly
- 🔒 **Force Join Channel** - Ensures users join the official channel
- 👑 **Admin Panel** - Broadcast messages and view detailed stats
- 🔄 **Daily Reset** - Automatic daily analytics reset

---

## 🏗️ Project Structure

-syllabus-bot/
├── main.py # Entry point
├── config.py # Configuration settings
├── requirements.txt # Dependencies
├── render.yaml # Hosting rander
├── README.md # Documentation
│
├── data/ # Data modules
│ ├── init.py
│ ├── constants.py # Emojis & constants
│ └── syllabus.py # Syllabus database
│
├── models/ # Data models
│ ├── init.py
│ ├── user_session.py # User session management
│ └── analytics.py # Analytics tracking
│
├── handlers/ # Bot handlers
│ ├── init.py
│ ├── base_handlers.py # Core commands (start, help, stats)
│ ├── syllabus_handlers.py # Syllabus flow handlers
│ ├── admin_handlers.py # Admin commands
│ └── callbacks.py # Callback handlers
│
└── utils/ # Utility modules
├── init.py
├── menu_builder.py # UI menu builder
├── validators.py # Validation functions
└── helpers.py # Helper functions

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| **Python 3.8+** | Programming Language |
| **PyTelegramBotAPI** | Telegram Bot API wrapper |
| **Flask** | Health check server |
| **Threading** | Concurrent operations |
| **JSON** | Data persistence |

---

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- Telegram Channel (for force join feature)

### 1. Create a Telegram Bot

1. Open Telegram and message [@BotFather](https://t.me/BotFather)
2. Send `/newbot` and follow the instructions
3. Copy the API token provided by BotFather

### 2. Clone the Repository

```bash
git clone https://github.com/yourusername/beu-syllabus-bot.git
cd beu-syllabus-bot

3. Install Dependencies
bash
pip install -r requirements.txt

4. Configure Environment Variables
Create a .env file in the root directory:

env
BOT_TOKEN=your_telegram_bot_token_here
PORT=8080
LOG_LEVEL=INFO
Or set them directly in your environment:

bash
export BOT_TOKEN="your_telegram_bot_token_here"

5. Update Configuration
Edit config.py to customize: python

# config.py
CHANNEL_USERNAME = "@YourChannelUsername"  # Your Telegram channel
ADMIN_ID = 123456789  # Your Telegram User ID (for admin access)

6. Run the Bot
bash
python main.py

📦 Deployment
Deploy on Railway Fork this repository

Create a new project on Railway

Connect your GitHub repository

Add environment variables:

BOT_TOKEN: Your bot token

PORT: 8080 (default)

Deploy!

Deploy on Render
Create a new Web Service on Render

Connect your GitHub repository

Set the start command: python main.py

Add environment variables

Deploy!

Deploy on Heroku
bash
heroku create beu-syllabus-bot
heroku config:set BOT_TOKEN=your_token_here
heroku addons:create heroku-postgresql:hobby-dev  # Optional
git push heroku main

🔧 Commands
User Commands Description
/start or /menu	Show main menu
📚 Syllabus	Access syllabus
📊 Stats	View bot statistics
ℹ️ Help	Show help guide
⭐ Feedback	Send feedback to admin
🔄 Reset	Reset current session

Admin Commands
Command	Description
/admin	Open admin panel
/broadcast <message>	Send message to all users
/stats	View detailed statistics

🗂️ Syllabus Data
The syllabus database includes:

Semesters: 1st to 8th (New & Old curriculum)

Branches: CE, CS, EE, ECE, ME, IoT

Format: Google Drive links (PDF)

To update syllabus data, edit data/syllabus.py.

📊 Analytics
The bot tracks:

Total users

Daily active users

Command usage statistics

Daily download counts

Analytics data is stored in analytics.json and resets daily.

🤝 Contributing
Contributions are welcome! Here's how you can help:

Fork the repository

Create a feature branch: git checkout -b feature/your-feature

Commit changes: git commit -m 'Add some feature'

Push: git push origin feature/your-feature

Open a Pull Request

👨‍💻 Developer
Md Zafar - LinkedIn

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments

PyTelegramBotAPI - Telegram Bot API wrapper

Flask - Web framework for health checks

All contributors and users of the bot

📞 Support
For issues, questions, or suggestions:

Open an issue

Contact the developer

📈 TODO
□ Add search functionality
□ Add more branches
□ Implement user preferences
□ Add multi-language support
□ Create web dashboard for analytics


🌟 Star this repository if you find it helpful!

