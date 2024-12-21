from aiogram import Bot, Dispatcher, types, executor
from aiogram.types.web_app_info import WebAppInfo
import atexit
from url import domen
from bottoken import bot_token

bot = Bot(bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'loadgame'])
async def start(message: types.Message):
    invited = message.from_user.id
    name = message.from_user.first_name
    print(name, " (", invited, ")")

    args = message.get_args()  # Get the arguments from the deeplink
    if args.startswith('invitor_'):  # Check if it's a referral deeplink
        invitor = args.split('_')[1]  # Extract the invitor ID
        url = f'{domen}/referral/?username={invited}&invitor={invitor}&user_firstname={name}'

        print(url)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Open app', web_app=WebAppInfo(url=url)))
        await message.answer(f"Let's start, open the web app.",
                             reply_markup=markup)
    else:
        url = f'{domen}/?username={invited}&user_firstname={name}'
        print(url)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Open app', web_app=WebAppInfo(url=url)))
        await message.answer("Let's start, open the web app.", reply_markup=markup)

executor.start_polling(dp)

