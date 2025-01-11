import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Регулярное выражение для проверки ссылок
URL_REGEX = re.compile(r'https?://[^\s]+')

# Функция для удаления сообщений с ссылками от не админов
async def delete_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = update.message.text
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id

    # Проверка, является ли пользователь администратором
    chat_member = await context.bot.get_chat_member(chat_id, user_id)
    if chat_member.status in ['administrator', 'creator']:
        return  # Если пользователь администратор, ничего не делаем

    if URL_REGEX.search(message_text):
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)
        except Exception as e:
            print(f"Ошибка при удалении сообщения: {e}")

# Функция для начала работы бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Я бот, который удаляет ссылки от не админов!")

def main() -> None:
    # Замените 'YOUR_TOKEN' на токен вашего бота
    application = ApplicationBuilder().token("7736458841:AAHaowvjBa4f0JtgXrOim-xMhwujmcnWUhY").build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, delete_link))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
