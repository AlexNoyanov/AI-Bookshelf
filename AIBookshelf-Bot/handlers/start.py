from telegram import Update
from telegram.ext import ContextTypes
from utils.db import Database
import logging

logger = logging.getLogger(__name__)

async def chat_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /chat command"""
    user = update.effective_user
    db = Database()
    
    try:
        # Check if there are any arguments provided
        if not context.args:
            db.log_user_activity(
                user_id=user.id,
                username=user.username,
                action_type='chat',
                message="No input provided"
            )
            await update.message.reply_text(
                "Please provide a message after /chat command.\n"
                "Example: /chat What is this book about?"
            )
            return

        # Get user's message
        user_message = ' '.join(context.args)
        
        # Log the chat command
        db.log_user_activity(
            user_id=user.id,
            username=user.username,
            action_type='chat',
            message=user_message
        )
        
        # Get user's books
        books = db.get_user_books(user.id)
        
        if not books:
            await update.message.reply_text(
                "You haven't uploaded any books yet. Please upload a PDF first!"
            )
            return
        
        # For now, just acknowledge the message
        response = (
            f"Received your message: {user_message}\n\n"
            f"You have {len(books)} books in your library.\n"
            "Chat functionality with your books is coming soon!"
        )
        
        await update.message.reply_text(response)
        
    except Exception as e:
        logger.error(f"Error in chat command: {e}")
        await update.message.reply_text(
            "Sorry, there was an error processing your request. Please try again later."
        )
    finally:
        db.close()

# You can keep these functions in the same file or move them to a separate file
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command"""
    user = update.effective_user
    db = Database()
    
    try:
        # Log the start command
        db.log_user_activity(
            user_id=user.id,
            username=user.username,
            action_type='command',
            message='/start'
        )
        
        await update.message.reply_text(
            "Welcome to AI Bookshelf Bot! I can help you manage and interact with your PDF books."
        )
    except Exception as e:
        print(f"Error in start command: {e}")
    finally:
        db.close()

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /help command"""
    user = update.effective_user
    db = Database()
    
    try:
        # Log the help command
        db.log_user_activity(
            user_id=user.id,
            username=user.username,
            action_type='command',
            message='/help'
        )
        
        help_text = """
Here are the available commands:

/start - Start the bot
/help - Show this help message
/list - List your uploaded books
/chat - Chat with your books
/logs - View your activity logs

You can also send me PDF files directly to upload them.
        """
        
        await update.message.reply_text(help_text)
    except Exception as e:
        print(f"Error in help command: {e}")
    finally:
        db.close()

async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /list command"""
    user = update.effective_user
    db = Database()
    
    try:
        # Log the list command
        db.log_user_activity(
            user_id=user.id,
            username=user.username,
            action_type='command',
            message='/list'
        )
        
        books = db.get_user_books(user.id)
        
        if not books:
            await update.message.reply_text("You haven't uploaded any books yet.")
            return
            
        response = "Your uploaded books:\n\n"
        for book in books:
            response += f"📚 {book['book_name']}\n"
            response += f"Size: {book['file_size']} bytes\n"
            response += f"Uploaded: {book['uploaded_at']}\n\n"
            
        await update.message.reply_text(response)
    except Exception as e:
        print(f"Error in list command: {e}")
    finally:
        db.close()
