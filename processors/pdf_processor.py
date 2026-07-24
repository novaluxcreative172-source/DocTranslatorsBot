"""
processors/pdf_processor.py
PDFs don't have an easy "edit text in place" API the way docx/pptx do --
a PDF is really a page of positioned drawing instructions, not paragraphs.
So the approach here (same one most document-translator bots use) is:

  1. Extract text per page with pdfplumber.
  2. Translate each paragraph.
  3. Rebuild a fresh, cleanly laid-out PDF with the translated text.

This means exact original layout (columns, image placement, custom fonts)
is NOT preserved -- you get a readable translated document, not a
pixel-identical clone. That trade-off is called out to the user in the
bot's reply caption (see handlers/document.py).

Unicode note: the bundled core font (Helvetica) only covers Latin-1
languages (English, French, Spanish, German, Portuguese, etc). For
Arabic, Chinese, Japanese, Korean, Russian, Hindi, etc, drop a Unicode
TTF (e.g. DejaVuSans.ttf, or Noto Sans for full CJK/Arabic coverage)
into the fonts/ folder -- the code below picks it up automatically.
"""

import os
import pdfplumber
from fpdf import FPDF

from translator import translate_text

FONTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fonts")
UNICODE_FONT_PATH = os.path.join(FONTS_DIR, "DejaVuSans.ttf")


def _build_pdf() -> FPDF:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    if os.path.exists(UNICODE_FONT_PATH):
        pdf.add_font("DejaVu", "", UNICODE_FONT_PATH, uni=True)
        pdf.set_font("DejaVu", size=12)
    else:
        # Falls back to a core font: fine for Western European languages,
        # will drop unsupported characters for scripts like Arabic/CJK.
        pdf.set_font("Helvetica", size=12)

    return pdf


def process(input_path: str, output_path: str, target_lang: str) -> None:
    pdf = _build_pdf()

    with pdfplumber.open(input_path) as src:
        for page in src.pages:
            pdf.add_page()
            text = page.extract_text() or ""
            if not text.strip():
                pdf.multi_cell(0, 8, "[No extractable text on this page -- "
                                      "it may be a scanned image.]")
                continue

            for paragraph in text.split("\n"):
                if paragraph.strip():
                    translated = translate_text(paragraph, target_lang)
                    pdf.multi_cell(0, 8, translated)
                else:
                    pdf.ln(4)

    pdf.output(output_path)
