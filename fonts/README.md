# fonts/

Drop a Unicode `.ttf` font here named **DejaVuSans.ttf** to enable full
Unicode support (Arabic, Chinese, Japanese, Korean, Russian, Hindi, etc)
in translated PDF output.

Without it, PDF translation still works, but falls back to a core Latin-1
font -- fine for English/French/Spanish/German/Portuguese/Italian/etc,
but characters outside that range will be dropped.

Good free options:
- DejaVu Sans: https://dejavu-fonts.github.io/ (good general coverage)
- Noto Sans: https://fonts.google.com/noto (best for CJK + Arabic + Indic scripts)

Just download the `.ttf` and commit it to this folder as `DejaVuSans.ttf`
(or edit `UNICODE_FONT_PATH` in `processors/pdf_processor.py` to match
whatever filename you use).
