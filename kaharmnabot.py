

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import schedule
import time
from datetime import datetime

API_TOKEN = '6971704916:AAEIi8HOL0gDfiHIMq5M26-o5iKw3LHpGBE'
CHANNEL_ID = '-1002194286114'  # Укажите ваш ID канала
bot = telebot.TeleBot(API_TOKEN)

# Словарь для отслеживания состояния кнопок
button_states = {
    "тренировка": False,
    "stepik": False,
    "unity": False,
    "база знаний": False,
    "реклама ватсап рассылки": False,
    "снять рилс видео": False,
    "пост инстаграм": False,
    "продвижения обучения рассылка": False,
    "создания сайтов лендинг": False,
    "создание инстаграм ботов рассылка": False,
    "indriver проверить заказы": False,
    "кворк сделать бота ": False,
    "сделать заказ для себя": False,
    "инстаграм аккаунты автоматизация": False,
    "попробывать upwork": False,
    "глобальный проект": False,
    "делать игровой проект": False
}
# Функция для создания клавиатуры
def create_keyboard():
    keyboard = InlineKeyboardMarkup()
    for key in button_states:
        emoji = "❌" if button_states[key] else ""
        button = InlineKeyboardButton(text=f"{key} {emoji}", callback_data=key)
        keyboard.add(button)
    return keyboard


# Отправка клавиатуры в канал утром
def morning_task():
    global button_states
    button_states = {key: False for key in button_states}  # Сброс состояния кнопок
    bot.send_message(CHANNEL_ID, "Выполни действие:", reply_markup=create_keyboard())
def half_hour_task():
    current_time = datetime.now().time()
    if current_time >= datetime.strptime("07:00", "%H:%M").time() and current_time < datetime.strptime("23:00","%H:%M").time():
        bot.send_message(CHANNEL_ID, "ты сделал пункт")

# Проверка состояния кнопок вечером
def evening_task():
    if all(button_states.values()):
        bot.send_message(CHANNEL_ID, "🏆 кахарман")
    else:
        bot.send_message(CHANNEL_ID, "катын")


# Запланировать задачи
schedule.every().day.at("11:19").do(morning_task)
schedule.every().day.at("23:00").do(evening_task)
schedule.every(30).minutes.do(half_hour_task)



# Обработчик команды /start



# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: call.data in button_states)
def handle_callback(call):
    # Переключаем состояние кнопки
    button_states[call.data] = not button_states[call.data]

    # Обновляем клавиатуру в канале
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=create_keyboard())


# Запуск планировщика и бота
def run_bot():
    while True:
        schedule.run_pending()
        time.sleep(1)


# Автоматический запуск бота и планировщика
if __name__ == "__main__":
    import threading

    bot_thread = threading.Thread(target=bot.polling, kwargs={"none_stop": True})
    bot_thread.start()

    run_bot()
