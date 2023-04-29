import logging
from telegram.ext import Application, MessageHandler, filters,  CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup
from config import BOT_TOKEN
from data import db_session
from data.users import User
from fpdf import FPDF
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG, filename='bot.log'
)

logger = logging.getLogger(__name__)
reply_keyboard = [['/start']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
second_stage_keyboard = [['Программист'], ['Повар'], ['Певец']]
markup_s = ReplyKeyboardMarkup(second_stage_keyboard, one_time_keyboard=True)
third_stage_keyboard = [['Нет'], ['Да']]
markup_t = ReplyKeyboardMarkup(third_stage_keyboard, one_time_keyboard=True)
fourth_stage_keyboard = [['Постоянный'], ['Непостоянный'], ['Свободный']]
markup_f = ReplyKeyboardMarkup(fourth_stage_keyboard, one_time_keyboard=True)
companys = [[], [], []]
data_user = dict()


def test(number):
    number = ''.join(number.split())
    if number.startswith('+'):
        if number[:2] != '+7':
            return False
        number = '+7' + number[2:]
    elif number.startswith('8'):
        number = '+7' + number[1:]
    else:
        return False
    scob_left = number.count('(')
    scob_right = number.count(')')
    if scob_left == 1 and scob_right == 1:
        if number.index(')') - number.index('(') != 4:
            return False
        number = number.replace('(', '').replace(')', '')
    elif scob_left != 0 or scob_right != 0:
        return False
    tire = number.split('-')
    if not all(tire):
        return False
    else:
        number = ''.join(tire)
    if not all(i.isnumeric() for i in number[2:]):
        return False
    if len(number) != 12:
        return False
    return True


async def help(update, context):
    await update.message.reply_text("Чтобы начать нажмите /start", reply_markup=markup)


async def stop(update, context):
    await update.message.reply_text("Всего доброго!")
    return ConversationHandler.END


async def make_rezume(update, context):
    db_sess = db_session.create_session()
    idd = update.effective_chat.id
    for us in db_sess.query(User).filter(User.id == idd):
        if us.name:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 20, txt=f"{us.name}", ln=1, align="C")
            pdf.output("simple_demo.pdf")
            return
    print(1)



async def start(update, context):
    data_user.clear()
    user = update.effective_user
    db_sess = db_session.create_session()
    idd = update.effective_chat.id
    for us in db_sess.query(User).filter(User.id == idd):
        if us.name:
            await update.message.reply_html(rf"И вновь здравствуй {user.mention_html()}! Желаешь ещё раз пройти тест?",
                                            reply_markup=markup_t)
            return 1.7

    await update.message.reply_html(
        rf"Здравствуйте {user.mention_html()}! Я Бот, который задаст тебе пару вопросов для "
    "устройства на работу. Удачи!"
        rf" ПЕРВЫЙ ЭТАП: "
        rf"Назовите свои Фамилию Имя Отчество")
    return 1


async def alt_first_stage(update, context):
    if third_stage_keyboard.index([update.message.text]):
        await update.message.reply_text('Чтож, тогда какова ваша специальность?', reply_markup=markup_s)
        return 2.5
    else:
        await update.message.reply_text('Всего доброго!') #


async def first_stage(update, context):
    data_user['id'] = update.effective_chat.id
    data_user['name'] = update.message.text
    await update.message.reply_text('Какой номер вашего телефона?')
    return 1.5


async def real_number(update, context):
    num = update.message.text
    if test(num):
        data_user['number'] = num
        await update.message.reply_text('Номер указан верно.\nКакова ваша специальность?', reply_markup=markup_s)
        return 2
    else:
        await update.message.reply_text('Номер указан неверно.\nНапишите найстоящий номер.')
        return 1.5


async def alt_second_stage(update, context):
    data_user['job'] = second_stage_keyboard.index([update.message.text])
    await update.message.reply_text('Находитесь ли вы браке?', reply_markup=markup_t)
    return 3.5


async def second_stage(update, context):
    data_user['job'] = second_stage_keyboard.index([update.message.text])
    await update.message.reply_text('Находитесь ли вы браке?', reply_markup=markup_t)
    return 3


async def alt_third_stage(update, context):
    data_user['marry'] = third_stage_keyboard.index([update.message.text])
    await update.message.reply_text("Какой график работы вы желаете иметь?", reply_markup=markup_f)
    return 4.5


async def third_stage(update, context):
    data_user['marry'] = third_stage_keyboard.index([update.message.text])
    await update.message.reply_text("Какой график работы вы желаете иметь?", reply_markup=markup_f)
    return 4


async def alt_fourth_stage(update, context):
    data_user['time_job'] = fourth_stage_keyboard.index([update.message.text])
    await update.message.reply_text('Мы считаем что вам идеально подходит эта компания.\nХотите ли вы чтобы мы вам '
                                    'сделали резюме для трудоустройства?', reply_markup=markup_t)
    return 9.5


async def fourth_stage(update, context):
    data_user['time_job'] = fourth_stage_keyboard.index([update.message.text])

    await update.message.reply_text('Мы считаем что вам идеально подходит эта компания.\nХотите ли вы чтобы мы вам '
                                    'сделали резюме для трудоустройства?', reply_markup=markup_t)
    return 9


async def alt_fin_stage(update, context):
    user = User()
    db_sess = db_session.create_session()
    user.quest_1 = data_user['job']
    user.quest_2 = data_user['marry']
    user.quest_3 = data_user['time_job']
    db_sess.commit()
    if third_stage_keyboard.index([update.message.text]):
        await update.message.reply_text('Если желаете именить ваши ответы то введите /start', reply_markup=markup)
        return ConversationHandler.END
    else:
        await update.message.reply_text('Если желаете именить ваши ответы то введите /start', reply_markup=markup)
        return ConversationHandler.END


async def fin_stage(update, context):
    user = User()
    db_sess = db_session.create_session()
    user.id = data_user['id']
    user.name = data_user['name']
    user.number_phone = data_user['number']
    user.quest_1 = data_user['job']
    user.quest_2 = data_user['marry']
    user.quest_3 = data_user['time_job']
    db_sess.add(user)
    db_sess.commit()
    if third_stage_keyboard.index([update.message.text]):
        await update.message.reply_text('Если желаете именить ваши ответы то введите /start', reply_markup=markup)
        return ConversationHandler.END
    else:
        await update.message.reply_text('Если желаете именить ваши ответы то введите /start', reply_markup=markup)
        return ConversationHandler.END


def main():
    db_session.global_init("db/blogs.db")

    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("make_rezume", make_rezume))

    conv_handler = ConversationHandler(entry_points=[CommandHandler('start', start)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_stage)],
            1.5: [MessageHandler(filters.TEXT & ~filters.COMMAND, real_number)],
            1.7: [MessageHandler(filters.TEXT & ~filters.COMMAND, alt_first_stage)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_stage)],
            2.5: [MessageHandler(filters.TEXT & ~filters.COMMAND, alt_second_stage)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, third_stage)],
            3.5: [MessageHandler(filters.TEXT & ~filters.COMMAND, alt_third_stage)],
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, fourth_stage)],
            4.5: [MessageHandler(filters.TEXT & ~filters.COMMAND, alt_fourth_stage)],
            9: [MessageHandler(filters.TEXT & ~filters.COMMAND, fin_stage)],
            9.5: [MessageHandler(filters.TEXT & ~filters.COMMAND, alt_fin_stage)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(conv_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
