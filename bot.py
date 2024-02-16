import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, ConversationHandler
import config
import vk

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARNING
)
#logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("__main__").setLevel(logging.INFO)

logger = logging.getLogger(__name__)

TYPE, SIZE, QUERY = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [['/resale']]
    await update.message.reply_text(
        "Добро пожаловать в Resale Bot. Чтобы приступить к поиску айтема, наберите /resale.",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="/resale"
        )
    )


async def item_search_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [['Кроссовки', 'Одежда', 'Аксессуары']]
    user = update.message.from_user
    logger.info("User %s started the search" % user)

    await update.message.reply_text(
        "Какой тип товара вы хотите найти?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True
        )
    )
    return TYPE

async def set_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    search_type = update.message.text
    context.user_data['search_type'] = search_type
    await update.message.reply_text("Введите название айтема для поиска (Можете вводить разные сокращения (к примеру AJ1 вместо Air Jordan 1): ")
    return QUERY


async def set_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    context.user_data['query'] = query

    if context.user_data['search_type'] == 'Кроссовки':
        reply_keyboard = [['7', '7.5', '8', '8.5', '9', '9.5', '10', '10.5', '11', '11.5', '12', 'Любой']]
    elif context.user_data['search_type'] == 'Одежда':
        reply_keyboard = [['XS', 'S', 'M', 'L', 'XL', 'XXL' 'Любой']]
    else :
        reply_keyboard = [[]]
    await update.message.reply_text(
        "Введите размер",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True
        )
    )
    return SIZE


async def set_size(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    context.user_data['size'] = update.message.text
    await update.message.reply_text('Поиск начат')


    response = await vk.parse_public_by_query(context.user_data['query'], context.user_data['type'], context.user_data['size'])
    await context.bot.send_message(chat_id=update.effective_chat.id, text=' '.join(response))
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the search.", user.first_name)
    await update.message.reply_text(
        "Спасибо за использование бота.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


if __name__ == '__main__':
    application = ApplicationBuilder().token(config.TG_BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)

    application.add_handler(start_handler)


    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('resale', item_search_start)],
        states={
            TYPE: [MessageHandler(~(filters.COMMAND), set_type)],
            QUERY: [MessageHandler(~filters.COMMAND, set_query)],
            SIZE: [MessageHandler(~filters.COMMAND, set_size)],
        },
        fallbacks = [CommandHandler('cancel', cancel)]
    )
    application.add_handler(conversation_handler)
    application.run_polling()
