
from telegram import Update
from telegram.ext import ContextTypes

async def command_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! 👋 I am your Telegram bot."
    )