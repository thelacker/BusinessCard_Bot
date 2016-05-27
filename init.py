from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
import telegram
import logging
from TOKEN import TOKEN
from models import TelegramUser
from uuid import uuid4
import json

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    telegramuser, created = TelegramUser.get_or_create(chat_id = update.message.chat_id)
    telegramuser.state = "main"
    telegramuser.save()
    KEYBOARD = [["Создать визитку"],["Посмотреть визитку"]]
    reply_markup = telegram.ReplyKeyboardMarkup(KEYBOARD)
    bot.sendMessage(update.message.chat_id, reply_markup = reply_markup, text='Hi!')


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')

def getcard(chat_id):
    telegramuser, created = TelegramUser.get_or_create(chat_id=chat_id)
    card = "\n<b>Имя:</b>\n" + str(telegramuser.first_name) + "\n<i>Адрес:</i>\n" + str(telegramuser.address)
    return card


def message(bot, update):
    telegramuser, created = TelegramUser.get_or_create(chat_id=update.message.chat_id)
    state = telegramuser.state

    if state == "main":
        if update.message.text == "Создать визитку":
            telegramuser.state = "question1"
            telegramuser.save()
            bot.sendMessage(update.message.chat_id, reply_markup = telegram.ReplyKeyboardHide(), text="Как Вас зовут?")
            return

        elif update.message.text == "Посмотреть визитку":
            telegramuser.state = "main"
            telegramuser.save()
            bot.sendMessage(update.message.chat_id, text=getcard(update.message.chat_id), parse_mode='HTML')
            return
        else:
            bot.sendMessage(update.message.chat_id, text="Я вас не понял")

    if state == "question1":
        telegramuser.state = "question2"
        telegramuser.first_name = update.message.text
        telegramuser.save()
        bot.sendMessage(update.message.chat_id, text="Какой Ваш адрес?")

    if state == "question2":
        telegramuser.state = "main"
        telegramuser.address = update.message.text
        telegramuser.save()
        KEYBOARD = [["Создать визитку"], ["Посмотреть визитку"]]
        reply_markup = telegram.ReplyKeyboardMarkup(KEYBOARD)
        bot.sendMessage(update.message.chat_id, reply_markup=reply_markup, text="Визитка сохранена!")

def inlinequery(bot, update):
    query = update.inline_query.query
    print (update.inline_query.from_user.id)
    results = list()

    results.append(InlineQueryResultArticle(id=uuid4(),
                                            title="Му Card",
                                            input_message_content=InputTextMessageContent(
                                                query + getcard(update.inline_query.from_user.id))))

    bot.answerInlineQuery(update.inline_query.id, results=results)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.addHandler(CommandHandler("start", start))
    dp.addHandler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.addHandler(MessageHandler([Filters.text], message))

    dp.addHandler(InlineQueryHandler(inlinequery))

    # log all errors
    dp.addErrorHandler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()