import telebot

TOKEN = "8044674232:AAFc9Fa31bTyx0L405YGQwI3YYvmvIccguo"
bot = telebot.TeleBot(TOKEN)

print("🚀 Бот запущен!")

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "🌍 **МФЦ ДЛЯ ПУТЕШЕСТВИЙ** работает! ✅")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Получил: {message.text}")

print("✅ Готов!")
bot.infinity_polling()
