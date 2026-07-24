"""
bot.py
Entry point for @DocTranslatorsBot. Run locally with `python bot.py`
(after setting BOT_TOKEN in a .env file), or deploy it on Railway --
see README.md for the full walkthrough.

Uses long polling rather than webhooks: simpler to run on Railway since
there's no public HTTPS endpoint to configure.
"""

import logging

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

from config import BOT_TOKEN
from handlers.start import start_command, help_command, status_command
from handlers.setlang import setlang_command, setlang_callback
from handlers.document import document_handler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CommandHandler("setlang", setlang_command))
    app.add_handler(CallbackQueryHandler(setlang_callback, pattern=r"^setlang:"))
    app.add_handler(MessageHandler(filters.Document.ALL, document_handler))

    logger.info("Bot starting (polling)...")
    app.run_polling(allowed_updates=["message", "callback_query"])


if __name__ == "__main__":
    main()
