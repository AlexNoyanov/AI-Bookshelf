import os
import sys
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from datetime import datetime

from handlers.chat_handler import chat_command


# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Add the project root to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from handlers.start import start_command, help_command, list_command
from utils.db import Database

from handlers.chat_handler import chat_command


# Load environment variables
load_dotenv()

class PDFHandler:
    def __init__(self, db):
        self.db = db

    async def handle_pdf(self, update: Update, context):
        try:
            file = update.message.document
            user = update.effective_user
            
            # First, ensure user is in database
            self.db.insert_user(
                user_id=user.id,
                username=user.username
            )
            
            # Then save the book
            book_id = self.db.insert_book(
                user_id=user.id,
                book_name=file.file_name,
                file_id=file.file_id,
                file_size=file.file_size
            )
            
            await update.message.reply_text(
                f"📚 Received your PDF: {file.file_name}\n"
                f"Size: {file.file_size} bytes\n"
                f"Successfully saved to database!"
            )

        except Exception as e:
            logger.error(f"Error handling PDF: {e}")
            await update.message.reply_text("Sorry, there was an error processing your PDF.")
            raise

def run_bot():
    """Run the bot."""
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        raise ValueError("No token found in environment variables!")
    
    logger.info("Token loaded successfully")

    # Initialize database
    db = Database()
    
    # Create PDF handler
    pdf_handler = PDFHandler(db)

    # Create application
    app = Application.builder().token(token).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("list", list_command))
    app.add_handler(CommandHandler("chat", chat_command))
    app.add_handler(MessageHandler(filters.Document.PDF, pdf_handler.handle_pdf))
    
    # Store database instance in bot_data
    app.bot_data['db'] = db

    logger.info("Bot is starting...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    try:
        run_bot()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error running bot: {e}")
        sys.exit(1)
