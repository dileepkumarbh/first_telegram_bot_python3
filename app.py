import logging
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler
from urllib.request import urlopen, Request
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from bs4 import BeautifulSoup
import os
PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = '....'
CHOOSING, TICKER_CHOICE = range(2)

def start(update, context):
    # update.message.reply_text("Search a ticker symbol to get daily headlines for a stock")
    # dp.add_handler(MessageHandler(Filters.text & ~Filters.command, parseInput))
    # text for the inline keyboard buttons, each list within keyboard is a row, 
    # each list within that is a column
    keyboard = [[InlineKeyboardButton("Search for ticker news", callback_data='tickerNews')],
                [InlineKeyboardButton("View ticker price", callback_data='tickerPrice')],
                [InlineKeyboardButton("Search company ticker", callback_data='tickerLookup')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)

    return CHOOSING


def button(update, context):
    query = update.callback_query

    # print('button option: {}').format(context.user_data['option'])
    if query.data == 'tickerNews':
        # print('button query.data: ' + query.data)
        context.user_data['option'] = query.data
        query.edit_message_text("Reply with a ticker symbol to get daily headlines for a stock")
    elif query.data == 'tickerPrice':
        # print('button query.data: ' + query.data)
        context.user_data['option'] = query.data
        query.edit_message_text("Reply with a ticker symbol to view its price")
    elif query.data == 'tickerLookup':
        # print('button query.data: ' + query.data)
        context.user_data['option'] = query.data
        query.edit_message_text("Reply with a company to view its stock ticker")

    return TICKER_CHOICE

def custom_ticker(update, context):
    # user_data = context.user_data
    # text = update.message.text
    # category = user_data['option']
    # user_data[category] = text

    parseInput(update, context)
    # reset chosen option
    # del query.data
    context.user_data.clear()
    # print('done')
    return ConversationHandler.END

def parseInput(update, context):
    user_input = update.message.text
    option = context.user_data['option']

    ticker = user_input.upper()
    # print('ticker input: {}'.format(ticker))
    # print('parseInput option: ' + option)
    if option == 'tickerNews':
        update.message.reply_text("News!")
    elif option == 'tickerPrice':
        update.message.reply_text("Price!")
    elif option == 'tickerLookup':
        update.message.reply_text("Ticker!")

    return
    
def error(update, context):
    """Log errors caused by Updates"""
    logger.warning('Update "%s" cause error "%s"', update, context.error)
    

    
def main():
    
    # Get the dispatcher to register handlers
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    # on different commands - answer in Telegram
    conv_handler = ConversationHandler(
        entry_points = [CommandHandler('start', start)],
        
        states = {
            CHOOSING:[CallbackQueryHandler(button, '(^tickerNews/tickerPrice/tickerLookup)$')],
            TICKER_CHOICE: [MessageHandler(Filters.text & ~Filters.command, custom_ticker)]
            },
        fallbacks = [CommandHandler('start', start)]

        )

    dp.add_handler(conv_handler)
    
    
    
    # log all errors
    dp.add_error_handler(error)
    
    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('example.com' + TOKEN)
    updater.idle()

if __name__ == '__main__':
    main()