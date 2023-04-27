import logging
from telegram.ext import Application, MessageHandler, filters,  CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from config import BOT_TOKEN


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)
spisok = []
reply_keyboard = [['/start']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
second_stage_keyboard = [['Создание програм'], ['Готовка разнообразных блюд'], ['Пение']]
markup_s = ReplyKeyboardMarkup(second_stage_keyboard, one_time_keyboard=True)
third_stage_keyboard = [['Да'], ['Нет']]
markup_t = ReplyKeyboardMarkup(third_stage_keyboard, one_time_keyboard=True)
fourth_stage_keyboard = [['Постоянный'], ['Непостоянный'], ['Свободный']]
markup_f = ReplyKeyboardMarkup(fourth_stage_keyboard, one_time_keyboard=True)
companys = [[], [], []]




async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    spisok.clear()
    user = update.effective_user
    await update.message.reply_html(
        rf"Здравствуйте {user.mention_html()}! Я Бот, который задаст тебе пару вопросов для устройства на работу. Удачи!"
        rf"ПЕРВЫЙ ЭТАП: "
        rf"Назовите свои Фамилию Имя Отчество")
    return 1


async def help(update, context):
    await update.message.reply_text("Чтобы начать нажмите /start", reply_markup=markup)


async def second_stage(update, context):
    spisok.append(update.message.text)
    await update.message.reply_text('Какого рода деятельность вам больше всего симпатизирует?', reply_markup=markup_s)
    return 2


async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


async def third_stage(update, context):
    spisok.append(second_stage_keyboard.index([update.message.text]))
    await update.message.reply_text('Находитесь ли вы браке?', reply_markup=markup_t)
    return 3


async def fourth_stage(update, context):
    spisok.append(update.message.text)
    await update.message.reply_text("Какой график работы вы желаете иметь?", reply_markup=markup_f)
    print(spisok)
    return ConversationHandler.END  # Константа, означающая конец диалога.
    # Все обработчики из states и fallbacks становятся неактивными.

def main():
    # Создаём объект Application.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    application = Application.builder().token(BOT_TOKEN).build()

    #application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))

    #text_handler = MessageHandler(filters.TEXT, twoquest)
    #application.add_handler(text_handler)

    conv_handler = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('start', start)],

        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            # Функция читает ответ на первый вопрос и задаёт второй.
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_stage)],
            # Функция читает ответ на второй вопрос и завершает диалог.
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, third_stage)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, fourth_stage)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(conv_handler)

    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()