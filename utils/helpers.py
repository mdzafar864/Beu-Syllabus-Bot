from datetime import datetime
from data.constants import BRANCH_EMOJIS

def get_download_link(drive_url: str) -> str:
    """Extract download link from Google Drive URL"""
    try:
        if "id=" in drive_url:
            file_id = drive_url.split("id=")[-1]
        elif "/d/" in drive_url:
            file_id = drive_url.split("/d/")[1].split("/")[0]
        else:
            return drive_url
        
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    except:
        return drive_url

def format_branch_text() -> str:
    """Format branch selection text"""
    text = "🏗️ *पहले अपनी Branch चुनें:*\n\n"
    for branch, emoji_name in BRANCH_EMOJIS.items():
        text += f"• {emoji_name}\n"
    text += "\n💡 *Branch चुनने के बाद Semester select करेंगे*"
    return text

def format_semester_text(branch: str, available_semesters: list) -> str:
    """Format semester selection text"""
    branch_name = BRANCH_EMOJIS.get(branch, branch)
    text = f"📚 *{branch_name} Branch*\n\n"
    text += "अब अपना *Semester* चुनें:\n\n"
    for i, sem in enumerate(available_semesters, 1):
        text += f"{i}. {sem}\n"
    return text

def format_time(timestamp) -> str:
    """Format datetime for display"""
    return timestamp.strftime('%d %b %Y, %I:%M %p')

def get_command_stats_text(command_stats: dict) -> str:
    """Format command statistics"""
    text = "📈 *Command Usage:*\n"
    for cmd, count in sorted(command_stats.items(), key=lambda x: x[1], reverse=True)[:10]:
        text += f"• /{cmd}: {count}\n"
    return text