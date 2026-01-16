from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.client.default import DefaultBotProperties
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
import os
from state import AddLang
from keyboard import lang_kb
from tarjimon import tarjimon
from ovoz import ovoz_yarat
import logging

logging.basicConfig(level=logging.INFO)

TOKEN = "8495751559:AAE0qwrCxpEasu2McMXHAo8YBC8L0Eq97F8"
ADMIN_ID = 5409624965

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher(storage=MemoryStorage())

user_texts = {}
languages = [
    ("🇷🇺 Rus", "ru"),
    ("🇺🇸 Ingliz", "en"),
    ("🇫🇷 Fransuz", "fr"),
    ("🇩🇪 Nemis", "de"),
    ("🇪🇸 Ispan", "es"),
    ("🇮🇹 Italya", "it"),
]

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(f"Salom {message.from_user.full_name}!\nMatn yuboring.")

@dp.message(Command("id"))
async def get_id(message: types.Message):
    await message.answer(f"Sizning ID: {message.from_user.id}")

@dp.message(Command("admin"))
async def admin_cmd(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ Admin emassiz!")
        return
    
    await message.answer("Til nomini yozing:")
    await state.set_state(AddLang.name)

@dp.message(AddLang.name)
async def get_lang_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Til kodini yozing:")
    await state.set_state(AddLang.code)

@dp.message(AddLang.code)
async def get_lang_code(message: types.Message, state: FSMContext):
    data = await state.get_data()
    languages.append((data["name"], message.text))
    await message.answer(f"✅ {data['name']} qo'shildi")
    await state.clear()

@dp.message(F.text)
async def get_text(message: types.Message):
    if message.text.startswith('/'):
        return
    
    user_texts[message.from_user.id] = message.text
    await message.answer("Tilni tanlang:", reply_markup=lang_kb(languages, page=0))

@dp.callback_query(F.data.startswith("page_"))
async def paginate(call: types.CallbackQuery):
    page = int(call.data.split("_")[1])
    await call.message.edit_reply_markup(reply_markup=lang_kb(languages, page))
    await call.answer()

@dp.callback_query(F.data == "page_info")
async def page_info(call: types.CallbackQuery):
    await call.answer("Sahifa haqida")

@dp.callback_query(F.data.startswith("lang_"))
async def choose_lang(call: types.CallbackQuery):
    user_id = call.from_user.id
    user_text = user_texts.get(user_id)
    
    if not user_text:
        await call.answer("❌ Matn yo'q")
        return
    
    target_lang = call.data.replace("lang_", "")
    
    try:
        await call.message.edit_reply_markup(reply_markup=None)
        
        tarjima_text = await tarjimon(user_text, target_lang)
        
        voice_file = await ovoz_yarat(tarjima_text, target_lang, user_id, call.id)
        
        if voice_file and os.path.exists(voice_file):
            voice = FSInputFile(voice_file)
            await call.message.answer_voice(voice=voice, caption=tarjima_text)
            os.remove(voice_file)
        else:
            await call.message.answer(f"Tarjima:\n{tarjima_text}")
            
    except:
        await call.message.answer("❌ Xatolik")
    
    await call.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())