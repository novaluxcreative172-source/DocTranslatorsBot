"""
processors/txt_processor.py
Translates a .txt file line by line so paragraph breaks are preserved.
"""

from translator import translate_text


def process(input_path: str, output_path: str, target_lang: str) -> None:
    with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    translated_lines = []
    for line in lines:
        stripped = line.rstrip("\n")
        if stripped.strip():
            translated_lines.append(translate_text(stripped, target_lang))
        else:
            translated_lines.append(stripped)  # keep blank lines as spacing

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(translated_lines))
