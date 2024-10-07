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


    args = message.get_args().split('=')
    if len(args) == 2 and args[0] == 'startapp':
        invitor = args[1]

        url = f'{domen}/referral/?username={invited}&invitor={invitor}&user_firstname={name}'
        print(url)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Open app', web_app=WebAppInfo(url=url)))
        await message.answer(f"Let's start, open the web app. You were invited by {invitor}.",
                             reply_markup=markup)
    else:
        url = f'{domen}/?username={invited}&user_firstname={name}'
        print(url)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Open app', web_app=WebAppInfo(url=url)))
        await message.answer("Let's start, open the web app.", reply_markup=markup)


@dp.message_handler(commands=['adminpanel'])
async def admin(message: types.Message):
    print(message.from_user.id)
    if message.from_user.id == 1351813206 or 6436266975:
        url = f'{domen}/admin/myapp/telegram_sub_tasks/'
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Open app', web_app=WebAppInfo(url=url)))
        await message.answer("Let's start, open the admin panel.", reply_markup=markup)
    else:
        print('not allowed')
        pass
executor.start_polling(dp)

