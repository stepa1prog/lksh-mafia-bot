from bot.create import create_game
from bot.join import join_game
from bot.state import *
from pathlib import Path
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import bot.messages as messages


def read_token() -> str:
    with (Path(__file__).parent / 'token.txt').open() as f:
        return f.readline()


def help_handler(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    full_name = user.first_name + (' ' + user.last_name if user.last_name is not None else '')
    update.message.reply_text(messages.HELP.format(full_name=full_name))


def create_handler(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    user = state.get_user(user_id)

    if user.status == UserStatus.CREATING:
        update.message.reply_text(messages.ALREADY_CREATING)
        return

    if user.status in (UserStatus.JOINING, UserStatus.JOINED):
        user.clear_status()

    user.status = UserStatus.CREATING
    update.message.reply_text(messages.CREATE_HELP)


def join_handler(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    user = state.get_user(user_id)

    if user.status in (UserStatus.JOINING, UserStatus.JOINED):
        user.clear_status()

    if user.status == UserStatus.CREATING:
        user.creating_game = None

    user.status = UserStatus.JOINING
    update.message.reply_text(messages.JOIN_HELP)


def text_handler(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    user = state.get_user(user_id)

    if user.status == UserStatus.CREATING:
        create_game(update, update.message.text, user)
    elif user.status == UserStatus.JOINING:
        join_game(update, update.message.text, user)
    else:
        help_handler(update, context)


def main() -> None:
    token = read_token()
    updater = Updater(token)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler(['start', 'help'], help_handler))
    dispatcher.add_handler(CommandHandler('create', create_handler))
    dispatcher.add_handler(CommandHandler('join', join_handler))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, text_handler))

    updater.start_polling()
    updater.idle()
