import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# ID администратора (замените на ваш Telegram ID)
ADMIN_ID = 6834749644  # Вставьте ваш Telegram ID

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот для сбора обратной связи. Напиши мне свои пожелания, предложения или проблемы, и я передам их администратору."
    )

# Обработчик текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_info = f"Обратная связь от {user.full_name} (@{user.username}, ID: {user.id}):\n{update.message.text}"
    
    # Отправляем сообщение администратору
    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text=user_info)
        await update.message.reply_text("Спасибо за ваш отзыв! Он отправлен администратору.")
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения администратору: {e}")
        await update.message.reply_text("Произошла ошибка при отправке отзыва. Попробуйте позже.")

# Обработчик ошибок
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}")

def main():
    # Вставьте ваш токен бота, полученный от @BotFather
    TOKEN = "7594115219:AAGN5NGehuy_bzwCuD0iDzmO5ZVs5r9VrzY"  # Замените на ваш токен

    # Создаем приложение
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)

    # Запускаем бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()