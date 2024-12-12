import telebot
from gradio_client import Client

# Инициализация клиента Gradio
client = Client("llamameta/Qwen2.5-Coder-32B-Instruct-Chat-Assistant")

# Стартовое системное сообщение
system_message = "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."
chat_history = []  # Хранение истории сообщений

# Токен Telegram-бота
TOKEN = "7294243811:AAHvsInC5_JV_K87pzUiTU4G0Z6HW-wrnu4"
bot = telebot.TeleBot(TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я ваш помощник. Напишите мне что-нибудь.")

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_message = message.text
    chat_history.append({"role": "user", "content": user_message})

    try:
        # Отправка запроса к модели
        result = client.predict(
            message=user_message,
            system_message=system_message,
            max_tokens=1000,
            temperature=0.7,
            top_p=0.8,
            api_name="/chat"
        )
        # Отправка ответа пользователю
        bot.reply_to(message, result)
        chat_history.append({"role": "assistant", "content": result})
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

# Запуск бота
if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling()
