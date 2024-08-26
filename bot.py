from aiogram import F, Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.enums import ParseMode
import re
import asyncio

# Initialize the bot and dispatcher
bot = Bot(token="7348387250:AAHu-3ik9G3vcS1oG6FTkxnL0tF_eoiC314")
dp = Dispatcher()

# Help command handler
@dp.message(Command("loadgame"))
async def cmd_help(message: Message):
    await message.answer(f"Hello, {(message.from_user.full_name)}!")


@dp.message(CommandStart(
    deep_link=True,
    magic=F.args.regexp(re.compile(r'invitor_(\d+)'))
))
async def cmd_start_invitor(
        message: Message,
        command: CommandObject
):
    number = command.args.split("_")[1]
    invited = "username"
    invitor = "username"
    await message.answer(f"https://yukkie.pythonanywhere.com/referral/?username={invited}&invitor={invitor} №{number}")


# Running the bot
async def main():
    await dp.start_polling(bot)

# Corrected the name check
if __name__ == "__main__":
    asyncio.run(main())



# https://yukkie.pythonanywhere.com/?username={invited}
# https://yukkie.pythonanywhere.com/referral/?username={invited}&invitor={invitor}
# https://t.me/LeoTon_bot?start=startapp=username