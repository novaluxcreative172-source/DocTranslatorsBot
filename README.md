# @DocTranslatorsBot

A Telegram bot that translates uploaded documents (PDF, Word, PowerPoint,
Excel, TXT) and sends back a translated copy. Source language is
auto-detected; target language is set per-user with `/setlang`.

Translation engine: Google Translate (via the free `deep-translator` library,
no API key required).

## 1. Create the bot on Telegram
1. Message **@BotFather**, send `/newbot`, name it so its username is `DocTranslatorsBot`.
2. Copy the token it gives you — you'll paste it into Railway as `BOT_TOKEN`.

## 2. Push to GitHub
Create every file above in a new repo (via GitHub's "Add file" button, or `git add . && git commit && git push`).
Never commit a real token — `.env` is already git-ignored.

## 3. Deploy on Railway
1. railway.app -> New Project -> Deploy from GitHub repo -> select this repo.
2. Variables tab -> add `BOT_TOKEN` (and optionally `DEFAULT_TARGET_LANG`).
3. Railway reads the `Procfile` and runs `python bot.py` as a worker.
4. Check Logs for "Bot starting (polling)..." then message the bot on Telegram.

Note: Railway's filesystem resets on redeploy, so `user_settings.db`
(each user's `/setlang` choice) resets too unless you move to Postgres.
