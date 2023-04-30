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
fin_stage_keyboard = [['/make_rezume'], ['/start']]
fin_stage_markup = ReplyKeyboardMarkup(fin_stage_keyboard, one_time_keyboard=True)
second_stage_keyboard = [['Программист'], ['Повар'], ['Актёр']]
markup_s = ReplyKeyboardMarkup(second_stage_keyboard, one_time_keyboard=True)
third_stage_keyboard = [['Нет'], ['Да']]
markup_t = ReplyKeyboardMarkup(third_stage_keyboard, one_time_keyboard=True)
fourth_stage_keyboard = [['Постоянный'], ['Плывучий'], ['Свободный']]
markup_f = ReplyKeyboardMarkup(fourth_stage_keyboard, one_time_keyboard=True)
companys = [[['Яндекс, в ней вы сможете набраться опыта и познакомится с работой программиста.'],
             ['Сбербанк, тут вы сможете полностью показать себя.']],
            [['Kikcha, тут вы сможете набраться опыта и познакомиться с работой повара.'],
             ['Ресторан Калмыцкая кухня, тут вы сможете работать в професиональной среде.']],
            [['Государственный театр танца Калмыкии «Ойраты», тут вы сможете познакомиться с работай актёра'],
             ['РЕСПУБЛИКАНСКИЙ РУССКИЙ ТЕАТР ДРАМЫ и КОМЕДИИ РЕСПУБЛИКИ КАЛМЫКИЯ, тут вы сможете показать всего себя']]]
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
            pdf.add_font('DejaVu', '', 'DefaVu/DejaVuSansCondensed.ttf', uni=True)
            pdf.set_font('DejaVu', '', 16)
            pdf.cell(200, 10, txt=f"{us.name}", align="C") #L C R
            pdf.cell(200, 10, txt='dsa', align='')
            pdf.output("simple_demo.pdf")
            return
    await update.message.reply_text(f'Вы ещё не прошли тест для создания резюме.'
                                    f'Чтобы пройти тест напишите /start', reply_markup=markup)


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
    await update.message.reply_text('Сколько вам лет?')
    return 5.5


async def fourth_stage(update, context):
    data_user['time_job'] = fourth_stage_keyboard.index([update.message.text])
    await update.message.reply_text('Сколько вам лет?')
    #await update.message.reply_text('Мы считаем что вам идеально подходит эта компания.\nХотите ли вы чтобы мы вам '
           #                         'сделали резюме для трудоустройства?', reply_markup=markup_t)
    return 5


async def alt_fif_stage(update, context):
    text = update.message.text
    try:
        data_user['years_old'] = abs(int(text))
        await update.message.reply_text('Имеется ли у вас опыт работы по вайшей специальности?', reply_markup=markup_t)
        return 9.5
    except Exception:
        await update.message.reply_text('Введите свой возраст в цифрах')
        return 5.5


async def fif_stage(update, context):
    text = update.message.text
    try:
        data_user['years_old'] = abs(int(text))
        await update.message.reply_text('Имеется ли у вас опыт работы по вайшей специальности?', reply_markup=markup_t)
        return 9
    except Exception:
        await update.message.reply_text('Введите свой возраст в цифрах')
        return 5


async def alt_fin_stage(update, context):
    data_user['exp'] = third_stage_keyboard.index([update.message.text])
    user = User()
    db_sess = db_session.create_session()
    user.job = data_user['job']
    user.marry = data_user['marry']
    user.time_job = data_user['time_job']
    user.years_old = data_user['years_old']
    user.exp = data_user['exp']
    db_sess.commit()
    await update.message.reply_text(
        'Если захотите сделать резюме то напишите /make_rezume, а если желаете изменить '
        'ответы то напишите /start', reply_markup=fin_stage_markup)
    return ConversationHandler.END


async def fin_stage(update, context):
    data_user['exp'] = third_stage_keyboard.index([update.message.text])
    user = User()
    db_sess = db_session.create_session()
    user.id = data_user['id']
    user.name = data_user['name']
    user.number_phone = data_user['number']
    user.quest_1 = data_user['job']
    user.quest_2 = data_user['marry']
    user.quest_3 = data_user['time_job']
    user.years_old = data_user['years_old']
    user.exp = data_user['exp']
    db_sess.add(user)
    db_sess.commit()
    await update.message.reply_text(
        'Если захотите сделать резюме то напишите /make_rezume, а если желаете изменить '
        'ответы то напишите /start', reply_markup=fin_stage_markup)
    return ConversationHandler.END


def main():
    db_session.global_init("db/database.db")

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
            5: [MessageHandler(filters.TEXT & ~filters.COMMAND, fif_stage)],
            5.5: [MessageHandler(filters.TEXT & ~filters.COMMAND, alt_fif_stage)],
            9: [MessageHandler(filters.TEXT & ~filters.COMMAND, fin_stage)],
            9.5: [MessageHandler(filters.TEXT & ~filters.COMMAND, alt_fin_stage)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(conv_handler)

    application.run_polling()


if __name__ == '__main__':
    main()