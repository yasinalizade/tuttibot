from aiogram import Bot, Dispatcher, executor
from aiogram.types import ReplyKeyboardMarkup, Message
from async_main import collect_data
from dotenv import load_dotenv
from os import getenv

# create .env file and put your bot token in the file.
# DO NOT forget to check if '.env' in your .gitignore file!
load_dotenv()

bot = Bot(token=getenv('TOKEN'))
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    await message.answer(
        'Buongiorno, tutti! Write here a composer and a piece, I will search it for you!',
        reply_markup=keyboard
    )


@dp.message_handler(content_types=["text"])
async def handle_text(message: Message):
    await message.answer('Please waiting...')
    answer = await collect_data(message.text)
    await bot.send_message(chat_id=message.chat.id, text=answer)


if __name__ == '__main__':
    executor.start_polling(dp)
