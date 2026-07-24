"""
languages.py
A curated list of languages shown in the /setlang inline keyboard, plus a
helper to validate a raw code typed by the user (e.g. /setlang pt-PT).
The underlying translator (Google via deep-translator) supports far more
than this list -- this is just what we surface as quick-pick buttons.
"""

# code -> display label
LANGUAGES = {
    "en": "English",
    "fr": "French",
    "es": "Spanish",
    "de": "German",
    "pt": "Portuguese",
    "it": "Italian",
    "ru": "Russian",
    "ar": "Arabic",
    "zh-CN": "Chinese (Simplified)",
    "ja": "Japanese",
    "ko": "Korean",
    "hi": "Hindi",
    "tr": "Turkish",
    "nl": "Dutch",
    "pl": "Polish",
    "sw": "Swahili",
    "yo": "Yoruba",
    "ha": "Hausa",
    "ig": "Igbo",
}


def is_supported(code: str) -> bool:
    """
    Accept anything in our curated list, and also let power users pass
    any code deep-translator understands (validated lazily at translate
    time, since deep-translator's full list is large and changes rarely).
    """
    return bool(code) and len(code) <= 10
