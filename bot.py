import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import config
import vk


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def parse_public(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = vk.parse_public_by_query(context.args)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=' '.join(response))


if __name__ == '__main__':
    application = ApplicationBuilder().token(config.TG_BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    parse_handler = CommandHandler('parse', parse_public)

    application.add_handler(start_handler)
    application.add_handler(parse_handler)

    application.run_polling()
