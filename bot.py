from aiogram import F, Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.enums import ParseMode
import re
import asyncio
from aiogram.types.web_app_info import WebAppInfo

# Initialize the bot and dispatcher
bot = Bot(token="7348387250:AAHu-3ik9G3vcS1oG6FTkxnL0tF_eoiC314")
dp = Dispatcher()
user_data = {}



@dp.message(Command("loadgame"))
async def load_game(message: types.Message):
    url = f'https://yukkie.pythonanywhere.com/?username={message.from_user.username}'

    buttonsstart = [
        [types.InlineKeyboardButton(text="Start", web_app=WebAppInfo(url=url))]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttonsstart)

    await message.answer(f"Hello, {message.from_user.full_name}!", reply_markup=keyboard)

@dp.message(CommandStart(deep_link=True))
async def load_game_referral(message: types.Message, command: CommandStart):
        number = command.args.split("_")[1]
        url = f'https://yukkie.pythonanywhere.com/referral/?username={message.from_user.username}&invitor={number}'

        buttonsref = [
            [types.InlineKeyboardButton(text="Start", web_app=WebAppInfo(url=url))]
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttonsref)

        await message.answer(f"Hello, {message.from_user.full_name}", reply_markup=keyboard)


@dp.message(CommandStart(deep_link=True))
async def cmd_start_invitor(message: types.Message, command: CommandStart):
    # Check if the deep link argument is present
    if command.args and re.match(r'invitor_(\d+)', command.args):
        number = command.args.split("_")[1]
        invited = "username"
        invitor = "username"
        await message.answer(f"https://yukkie.com/referral/?username={invited}&invitor={invitor} №{number}")
    else:
        # Handle the case when no deep link is provided
        await message.answer("Welcome! You haven't used a referral link.")


async def update_num_text(message: types.Message, new_value: int):
    await message.edit_text(
        f"Укажите число: {new_value}",
        reply_markup=get_keyboard()
    )

@dp.message(Command("numbers"))
async def cmd_numbers(message: types.Message):
    user_data[message.from_user.id] = 0
    await message.answer("Укажите число: 0", reply_markup=get_keyboard())


@dp.callback_query(F.data.startswith("num_"))
async def callbacks_num(callback: types.CallbackQuery):
    user_value = user_data.get(callback.from_user.id, 0)
    action = callback.data.split("_")[1]

    if action == "incr":
        user_data[callback.from_user.id] = user_value+1
        await update_num_text(callback.message, user_value+1)
    elif action == "decr":
        user_data[callback.from_user.id] = user_value-1
        await update_num_text(callback.message, user_value-1)
    elif action == "finish":
        await callback.message.edit_text(f"Итого: {user_value}")

    await callback.answer()
#



# Running the bot
async def main():
    await dp.start_polling(bot)

# Corrected the name check
if __name__ == "__main__":
    asyncio.run(main())







#
# @dp.message(Command("yoyo"))
# async def cmd_start(message: types.Message):
#     kb = [
#         [
#             types.KeyboardButton(text="С пюрешкой"),
#             types.KeyboardButton(text="Без пюрешки")
#         ],
#     ]
#     keyboard = types.ReplyKeyboardMarkup(
#         keyboard=kb,
#         resize_keyboard=True,
#         input_field_placeholder="Выберите способ подачи"
#     )
#     await message.answer("Как подавать котлеты?", reply_markup=keyboard)
# @dp.message(F.text.lower() == "с пюрешкой")
# async def with_puree(message: types.Message):
#     await message.reply("Отличный выбор!")
#
# @dp.message(F.text.lower() == "без пюрешки")
# async def without_puree(message: types.Message):
#     await message.reply("Так невкусно!")
#
# user_data = {}
#
# def get_keyboard():
#     buttons = [
#         [
#             types.InlineKeyboardButton(text="-1", callback_data="num_decr"),
#             types.InlineKeyboardButton(text="+1", callback_data="num_incr")
#         ],
#         [types.InlineKeyboardButton(text="Подтвердить", callback_data="num_finish")]
#     ]
#     keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
#     return keyboard




# https://yukkie.pythonanywhere.com/?username={invited}
# https://yukkie.pythonanywhere.com/referral/?username={invited}&invitor={invitor}
# https://t.me/LeoTon_bot?start=startapp=username