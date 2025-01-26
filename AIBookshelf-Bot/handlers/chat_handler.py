import logging
import aiohttp
from telegram import Update
from telegram.constants import ChatAction  # Changed import
from telegram.ext import ContextTypes, CommandHandler

logger = logging.getLogger(__name__)

GPT4ALL_API_BASE = "http://localhost:4891/v1"
DEFAULT_MODEL = "gpt4all-j-v1.3-groovy"

async def chat_with_gpt4all(message: str) -> str:
    """Send a chat request to GPT4ALL API"""
    payload = {
        "messages": [
            {"role": "user", "content": message}
        ],
        "model": DEFAULT_MODEL,
        "temperature": 0.7,
        "max_tokens": 500,
        "stream": False
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{GPT4ALL_API_BASE}/chat/completions",
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return result["choices"][0]["message"]["content"]
                else:
                    error_text = await response.text()
                    logger.error(f"GPT4ALL API error: {error_text}")
                    raise Exception(f"API request failed with status {response.status}")
    except Exception as e:
        logger.error(f"Error communicating with GPT4ALL: {e}")
        raise

async def chat_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /chat command"""
    user = update.effective_user
    message = update.message
    
    # Extract the text after the /chat command
    user_message = message.text.replace('/chat', '', 1).strip()
    
    if not user_message:
        await message.reply_text(
            "Please provide a message after /chat command.\n"
            "Example: /chat What books do you recommend?"
        )
        return

    try:
        logger.info(f"Chat request from user {user.id} ({user.username}): {user_message}")
        
        # Updated to use correct ChatAction syntax
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action=ChatAction.TYPING
        )
        
        response = await chat_with_gpt4all(user_message)
        
        if len(response) > 4000:
            chunks = [response[i:i+4000] for i in range(0, len(response), 4000)]
            for chunk in chunks:
                await message.reply_text(chunk)
        else:
            await message.reply_text(response)
        
        logger.info(f"Chat response sent to user {user.id}")
            
    except Exception as e:
        error_message = "Sorry, I couldn't process your request. Please try again later."
        logger.error(f"Error processing chat for user {user.id}: {str(e)}")
        await message.reply_text(error_message)
