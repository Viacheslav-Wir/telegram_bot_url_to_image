import os
import re
import html
import json
import logging
import requests
import traceback

from telegram import (Update, ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, CallbackContext, MessageHandler, 
                          Filters, ConversationHandler)
from dotenv import load_dotenv
from os import listdir
from os.path import isfile, join

from utils import get_screenshot, show_file_names

load_dotenv()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

PROCESS = range(1)
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/53 7.36'}
URL_CHECK = "^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$"


def start(update, context):
    update.message.reply_text(
    	"Hi! I will help you to take a webpage screenshot.\n"
        "Please insert the URL to get a screenshot.\n"
        "Send /cancel to stop talking to me.",)

    return PROCESS


def send_request(update, context):
    url = update.message.text
    match = re.match(URL_CHECK, url)
    if match:
        r = requests.get(url=url, headers=HEADERS)
        if r.status_code == 200:
            update.message.reply_text("Your URL is being processed. Wait please.")

            status, image_path = get_screenshot(url)
            if status:
                # if show_file_names():
                #     reply_keyboard = [['List of all files']]
                context.bot.send_document(chat_id=update.message.chat.id, document=open('{}'.format(image_path), 'rb'))
                # context.bot.send_document(chat_id=update.message.chat.id, document=open('{}'.format(image_path), 'rb'), reply_markup = ReplyKeyboardRemove())
                # context.bot.send_document(chat_id=update.message.chat.id, document=open('{}'.format(image_path), 'rb'), reply_markup=ReplyKeyboardMarkup(reply_keyboard))
            else:
                context.bot.send_message("Some troubles happen. Try another URL.")
        else:
            update.message.reply_text("Some troubles happen. Requests error code {}.".fromat(r.status_code))
    else:
        if url == '/cancel':
            cancel(update, context)
        else:
            update.message.reply_text("Url is inccorect. Place full URL e.g.: 'https://dou.ua/'.")


# def echo(update, context):
#     """Echo the user message."""
#     update.message.reply_text(update.message.text)


def error_handler(update: Update, context: CallbackContext):
    dev_chat_id = os.getenv("DEVELOPER_CHAT_ID")

    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb = ''.join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    message = (
        'An exception was raised while handling an update\n'
        '<pre>update = {}</pre>\n\n'
        '<pre>context.chat_data = {}</pre>\n\n'
        '<pre>context.user_data = {}</pre>\n\n'
        '<pre>{}</pre>'
    ).format(
        html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False)),
        html.escape(str(context.chat_data)),
        html.escape(str(context.user_data)),
        html.escape(tb)
    )

    # Finally, send the message
    context.bot.send_message(chat_id=dev_chat_id, text=message, parse_mode=ParseMode.HTML)


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I may help again someday.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    updater = Updater(token, use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            PROCESS: [MessageHandler(Filters.text, send_request)],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)
    dp.add_error_handler(error_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()