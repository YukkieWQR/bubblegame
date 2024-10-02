from aiogram import F, Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
import requests
from bottoken import *
from url import domen

bot = Bot(bot_token_community)
dp = Dispatcher()

user_tasks = {}

def get_chat_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('chat_id'), data.get('url')
    else:
        print(f"Failed to fetch data from {url}")
        return None, None

chat_id_1, channel_url_1 = get_chat_data(f'{domen}/json_bot_1/')
chat_id_2, channel_url_2 = get_chat_data(f'{domen}/json_bot_2/')

subscribe_button_1 = types.InlineKeyboardButton(text="Subscribe to Channel", url=channel_url_1)
subscribe_button_2 = types.InlineKeyboardButton(text="Subscribe to Channel", url=channel_url_2)
check_button = types.InlineKeyboardButton(text="Check Subscription", callback_data="check_subscription")


@dp.message(Command("start"))
async def load_game(message: types.Message):
    buttonsstart = [
        [types.InlineKeyboardButton(text="Tasks", callback_data="checkbuttons")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttonsstart)
    await message.answer(f"Hello, {message.from_user.full_name}, let's start!", reply_markup=keyboard)


@dp.callback_query(F.data == "checkbuttons")
async def checkbuttons(callback_query: types.CallbackQuery):
    task_button_1 = types.InlineKeyboardButton(text="Task 1", callback_data="task_1")
    task_button_2 = types.InlineKeyboardButton(text="Task 2", callback_data="task_2")
    task_keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[task_button_1], [task_button_2]])
    await callback_query.message.answer("Choose a task:", reply_markup=task_keyboard)


@dp.callback_query(F.data.in_({"task_1", "task_2"}))
async def select_task(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_tasks[user_id] = callback_query.data

    if callback_query.data == "task_1":
        await callback_query.message.answer(
            "You selected Task 1. Please subscribe to the channel and then check your subscription.",
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[subscribe_button_1, check_button]])
        )
    elif callback_query.data == "task_2":
        await callback_query.message.answer(
            "You selected Task 2. Please subscribe to the channel and then check your subscription.",
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[subscribe_button_2, check_button]])
        )


@dp.callback_query(F.data == "check_subscription")
async def check_subscription(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    selected_task = user_tasks.get(user_id)

    if selected_task == "task_1":
        chat_id = chat_id_1
    elif selected_task == "task_2":
        chat_id = chat_id_2
    else:
        await callback_query.message.answer("Please select a task first.")
        return

    chat_member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)

    if chat_member.status in ['member', 'administrator', 'creator']:
        google_button = types.InlineKeyboardButton(
            text="Get reward!",
            web_app=types.WebAppInfo(
                url=f"{domen}/reward_for_subscription/?username={callback_query.from_user.username}&reward_id={chat_id}")
        )

        await callback_query.message.answer(
            "You are subscribed! Take your reward: ",
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[[google_button]])
        )
    else:
        await callback_query.message.answer("You are not subscribed yet. Please subscribe to get the reward.")


@dp.message(Command("stats"))
async def stats(message: types.Message):
    response = requests.get(f'{domen}/json_bot_stats')
    if response.status_code == 200:
        data = response.json()
        total_users = data.get('total_users')
        users_joined_today = data.get('users_joined_today')
        users_joined_this_month = data.get('users_joined_this_month')
        users_online_today = data.get('users_online_today')

        stats_message = (
            f"📊 Bot Statistics:\n"
            f"Total users: {total_users}\n"
            f"Users joined today: {users_joined_today}\n"
            f"Users joined this month: {users_joined_this_month}\n"
            f"Users online today: {users_online_today}"
        )

        await message.answer(stats_message)
    else:
        await message.answer("Failed to fetch stats.")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
