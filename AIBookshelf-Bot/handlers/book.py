from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from models.book import Book
import os

class BookHandler:
    def __init__(self):
        self.book_model = Book()

    async def handle_pdf(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle PDF file uploads"""
        if not update.message.document.file_name.lower().endswith('.pdf'):
            await update.message.reply_text("Please send only PDF files.")
            return

        try:
            file = update.message.document
            user_id = update.effective_user.id
            
            # Add book to database
            self.book_model.add_book(
                user_id=user_id,
                book_name=file.file_name,
                file_id=file.file_id,
                file_size=file.file_size
            )

            await update.message.reply_text(
                f"📚 Book '{file.file_name}' has been added to your library!"
            )

        except Exception as e:
            await update.message.reply_text(
                "Sorry, there was an error processing your book. Please try again."
            )
            raise e

    async def list_books(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """List all books for the user"""
        user_id = update.effective_user.id
        books = self.book_model.get_user_books(user_id)

        if not books:
            await update.message.reply_text("Your library is empty. Send me PDF files to add books!")
            return

        message = "📚 Your Books:\n\n"
        for book in books:
            message += f"📖 {book['book_name']}\n"
            if book['title'] or book['author']:
                message += f"   Title: {book['title'] or 'N/A'}\n"
                message += f"   Author: {book['author'] or 'N/A'}\n"
            message += "\n"

        # Add pagination if the message is too long
        if len(message) > 4096:
            chunks = [message[i:i+4096] for i in range(0, len(message), 4096)]
            for chunk in chunks:
                await update.message.reply_text(chunk)
        else:
            await update.message.reply_text(message)

    async def get_book(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Download a specific book"""
        if not context.args:
            await update.message.reply_text("Please provide the book ID.")
            return

        try:
            book_id = int(context.args[0])
            book = self.book_model.get_book(book_id, update.effective_user.id)

            if not book:
                await update.message.reply_text("Book not found.")
                return

            await update.message.reply_document(book['file_id'])

        except ValueError:
            await update.message.reply_text("Invalid book ID.")
        except Exception as e:
            await update.message.reply_text("Error retrieving the book.")
            raise e

    async def delete_book(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Delete a book"""
        if not context.args:
            await update.message.reply_text("Please provide the book ID.")
            return

        try:
            book_id = int(context.args[0])
            if self.book_model.delete_book(book_id, update.effective_user.id):
                await update.message.reply_text("Book has been deleted.")
            else:
                await update.message.reply_text("Book not found.")

        except ValueError:
            await update.message.reply_text("Invalid book ID.")
        except Exception as e:
            await update.message.reply_text("Error deleting the book.")
            raise e
