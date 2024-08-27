from aiogram import F, Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.enums import ParseMode
import re
import asyncio
from aiogram.types.web_app_info import WebAppInfo
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# token here is token of telegram bot, you get it from @BotFather
# токен здесь - это токен бота Telegram, вы получаете его от @BotFather
bot = Bot(token="7348387250:AAHu-3ik9G3vcS1oG6FTkxnL0tF_eoiC314")
dp = Dispatcher()
user_data = {}




#HERE IS url='', dont change structure, Bot must be admin in that channel to see users list
subscribe_button_1 = InlineKeyboardButton(text="Subscribe to Channel", url="https://t.me/testChannelYea")
subscribe_button_2 = InlineKeyboardButton(text="Subscribe to Channel", url="https://t.me/testChannelYea")
subscribe_button_3 = InlineKeyboardButton(text="Subscribe to Channel", url="https://t.me/testChannelYea")
#ЗДЕСЬ url='', не меняйте структуру, бот должен быть администратором на этом канале, чтобы видеть список пользователей


#same structure with urls upper, here must be your telergam channel id
chat_id_1 = "-1002172423606"
chat_id_2 = "-1002172423606"
chat_id_3 = "-1002172423606"
#та же структура с URL-адресами вверху, здесь должен быть ваш идентификатор (id) канала Telegram





check_button = InlineKeyboardButton(text="Check Subscription", callback_data="check_subscription")


google_button = InlineKeyboardButton(text="Open Google", url="https://yukkie.pythonanywhere.com/reward_for_subscription")


user_tasks = {}


@dp.message(Command("loadgame"))
async def load_game(message: types.Message):
    url = f'https://yukkie.pythonanywhere.com/?username={message.from_user.username}'

    buttonsstart = [
        [types.InlineKeyboardButton(text="Start", web_app=WebAppInfo(url=url))],
        [types.InlineKeyboardButton(text="Tasks", callback_data="checkbuttons")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttonsstart)

    await message.answer(f"Hello, {message.from_user.full_name}, let's start!", reply_markup=keyboard)


@dp.message(CommandStart(deep_link=True))
async def load_game_referral(message: types.Message, command: CommandStart):
        number = command.args.split("_")[1]
        url = f'https://yukkie.pythonanywhere.com/referral/?username={message.from_user.username}&invitor={number}'

        buttonsref = [
            [types.InlineKeyboardButton(text="Start", web_app=WebAppInfo(url=url))],
            [types.InlineKeyboardButton(text="Tasks", callback_data="checkbuttons")]
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttonsref)

        await message.answer(f"Hello, {message.from_user.full_name}, let's start!", reply_markup=keyboard)







#########################################################################################
## next part of code is for tasks #######################################################
#########################################################################################






@dp.callback_query(F.data == "checkbuttons")
async def checkbuttons(callback_query: types.CallbackQuery):

    task_button_1 = InlineKeyboardButton(text="Task 1", callback_data="task_1")
    task_button_2 = InlineKeyboardButton(text="Task 2", callback_data="task_2")
    task_button_3 = InlineKeyboardButton(text="Task 3", callback_data="task_3")


    task_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [task_button_1],
        [task_button_2],
        [task_button_3]
    ])


    await callback_query.message.answer("Choose a task:", reply_markup=task_keyboard)

@dp.callback_query(F.data.in_({"task_1", "task_2", "task_3"}))
async def select_task(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id


    user_tasks[user_id] = callback_query.data


    if callback_query.data == "task_1":
        await callback_query.message.answer(
            "You selected Task 1. Please subscribe to the channel and then check your subscription.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[subscribe_button_1, check_button]])
        )
    elif callback_query.data == "task_2":
        await callback_query.message.answer(
            "You selected Task 2. Please subscribe to the channel and then check your subscription.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[subscribe_button_2, check_button]])
        )
    elif callback_query.data == "task_3":
        await callback_query.message.answer(
            "You selected Task 3. Please subscribe to the channel and then check your subscription.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[subscribe_button_3, check_button]])
        )


@dp.callback_query(F.data == "check_subscription")
async def check_subscription(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    # Determine which task was selected
    selected_task = user_tasks.get(user_id)

    if selected_task == "task_1":
        chat_id = chat_id_1
    elif selected_task == "task_2":
        chat_id = chat_id_2
    elif selected_task == "task_3":
        chat_id = chat_id_3
    else:
        await callback_query.message.answer("Please select a task first.")
        return

    # Check if the user is subscribed
    chat_member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)

    if chat_member.status in ['member', 'administrator', 'creator']:
        await callback_query.message.answer(
            "You are subscribed! Take your reward: ",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[[google_button]])
        )
    else:
        await callback_query.message.answer(
            "You are not subscribed. Please subscribe to the channel and try again.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [
                    subscribe_button_1 if selected_task == "task_1" else subscribe_button_2 if selected_task == "task_2" else subscribe_button_3,
                    check_button]
            ])
        )








async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())




