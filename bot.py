import logging
from telegram import ReplyKeyboardRemove, Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler, PicklePersistence,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s", level=logging.INFO,
    filename='bot.log', encoding='utf-8',
)
logger = logging.getLogger(__name__)

PRE_QUESTIONNAIRE, QUESTIONNAIRE_START, GENDER, FIRST_NAME, LAST_NAME, AGE, PHOTO, PHONE_NUMBER, REGISTER_TIME, \
    EXIT, SEND_CONTACT, SEND_ANSWER, DID_PARTICIPATE = range(13)

CHAT_ID = "CHAT_ID"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("%s id:%s нажал /start.", user.full_name, user.id)

    if "questionnaire_done" in context.user_data:
        await update.message.reply_text(
            "Вы уже заполняли анкету."
        )
        return ConversationHandler.END

    keyboard = [["👍", "👎"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        f"Привет, <b>{user.first_name}</b>!\n"
        "Хочешь поучаствовать в нашей фотосессии для тестирования ИСКУССТВЕННОГО ИНТЕЛЕКТА?",
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

    return PRE_QUESTIONNAIRE


async def wrong_pre_questionnaire(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("%s id:%s %s", user.full_name, user.id, update.message.text)

    await update.message.reply_text(
        "Хочешь поучавствовать в нашей фотосессии?\n"
        "Отправьте 👍 или 👎",
    )

    return PRE_QUESTIONNAIRE


async def pre_questionnaire(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("%s id:%s %s", user.full_name, user.id, update.message.text)

    keyboard = [
        ["Заполнить анкету"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text(
        "Для того чтобы оставить заявку, необходимо заполнить небольшую анкету.",
        reply_markup=reply_markup,
    )
    return QUESTIONNAIRE_START


async def questionnaire_decline(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("%s id:%s %s", user.full_name, user.id, update.message.text)

    await update.message.reply_text(
        "Нам очень жаль, что вас не заинтересовало наше предложение.\n"
        "Если у вас возникли вопросы, воспользуйтесь командой /contact.\n"
        "Введите /start, если хотите начать заново.",
        reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


async def questionnaire_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("%s id:%s %s", user.full_name, user.id, update.message.text)

    context.user_data['id'] = user.id
    context.user_data['tg_name'] = str(user.full_name)

    keyboard = [["Мужской", "Женский"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, input_field_placeholder="Ваш пол",
                                       resize_keyboard=True)
    await update.message.reply_text(
        "Выберите ваш пол.",
        reply_markup=reply_markup,
    )

    return GENDER


async def wrong_gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("%s id:%s %s", user.full_name, user.id, update.message.text)

    keyboard = [["Мужской", "Женский"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, input_field_placeholder="Ваш пол",
                                       resize_keyboard=True)
    await update.message.reply_text(
        "Нет такого варианта ответа.",
        reply_markup=reply_markup,
    )

    return GENDER


async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("%s id:%s %s", user.full_name, user.id, update.message.text)

    context.user_data['gender'] = update.message.text

    await update.message.reply_text(
        "Введите ваше имя.",
        reply_markup=ReplyKeyboardRemove()
    )

    return FIRST_NAME


async def first_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("%s id:%s %s", user.full_name, user.id, update.message.text)

    context.user_data['first_name'] = update.message.text
    await update.message.reply_text("Введите вашу фамилию.")

    return LAST_NAME


async def last_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("%s id:%s %s", user.full_name, user.id, update.message.text)

    context.user_data['last_name'] = update.message.text
    await update.message.reply_text("Введите ваш возраст.")

    return AGE


async def wrong_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("%s id:%s %s", user.full_name, user.id, update.message.text)

    await update.message.reply_text("Возраст должен быть числом в диапазоне 16-99.")

    return AGE


async def age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("%s id:%s %s", user.full_name, user.id, update.message.text)

    context.user_data['age'] = update.message.text

    keyboard = [["Пропустить"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        "Отправьте ваше фото (желательно портретное фото).\n"
        "Анкеты с фото рассматриваются быстрее.",
        reply_markup=reply_markup
    )

    return PHOTO


async def wrong_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    logger.info("%s id:%s %s", user.full_name, user.id, update.message.text)

    keyboard = [["Пропустить"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        "Неверный формат.\n"
        "Отправьте ваше фото в формате jpg/png.",
        reply_markup=reply_markup
    )

    return PHOTO


async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    logger.info("%s id:%s %s", user.full_name, user.id, update.message.text)

    context.user_data['photo'] = update.message.photo[-1]

    await update.message.reply_text(
        "Введите ваш номер телефона (для контакта).",
        reply_markup=ReplyKeyboardRemove()
    )

    return PHONE_NUMBER


async def skip_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    logger.info("%s id:%s %s", user.full_name, user.id, update.message.text)

    await update.message.reply_text(
        "Введите ваш номер телефона (для контакта).",
        reply_markup=ReplyKeyboardRemove()
    )

    return PHONE_NUMBER


async def wrong_phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("%s id:%s %s", user.full_name, user.id, update.message.text)

    await update.message.reply_text(
        "Неверный формат.\n"
        "Введите ваш номер телефона в формате +7 (999) 111-22-33",
    )

    return PHONE_NUMBER


async def phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("%s id:%s %s", user.full_name, user.id, update.message.text)

    context.user_data['phone_number'] = update.message.text

    keyboard = [
        ["с 10 до 12 часов — утро"],
        ["с 12 до 18 часов — день"],
        ["с 18 до 20 часов — вечер"],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, input_field_placeholder="Свой вариант")
    await update.message.reply_text(
        "Выберите удобное время для записи (или напишите свой вариант).",
        reply_markup=reply_markup,
    )

    return REGISTER_TIME


async def register_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("%s id:%s %s", user.full_name, user.id, update.message.text)

    context.user_data['register_time'] = update.message.text

    keyboard = [["👍", "👎"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        "Участвовали ли вы в подобных фотосессия с использованием искусственного интеллекта или нейросетей?",
        reply_markup=reply_markup
    )

    return DID_PARTICIPATE


async def did_participate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("%s id:%s %s", user.full_name, user.id, update.message.text)

    context.user_data['did_participate'] = update.message.text

    await update.message.reply_text(
        f"Отлично <b>{user.first_name}</b> 😊\n"
        "Мы свяжемся с вами в ближайшее время.\n"
        "Если у вас возникли какие-либо вопросы, воспользуйтесь командой /contact, чтобы связаться с нами.",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove()
    )

    context.user_data["questionnaire_done"] = True
    await send_questionnaire(update, context)

    return ConversationHandler.END


async def send_questionnaire(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    logger.info("%s id:%s %s", user.full_name, user.id, context.user_data)

    keyboard = [
        [
            InlineKeyboardButton("Ответить", callback_data="answer_" + str(update.message.from_user.id)),
            InlineKeyboardButton("Геолокация", callback_data="location_" + str(update.message.from_user.id)),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = f"Заявка от {update.effective_user.mention_html()}:\n" \
              f"Id: {context.user_data['id']}\n" \
              f"Пол: {context.user_data['gender']}\n" \
              f"Имя: {context.user_data['first_name']}\n" \
              f"Фамилия: {context.user_data['last_name']}\n" \
              f"Возраст: {context.user_data['age']}\n" \
              f"Номер: {context.user_data['phone_number']}\n" \
              f"Время: {context.user_data['register_time']}\n" \
              f"Участвовали: {context.user_data['did_participate']}"
    if 'photo' in context.user_data:
        await context.bot.send_photo(CHAT_ID, context.user_data['photo'], caption=message,
                                     parse_mode="HTML", reply_markup=reply_markup)
        return
    await context.bot.send_message(CHAT_ID, message, parse_mode="HTML", reply_markup=reply_markup)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("%s id:%s %s", user.full_name, user.id, update.message.text)

    await update.message.reply_text(
        "Действие отменено.",
        reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("%s id:%s %s", user.full_name, user.id, update.message.text)

    if 'contact_count' not in context.user_data:
        context.user_data['contact_count'] = 0
    if context.user_data['contact_count'] >= 5:
        await update.message.reply_text("Вы исчерпали лимит запросов.")
        return ConversationHandler.END
    context.user_data['contact_count'] += 1

    keyboard = [["Отменить"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True,
                                       input_field_placeholder="Ваш вопрос")
    await update.message.reply_text(
        "Введите ваш вопрос.",
        reply_markup=reply_markup,
    )

    return SEND_CONTACT


async def send_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("%s id:%s %s", user.full_name, user.id, update.message.text)

    await update.message.reply_text("Сообщение отправлено. Мы свяжемся с вами в ближайшее время.")

    keyboard = [
        [
            InlineKeyboardButton("Ответить", callback_data="answer_" + str(update.message.from_user.id)),
            InlineKeyboardButton("Геолокация", callback_data="location_" + str(update.message.from_user.id)),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = f"Пользователь {update.effective_user.mention_html()} " \
              f"id: {update.message.from_user.id} запрашивает обратную связь.\n" \
              f"Текст сообщения: {update.message.text}"
    await context.bot.send_message(CHAT_ID, message, parse_mode="HTML", reply_markup=reply_markup)

    return ConversationHandler.END


async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.callback_query.message.from_user
    logger.info("%s id:%s %s", user.full_name, user.id, update.callback_query.message.text)

    query = update.callback_query
    await query.answer()

    user_id = query.data.partition('_')[2]
    context.user_data["answer_id"] = user_id

    keyboard = [["Отменить"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True,
                                       input_field_placeholder="Текст ответа")
    await query.message.reply_text(
        f"Ответ пользователю id:{user_id}",
        reply_markup=reply_markup,
    )

    return SEND_ANSWER


async def send_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    logger.info("%s id:%s %s", user.full_name, user.id, update.message.text)

    await context.bot.send_message(
        context.user_data["answer_id"],
        f"{update.message.text}",
        parse_mode="HTML"
    )

    await update.message.reply_text(
        f"Пользователю id:{context.user_data['answer_id']} отправлено сообщение: {update.message.text}"
    )

    return ConversationHandler.END


async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.callback_query.message.from_user
    logger.info("%s id:%s %s", user.full_name, user.id, update.callback_query.message.text)

    query = update.callback_query
    await query.answer()

    user_id = query.data.partition('_')[2]
    await context.bot.send_location(user_id, latitude=54.4679700975935, longitude=64.7968144567598)

    await query.message.reply_text(f"Пользователю id:{user_id} отправлена геолокация.")


def main() -> None:
    persistence = PicklePersistence(filepath="bot")
    application = Application.builder().token("TOKEN").persistence(
        persistence).build()

    contact_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("contact", contact)],
        states={
            SEND_CONTACT: [
                MessageHandler(~filters.Regex("^Отменить") & filters.TEXT & ~filters.COMMAND, send_contact)
            ],
        },
        fallbacks=[
            MessageHandler(filters.Regex("^Отменить") & ~filters.COMMAND, cancel),
            MessageHandler(filters.COMMAND, cancel),
        ],
        allow_reentry=True,
    )
    application.add_handler(contact_conv_handler)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            PRE_QUESTIONNAIRE: [
                MessageHandler(filters.Regex("^👍$") & ~filters.COMMAND, pre_questionnaire),
                MessageHandler(filters.Regex("^👎$") & ~filters.COMMAND, questionnaire_decline),
                MessageHandler(~filters.Regex("^(👍|👎)$") & ~filters.COMMAND, wrong_pre_questionnaire)
            ],
            QUESTIONNAIRE_START: [MessageHandler(filters.TEXT & ~filters.COMMAND, questionnaire_start)],
            GENDER: [
                MessageHandler(filters.Regex("^Мужской$|^Женский$") & ~filters.COMMAND, gender),
                MessageHandler(~filters.Regex("^Мужской$|^Женский$") & ~filters.COMMAND, wrong_gender)
            ],
            FIRST_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_name)],
            LAST_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, last_name)],
            AGE: [
                MessageHandler(filters.Regex("^(1[6-9]|[2-9][0-9])$") & ~filters.COMMAND, age),
                MessageHandler(~filters.Regex("^(1[6-9]|[2-9][0-9])$") & ~filters.COMMAND, wrong_age)
            ],
            PHOTO: [
                MessageHandler(filters.PHOTO, photo),
                MessageHandler(~filters.PHOTO & ~filters.COMMAND & ~filters.Regex("^Пропустить$"), wrong_photo),
                MessageHandler(filters.Regex("^Пропустить$") & ~filters.COMMAND, skip_photo)
            ],
            PHONE_NUMBER: [
                MessageHandler(
                    filters.Regex("^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$")
                    & ~filters.COMMAND, phone_number),
                MessageHandler(
                    ~filters.Regex("^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$")
                    & ~filters.COMMAND, wrong_phone_number)
            ],
            REGISTER_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, register_time)],
            DID_PARTICIPATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, did_participate)]
        },
        fallbacks=[MessageHandler(filters.COMMAND, cancel)],
        allow_reentry=True,
        name="questionnaire",
        persistent=True,
    )
    application.add_handler(conv_handler)

    answer_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(answer, pattern="^answer")],
        states={
            SEND_ANSWER: [
                MessageHandler(~filters.Regex("^Отменить") & filters.TEXT & ~filters.COMMAND, send_answer),
            ],
        },
        fallbacks=[
            MessageHandler(filters.Regex("^Отменить") & ~filters.COMMAND, cancel),
            MessageHandler(filters.COMMAND, cancel),
        ],
    )
    application.add_handler(answer_conv_handler)
    application.add_handler(CallbackQueryHandler(location, pattern="^location"))

    application.run_polling()


if __name__ == "__main__":
    main()
