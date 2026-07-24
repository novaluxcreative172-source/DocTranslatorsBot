"""
handlers/setlang.py
/setlang shows an inline keyboard of common languages. Power users can
also type /setlang <code> directly (e.g. /setlang pt-PT) for anything
the curated list doesn't cover.
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from languages import LANGUAGES, is_supported
from storage import set_target_lang

_CALLBACK_PREFIX = "setlang:"


def _build_keyboard() -> InlineKeyboardMarkup:
    items = list(LANGUAGES.items())
    rows = []
    for i in range(0, len(items), 2):
        row = []
        for code, name in items[i:i + 2]:
            row.append(InlineKeyboardButton(name, callback_data=f"{_CALLBACK_PREFIX}{code}"))
        rows.append(row)
    return InlineKeyboardMarkup(rows)


async def setlang_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # /setlang <code> -- direct text entry
    if context.args:
        code = context.args[0]
        if is_supported(code):
            set_target_lang(update.effective_user.id, code)
            await update.message.reply_text(f"Target language set to `{code}`.", parse_mode="Markdown")
        else:
            await update.message.reply_text("That doesn't look like a valid language code.")
        return

    # Otherwise show the picker
    await update.message.reply_text(
        "Choose your target language:", reply_markup=_build_keyboard()
    )


async def setlang_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    code = query.data.removeprefix(_CALLBACK_PREFIX)
    set_target_lang(query.from_user.id, code)

    lang_name = LANGUAGES.get(code, code)
    await query.edit_message_text(f"\u2705 Target language set to *{lang_name}*.", parse_mode="Markdown")
