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
        "/help - Show this help message\n"
         "/chat - Send message to AI"
    )
    await update.message.reply_text(welcome_text)

async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db = context.bot_data.get('db')
    
    if not db:
        await update.message.reply_text("Sorry, database is not available.")
        return

    books = db.get_user_books(user_id)
    
    if not books:
        await update.message.reply_text("You haven't uploaded any books yet!")
        return

    response = "📚 Your uploaded books:\n\n"
    for book in books:
        response += f"📖 {book['book_name']}\n"
        if book['title'] or book['author']:
            response += f"   Title: {book['title'] or 'N/A'}\n"
            response += f"   Author: {book['author'] or 'N/A'}\n"
        if book['categories']:
            response += f"   Categories: {book['categories']}\n"
        response += f"   Uploaded: {book['uploaded_at']}\n\n"
    
    await update.message.reply_text(response)
