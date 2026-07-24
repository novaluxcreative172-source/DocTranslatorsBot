"""
translator.py
Single point of contact with the translation engine. Everything else in
the project calls translate_text() -- if you ever swap Google for DeepL
or LibreTranslate, this is the only file you need to touch.
"""

import time
import logging
from deep_translator import GoogleTranslator
from deep_translator.exceptions import RequestError, TranslationNotFound

logger = logging.getLogger(__name__)

# GoogleTranslator (via deep-translator) caps requests around 5000 chars.
# We chunk conservatively below that so we never hit the limit mid-sentence.
MAX_CHUNK_CHARS = 4500
MAX_RETRIES = 3


def _chunk_text(text: str, max_chars: int = MAX_CHUNK_CHARS):
    """Split on paragraph/sentence boundaries so translation quality holds up."""
    if len(text) <= max_chars:
        yield text
        return

    parts = text.split("\n")
    buffer = ""
    for part in parts:
        candidate = f"{buffer}\n{part}" if buffer else part
        if len(candidate) > max_chars:
            if buffer:
                yield buffer
            buffer = part
        else:
            buffer = candidate
    if buffer:
        yield buffer


def translate_text(text: str, target_lang: str, source_lang: str = "auto") -> str:
    """
    Translate a single string. Empty/whitespace-only input is returned as-is
    (no point spending an API call translating blank cells/lines).
    """
    if not text or not text.strip():
        return text

    translated_chunks = []
    for chunk in _chunk_text(text):
        translated_chunks.append(_translate_with_retry(chunk, target_lang, source_lang))
    return "\n".join(translated_chunks) if len(translated_chunks) > 1 else translated_chunks[0]


def _translate_with_retry(chunk: str, target_lang: str, source_lang: str) -> str:
    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            translator = GoogleTranslator(source=source_lang, target=target_lang)
            return translator.translate(chunk)
        except (RequestError, TranslationNotFound) as exc:
            last_error = exc
            logger.warning("Translation attempt %s failed: %s", attempt, exc)
            time.sleep(1.5 * attempt)  # simple backoff
        except Exception as exc:  # noqa: BLE001 - we want to retry on anything transient
            last_error = exc
            logger.warning("Unexpected translation error, attempt %s: %s", attempt, exc)
            time.sleep(1.5 * attempt)

    logger.error("Giving up translating chunk after %s attempts: %s", MAX_RETRIES, last_error)
    # Fail soft: return the original text rather than crashing the whole document.
    return chunk
