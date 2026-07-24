"""
handlers/start.py
/start and /help -- onboarding messages.
"""

from telegram import Update
from telegram.ext import ContextTypes

from storage import get_target_lang
from languages import LANGUAGES

WELCOME = (
    "\U0001F44B Welcome to *Document Translator Bot*!\n\n"
    "Send me a document -- PDF, Word (.docx), PowerPoint (.pptx), Excel "
    "(.xlsx), or a plain .txt file -- and I'll translate its text and send "
    "the translated file back.\n\n"
    "Your current target language is *{lang}*.\n"
    "Use /setlang to change it, or /help to see everything I can do."
)

HELP = (
    "*Commands*\n"
    "/setlang -- choose the language I translate documents into\n"
    "/status -- see your current target language\n"
    "/help -- show this message\n\n"
    "*Supported files*\n"
    "PDF, DOCX, PPTX, XLSX, TXT (up to 20 MB, Telegram's bot file limit).\n\n"
    "*How it works*\n"
    "Source language is detected automatically. Just send a document and "
    "I'll reply with a translated copy. For PDFs, note that I rebuild a "
    "clean translated document rather than an exact pixel copy of the "
    "original layout."
)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang_code = get_target_lang(update.effective_user.id)
    lang_name = LANGUAGES.get(lang_code, lang_code)
    await update.message.reply_text(
        WELCOME.format(lang=lang_name), parse_mode="Markdown"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(HELP, parse_mode="Markdown")


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang_code = get_target_lang(update.effective_user.id)
    lang_name = LANGUAGES.get(lang_code, lang_code)
    await update.message.reply_text(
        f"Your documents are currently translated into *{lang_name}* "
        f"(`{lang_code}`). Use /setlang to change it.",
        parse_mode="Markdown",
    )
