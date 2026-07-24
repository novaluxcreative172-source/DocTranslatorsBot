"""
config.py
Loads configuration from environment variables (.env locally, or Railway's
'Variables' tab in production). Nothing else in the project should read
os.environ directly -- import from here instead.
"""

import os
from dotenv import load_dotenv

load_dotenv()  # no-op on Railway, but useful for local development

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN is not set. Add it to a local .env file, "
        "or as a Variable in your Railway project settings."
    )

DEFAULT_TARGET_LANG = os.getenv("DEFAULT_TARGET_LANG", "en")

# Telegram limits file downloads to 20 MB for bots.
MAX_FILE_SIZE_BYTES = 20 * 1024 * 1024

# Where translated files are temporarily written before being sent back.
TEMP_DIR = os.getenv("TEMP_DIR", "tmp_files")

# Path to the sqlite DB storing each user's preferred target language.
DB_PATH = os.getenv("DB_PATH", "user_settings.db")
