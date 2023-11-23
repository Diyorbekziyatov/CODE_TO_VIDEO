import aiogram
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext, filters
from aiogram.types import Message
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

token = "6636034372:AAGq5_5YsoyeMfEdmdeZa3DNHr30i1LIOLI"

code_to_video = {
    "12345": "https://t.me/Tarjima_kinolar_ujastik_kinolar/824",
    "67890": ""
}

bot = aiogram.Bot(token=token)
dp = Dispatcher(bot)


admins = ["https://t.me/DIYOR_003E", "https://t.me/Elshod_cik"]

custom_keyboard = InlineKeyboardMarkup(row_width=2)
custom_keyboard.add(InlineKeyboardButton("KINO CODI", callback_data="KINO CODI"))
custom_keyboard.add(InlineKeyboardButton("BIZNING KANAL", callback_data="BIZNING KANAL"))


class VideoCodeState(StatesGroup):
    waiting_for_video_code = State()

@dp.message_handler(commands=['post_video'])
async def post_video_start(message: types.Message):
    user = message.from_user

    if user.username in admins:
        await message.reply("Iltimos kino kodini kiriting.")
        await VideoCodeState.waiting_for_video_code.set()
    else:
        await message.reply("Kino kodini xato kiritingiz.")

@dp.message_handler(state=VideoCodeState.waiting_for_video_code)
async def post_video_step(message: types.Message, state: FSMContext):
    user_input = message.text
    video_url = code_to_video.get(user_input)

    if video_url:
        await bot.send_video(message.chat.id, video=video_url, caption="Siz izlagan kino:")
        await state.finish()
    else:
        await message.reply("Kechirasiz, bu kod uchun video topa olmadim. Iltimos, yana bir bor urinib ko'ring.")



@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user = message.from_user

    start_message = (
        "Assalomu alaykum yangi foydalanuvchi botimizga xush kelipsiz\n"
        "BOT sizga qidirayotgan kinoyingizni topishda yordam beradi! \n Iltimos kino kodini kiriting!"
    )
   
    await message.reply(
        start_message,
        reply_markup=custom_keyboard
    )

@dp.callback_query_handler(lambda callback_query: True)
async def button(callback_query: types.CallbackQuery):
    await callback_query.answer()

    if callback_query.data == "KINO CODI":
        
        await callback_query.message.reply("Iltimos kino kodini kiriting.")
    elif callback_query.data == "BIZNING KANAL":
        
        await callback_query.message.reply("Bu bizning official kanal: https://t.me/BASSMUZIKALAR_MUZIKALAR2023HIT")
    
@dp.message_handler(lambda message: message.text.isnumeric())
async def handle_text(message: types.Message):
    user_input = message.text
    video_url = code_to_video.get(user_input)

    if video_url:
        await message.reply(f"Siz izlagan kino: {video_url}")
    else:
        await message.reply("Kechirasiz, bu kod uchun video topa olmadim. Iltimos, yana bir bor urinib ko'ring.")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
