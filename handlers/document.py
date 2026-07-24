"""
handlers/document.py
Handles incoming file uploads: figures out the file type, downloads it,
runs the matching processor from processors/, and sends the translated
file back to the user.
"""

import os
import uuid
import logging

from telegram import Update
from telegram.ext import ContextTypes

from config import MAX_FILE_SIZE_BYTES, TEMP_DIR
from storage import get_target_lang
from languages import LANGUAGES
from processors import (
    txt_processor,
    docx_processor,
    pptx_processor,
    xlsx_processor,
    pdf_processor,
)

logger = logging.getLogger(__name__)

PROCESSORS = {
    ".txt": txt_processor,
    ".docx": docx_processor,
    ".pptx": pptx_processor,
    ".xlsx": xlsx_processor,
    ".pdf": pdf_processor,
}

PDF_NOTE = (
    "\n\n_Note: PDFs are rebuilt as a clean translated document rather than "
    "an exact copy of the original layout._"
)


async def document_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    doc = update.message.document
    if doc is None:
        return

    filename = doc.file_name or "file"
    ext = os.path.splitext(filename)[1].lower()

    if ext not in PROCESSORS:
        supported = ", ".join(sorted(PROCESSORS.keys()))
        await update.message.reply_text(
            f"Sorry, I can't handle *{ext or 'that file type'}* yet.\n"
            f"Supported formats: {supported}",
            parse_mode="Markdown",
        )
        return

    if doc.file_size and doc.file_size > MAX_FILE_SIZE_BYTES:
        await update.message.reply_text(
            "That file is larger than Telegram's 20 MB bot limit -- "
            "please send a smaller file."
        )
        return

    user_id = update.effective_user.id
    target_lang = get_target_lang(user_id)
    lang_name = LANGUAGES.get(target_lang, target_lang)

    status_msg = await update.message.reply_text(
        f"Translating your document into *{lang_name}*... \u23F3",
        parse_mode="Markdown",
    )

    os.makedirs(TEMP_DIR, exist_ok=True)
    job_id = uuid.uuid4().hex
    input_path = os.path.join(TEMP_DIR, f"{job_id}_input{ext}")
    output_path = os.path.join(TEMP_DIR, f"{job_id}_translated{ext}")

    try:
        tg_file = await doc.get_file()
        await tg_file.download_to_drive(input_path)

        processor = PROCESSORS[ext]
        processor.process(input_path, output_path, target_lang)

        base_name = os.path.splitext(filename)[0]
        out_filename = f"{base_name}_{target_lang}{ext}"

        caption = f"Here's your document translated into {lang_name}."
        if ext == ".pdf":
            caption += PDF_NOTE

        with open(output_path, "rb") as f:
            await update.message.reply_document(
                document=f,
                filename=out_filename,
                caption=caption,
                parse_mode="Markdown",
            )
        await status_msg.delete()

    except Exception:
        logger.exception("Failed to process document %s", filename)
        await status_msg.edit_text(
            "Something went wrong translating that file. Please try again, "
            "or try a different file."
        )
    finally:
        for path in (input_path, output_path):
            if os.path.exists(path):
                os.remove(path)
