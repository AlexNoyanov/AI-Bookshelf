from telegram import Update
from telegram.ext import ContextTypes
from models.user import User

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = User()
    user.create_user(
        user_id=update.effective_user.id,
        username=update.effective_user.username
    )
    
    welcome_text = (
        "Welcome to AI Bookshelf! 📚\n\n"
        "Commands:\n"
        "/add - Add a new book (send PDF)\n"
        "/list - View your books\n"
        "/categories - Manage categories\n"
        "/help - Show this help message"
    )
    await update.message.reply_text(welcome_text)
