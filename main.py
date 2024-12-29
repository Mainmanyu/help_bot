# main.py

import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from config.config import TOKEN
from database.db import create_connection, create_table, insert_request
from faq.faq import FAQ

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Создание базы данных
conn = create_connection("support_bot.db")
create_table(conn)

# Команда /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "👋 Привет! Я бот техподдержки интернет-магазина 'Продаем все на свете'. Задайте свой вопрос или выберите один из часто задаваемых вопросов.",
        reply_markup=ForceReply(selective=True)
    )

# Обработка текстовых сообщений
def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    user_id = update.message.from_user.id

    # Проверка на наличие FAQ
    if user_message in FAQ:
        answer = FAQ[user_message]
        update.message.reply_text(answer)
    else:
        # Сохранение запроса в базе данных
                department = "sales" if "товар" in user_message else "programmers"
        insert_request(conn, user_id, user_message, department)
        update.message.reply_text(
            "Ваш запрос был записан. Мы свяжемся с вами в ближайшее время."
        )

def main():
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
