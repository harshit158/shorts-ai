from src.quiz import generate_quiz
from src.settings import settings
from src.logging_setup import get_logger

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)

from src.agents.quiz_agent import quiz_agent
from src.scraper import Scraper
from src.bot import handlers

logger = get_logger(__name__)

async def command_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show help"
    )

async def command_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Received /quiz command from user")
    
    # Set state to wait for URL
    context.user_data['waiting_for_url'] = True
    
    await update.message.reply_text(
        "📎 Please share the URL you want to create a quiz from:"
    )

async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Check if we're waiting for a URL
    if not context.user_data.get('waiting_for_url'):
        return
    
    url = update.message.text
    context.user_data['waiting_for_url'] = False
    
    await update.message.reply_text(
        "⏳ Generating a quiz question for you..."
    )
    
    try:
        logger.info("Received URL: %s", url)
        scraped_content = Scraper().scrape(url)
        logger.info("Scraped content length: %d characters", len(scraped_content))
        logger.info("Invoking quiz agent with scraped content")
        quiz_str = "\n\n".join(quiz_agent.invoke({"context": scraped_content})["questions"])
        
        await update.message.reply_text(
            quiz_str,
            parse_mode="HTML"
        )
    except Exception as e:
        await update.message.reply_text(
            f"❌ Error generating quiz: {str(e)}"
        )

def log_app_settings():
    logger.info("Application Settings:")
    logger.info(f"Telegram Bot Token: {'SET' if settings.telegram_bot_token else 'NOT SET'}")
    
def main():
    app = ApplicationBuilder().token(settings.telegram_bot_token).build()

    app.add_handler(CommandHandler("start", handlers.command_start))
    app.add_handler(CommandHandler("help", command_help))
    app.add_handler(CommandHandler("quiz", command_quiz))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url))

    log_app_settings()
    app.run_polling()


if __name__ == "__main__":
    main()