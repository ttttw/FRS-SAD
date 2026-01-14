import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from flask import Flask
from threading import Thread

# =========================================================
# إعدادات البوت (تم وضع بياناتك هنا)
# =========================================================
API_TOKEN = '8350163121:AAEjhBXzm-uqDg4iUbpSerR35UGOK21vCVI'
ADMIN_ID = 5803355350
CHANNEL_ID = "@T777T55" 
# =========================================================

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
app = Flask('')

# سيرفر ويب للبقاء حياً 24 ساعة (Keep Alive)
@app.route('/')
def home():
    return "Bot is Running 24/7!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web)
    t.daemon = True
    t.start()

# دالة فحص الاشتراك الإجباري
async def is_subscribed(user_id: int):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ["member", "creator", "administrator"]
    except Exception as e:
        logging.error(f"Error checking sub: {e}")
        return False

# أمر /start
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    if await is_subscribed(user_id):
        await message.answer(f"أهلاً بك يا {message.from_user.first_name} في بوت صائد الفرص! 🔥\n\nأرسل اسم المنتج الذي تبحث عنه وسأقوم بمراقبته لك.")
    else:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="انضم للقناة أولاً ✅", url="https://t.me/T777T55")],
            [InlineKeyboardButton(text="تأكيد الاشتراك 🔄", callback_data="check_sub")]
        ])
        await message.answer(f"عذ
