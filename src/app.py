import os
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    ConversationHandler
)

async def command_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! 👋 I am your Telegram bot."
    )


async def command_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show help"
    )

async def command_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Quiz command is not yet implemented."
    )
    
# menu_conv = ConversationHandler(
#     entry_points=[CommandHandler("menu", menu_start)],
#     states={
#         MenuStates.WAIT_INPUT_TYPE: [
#             CallbackQueryHandler(input_type_selected),
#         ],
#         MenuStates.WAIT_MENU_CONTENT: [
#             MessageHandler(filters.PHOTO, handle_menu_image),
#             MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_text),
#         ],
#         MenuStates.SHOW_RESULTS: [
#             CallbackQueryHandler(scan_again),
#         ],
#     },
#     fallbacks=[CommandHandler("cancel", cancel_menu)],
# )


def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", command_start))
    app.add_handler(CommandHandler("help", command_help))
    app.add_handler(CommandHandler("quiz", command_quiz))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()