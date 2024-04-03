from environment import OPENAI_API_KEY, BASE_URL, GPT_MODEL, TELEGRAM_TOKEN
import telebot
import re  # Импортируем модуль для работы с регулярными выражениями
from openai import OpenAI

# Замените 'YOUR_TOKEN_HERE' на токен, полученный от BotFather
bot = telebot.TeleBot(TELEGRAM_TOKEN)

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=BASE_URL,
)

chat_completion = client.chat.completions.create(
    model=GPT_MODEL, messages=[{"role": "user", "content": "Hello world"}]
)

messages = []

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я твой помощник. Напиши /help, чтобы узнать, что я умею.")

# Обработчик команды /help
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Список доступных команд:\n/start - начало работы с ботом\n/help - получить список команд\n/perevorot <текст> - переворачивает текст\n/caps <текст> - преобразовывает текст в заглавные буквы\n/cut <текст> - удаляет все гласные буквы из текста\n/count <текст> - подсчитывает число согласных букв из текста\n/chat <текст> - общение с ChatGPT")

# Обработчик команды /chat
@bot.message_handler(commands=['chat'])
def chat_text(message):
    try:
        bot.reply_to(message, "Думаю....")
        messages.append({"role": "user", "content": message.text})
        # Запрашиваем у нейросети ответ на введенное сообщение
        chat_completion = client.chat.completions.create(
            model=GPT_MODEL, messages=messages
        )
        # Получаем и выводим ответ от нейросети
        ai_response = chat_completion.choices[0].message.content
        # Добавляем ответ нейросети в список сообщений
        messages.append({"role": "assistant", "content": ai_response})
        bot.reply_to(message, ai_response)
    except IndexError:
        bot.reply_to(message, "Пожалуйста, введите текст после команды /chat. Например: /chat текст")

# Обработчик команды /count
@bot.message_handler(commands=['count'])
def count_consonants(message):
    try:
        text = message.text.split(" ", 1)[1]
        # Считаем согласные буквы
        consonants_count = sum(1 for letter in text if letter.lower() in 'bcdfghjklmnpqrstvwxyzбвгджзйклмнпрстфхцчшщ')
        bot.reply_to(message, f"Количество согласных букв в вашем сообщении: {consonants_count}")
    except IndexError:
        bot.reply_to(message, "Пожалуйста, введите текст после команды /count. Например: /count текст")

# Обработчик команды /perevorot
@bot.message_handler(commands=['perevorot'])
def perevorot_text(message):
    try:
        text = message.text.split(" ", 1)[1]
        bot.reply_to(message, text[::-1])
    except IndexError:
        bot.reply_to(message, "Пожалуйста, введите текст после команды /perevorot. Например: /perevorot текст")

# Обработчик команды /caps
@bot.message_handler(commands=['caps'])
def caps_text(message):
    try:
        text = message.text.split(" ", 1)[1]
        bot.reply_to(message, text.upper())
    except IndexError:
        bot.reply_to(message, "Пожалуйста, введите текст после команды /caps. Например: /caps текст")

# Обработчик команды /cut
@bot.message_handler(commands=['cut'])
def cut_text(message):
    try:
        text = message.text.split(" ", 1)[1]
        # Удаляем гласные буквы
        result = re.sub(r'[aeiouAEIOUаеёиоуыэюяАЕЁИОУЫЭЮЯ]', '', text)
        bot.reply_to(message, result)
    except IndexError:
        bot.reply_to(message, "Пожалуйста, введите текст после команды /cut. Например: /cut текст")

# Запускает бота для опроса серверов Telegram
bot.polling(none_stop=True)