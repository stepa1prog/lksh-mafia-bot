from pathlib import Path
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import bot.messages as messages


def read_token() -> str:
    with (Path(__file__).parent / 'token.txt').open() as f:
        return f.readline()


def help_handler(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    full_name = user.first_name + (' ' + user.last_name if user.last_name is not None else '')
    update.message.reply_text(messages.HELP.format(full_name=full_name))


def create_handler(update: Update, context: CallbackContext) -> None:
    pass


def join_handler(update: Update, context: CallbackContext) -> None:
    pass


def main() -> None:
    token = read_token()
    updater = Updater(token)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler(['start', 'help'], help_handler))
    dispatcher.add_handler(CommandHandler('create', create_handler))
    dispatcher.add_handler(CommandHandler('join', join_handler))

    updater.start_polling()
    updater.idle()
