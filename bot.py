"""
Main bot file - Entry point for the AI Career Guidance Chatbot
Run this file to start the bot
"""

import asyncio
import logging
from pyrogram.client import Client
from pyrogram.errors import RPCError
from config import API_ID, API_HASH, BOT_TOKEN
from handlers import register_handlers
from db import get_db_status

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)



def main():
    """Main function to start the bot"""
    
    # Check database connection
    if not get_db_status():
        logger.error("❌ MongoDB connection failed! Please check your MONGO_URI in config.py")
        return
    
    logger.info("✅ MongoDB connection successful!")
    
    # Create Pyrogram client with optimized timeouts
    app = Client(
        "career_guidance_bot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        sleep_threshold=60,          # Reduce flood wait sleep time
        workers=8,                   # Increase concurrent workers
        max_concurrent_transmissions=2  # Optimize concurrent transmissions
    )
    
    # Register all handlers
    register_handlers(app)
    
    # Start the bot
    try:
        logger.info("🚀 Starting AI Career Guidance Chatbot...")
        app.run()
    except RPCError as e:
        logger.error(f"❌ Telegram API error: {e}")
        logger.error("Please check your API_ID, API_HASH, and BOT_TOKEN in config.py")
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
