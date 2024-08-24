from aiogram import Bot, Dispatcher, types, executor
from aiogram.types.web_app_info import WebAppInfo
import sqlite3
import atexit

# Initialize bot and dispatcher
bot = Bot('7348387250:AAHu-3ik9G3vcS1oG6FTkxnL0tF_eoiC314')
dp = Dispatcher(bot)

# Initialize SQLite database and create table if not exists
def init_db():
    with sqlite3.connect('referrals.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS referrals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invitor TEXT NOT NULL,
                invited TEXT NOT NULL
            )
        ''')
        conn.commit()

init_db()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    invited = message.from_user.username

    # Extract referral code if present
    args = message.get_args().split('=')
    if len(args) == 2 and args[0] == 'startapp':
        invitor = args[1]

        # Save invitor and invited information in the database
        try:
            with sqlite3.connect('referrals.db') as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO referrals (invitor, invited) VALUES (?, ?)', (invitor, invited))
                conn.commit()

            # Prepare the URL for the web app with referral
            url = f'https://yukkie.pythonanywhere.com/referral/?username={invited}&invitor={invitor}'
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Open app', web_app=WebAppInfo(url=url)))

            await message.answer(f"Let's start, open the web app. You were invited by {invitor}.", reply_markup=markup)
        except sqlite3.Error as e:
            await message.answer("An error occurred while processing your referral. Please try again later.")
            print(f"SQLite error: {e}")
    else:
        # Handle the case where there is no referral code
        url = f'https://yukkie.pythonanywhere.com/?username={invited}'
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Open app', web_app=WebAppInfo(url=url)))

        await message.answer("Let's start, open the web app.", reply_markup=markup)

@dp.message_handler(commands=['check'])
async def check_subscription(message: types.Message):
    user_id = message.from_user.id
    args = message.get_args().split()

    if len(args) == 0:
        await message.answer("No channel link provided.")
        return

    channel_url = args[0]

    # Extract channel username or ID from the URL
    if "t.me" in channel_url:
        chat_id = channel_url.split('/')[-1]
        if not chat_id.startswith('@'):
            chat_id = f'@{chat_id}'
    else:
        await message.answer("Invalid channel URL.")
        return

    try:
        member = await bot.get_chat_member(chat_id, user_id)
        if member.is_chat_member():
            youtube_url = 'https://www.youtube.com/'  # Replace with your desired YouTube URL
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Open YouTube', url=youtube_url))
            await message.answer("You are subscribed! Enjoy the content on YouTube.", reply_markup=markup)
        else:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Subscribe to the channel', url=channel_url))
            await message.answer("Please subscribe to the channel first.", reply_markup=markup)
    except Exception as e:
        await message.answer("An error occurred while checking your subscription. Please try again later.")
        print(f"Error checking subscription: {e}")

executor.start_polling(dp)

# Close the database connection on exit
atexit.register(bot.close)