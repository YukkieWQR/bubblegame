from aiogram import Bot, Dispatcher, types, executor
from aiogram.types.web_app_info import WebAppInfo
from aiogram.utils.exceptions import ChatNotFound
import sqlite3
import atexit
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


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
    username = message.from_user.username
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
        # Check if the user is a member of the channel
        member = await bot.get_chat_member(chat_id, username)
        if member.is_chat_member():
            youtube_url = 'https://www.youtube.com/'  # Replace with your desired YouTube URL
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Open YouTube', url=youtube_url))
            await message.answer("You are subscribed! Enjoy the content on YouTube.", reply_markup=markup)
        else:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Subscribe to the channel', url=channel_url))
            await message.answer("Please subscribe to the channel first.", reply_markup=markup)
    except ChatNotFound:
        await message.answer("Channel not found.")
    except Exception as e:
        await message.answer("An error occurred while checking your subscription. Please try again later.")
        print(f"Error checking subscription: {e}")

executor.start_polling(dp)

# Close the database connection on exit
atexit.register(bot.close)


@csrf_exempt
def telegram_subscription(request):
    username = request.POST.get('username')
    task_pk = request.POST.get('task_pk')
    channel_url = request.POST.get('channel_url')

    if username and channel_url:
        # Call Telegram bot's webhook to check the subscription
        response = requests.post(
            'https://yukkie.pythonanywhere.com/bot/webhook/',
            json={
                'command': 'check',
                'channel_url': channel_url,
                'username': username
            }
        )

        # Optional: Handle the bot's response
        if response.status_code == 200:
            bot_response = response.json()

        user, created = UserProfile.objects.get_or_create(username=username)
        task = Task.objects.get(pk=task_pk)
        user.wallet += task.cost
        user.save()

    response_data = {
        'username': username,
    }

    return JsonResponse(response_data)