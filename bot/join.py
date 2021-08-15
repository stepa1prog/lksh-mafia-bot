from bot.state import *
from telegram import Update


def join_game(update: Update, text: str, user: User) -> None:
    update.message.reply_text(f'join {text} {user}')
