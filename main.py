from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config.config import BOT_TOKEN
from handlers.start import start_command
from handlers.book import BookHandler

def main():
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()

    # Initialize handlers
    book_handler = BookHandler()

    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", start_command))
    application.add_handler(CommandHandler("list", book_handler.list_books))
    application.add_handler(CommandHandler("get", book_handler.get_book))
    application.add_handler(CommandHandler("delete", book_handler.delete_book))

    # Add message handlers
    application.add_handler(MessageHandler(filters.Document.PDF, book_handler.handle_pdf))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
