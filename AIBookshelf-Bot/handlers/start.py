from telegram import Update
from telegram.ext import ContextTypes

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👋 Welcome to AI Bookshelf!\n\n"
        "I can help you manage and analyze your PDF documents.\n\n"
        "Commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/list - Show your uploaded books\n\n"
        "Simply send me any PDF file to get started!"
    )
    await update.message.reply_text(welcome_text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "📚 AI Bookshelf Help\n\n"
        "How to use:\n"
        "1. Send any PDF file\n"
        "2. I'll save and process it\n"
        "3. Use /list to see your uploads\n\n"
        "Commands:\n"
        "/start - Restart the bot\n"
        "/help - Show this help\n"
        "/list - Show your books"
    )
    await update.message.reply_text(help_text)

async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    db = context.bot_data.get('db')
    
    if not db:
        await update.message.reply_text("Sorry, database is not available.")
        return

    books = db.get_user_books(user_id)  # Changed from get_user_pdfs to get_user_books
    
    if not books:
        await update.message.reply_text("You haven't uploaded any books yet!")
        return

    response = "📚 Your uploaded books:\n\n"
    for book in books:
        response += f"📖 {book['book_name']}\n"
        if book.get('title') or book.get('author'):
            response += f"   Title: {book.get('title') or 'N/A'}\n"
            response += f"   Author: {book.get('author') or 'N/A'}\n"
        if book.get('categories'):
            response += f"   Categories: {book.get('categories')}\n"
        response += f"   Uploaded: {book['uploaded_at']}\n\n"
    
    # If response is too long, split it into multiple messages
    if len(response) > 4096:
        parts = [response[i:i+4096] for i in range(0, len(response), 4096)]
        for part in parts:
            await update.message.reply_text(part)
    else:
        await update.message.reply_text(response)
