import logging
from telegram.ext import Application, MessageHandler, filters,  CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from config import BOT_TOKEN


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)
spisok = []
reply_keyboard = [['/start']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)




async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    await update.message.reply_html(
        rf"Здравствуйте {user.mention_html()}! Я Бот, который задаст тебе пару вопросов для устройства на работу. Удачи!"
        rf"ПЕРВЫЙ ЭТАП: "
        rf"Назовите свои Фамилию Имя Отчество", reply_markup=ReplyKeyboardRemove()
    )


async def help(update, context):
    await update.message.reply_text("Чтобы начать нажмите /start", reply_markup=markup)


async def twoquest(update, context):
    spisok.append(update.message.text)
    await update.message.reply_text(f'Записал. {spisok[0]}')


def main():
    # Создаём объект Application.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    #application.add_handler(MessageHandler(filters.text, twoquest))
    # Создаём обработчик сообщений типа filters.TEXT
    # из описанной выше асинхронной функции echo()
    # После регистрации обработчика в приложении
    # эта асинхронная функция будет вызываться при получении сообщения
    # с типом "текст", т. е. текстовых сообщений.
    text_handler = MessageHandler(filters.TEXT, twoquest)

    # Регистрируем обработчик в приложении.
    application.add_handler(text_handler)

    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()