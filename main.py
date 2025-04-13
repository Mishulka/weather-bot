from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import asyncio
import requests
from dotenv import load_dotenv
import os

# Загружаем переменные окружения
load_dotenv()

# Получаем токены из переменных окружения
TOKEN = os.getenv('BOT_TOKEN')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command('start'))
async def start(message: types.Message):
    await message.answer("Привет! Напиши /weather Москва")

@dp.message(Command('weather'))
async def weather(message: types.Message):
    try:
        city = message.text.split(maxsplit=1)[1]
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
        data = requests.get(url).json()
        
        if data['cod'] != 200:
            return await message.answer("Город не найден")
        
        await message.answer(
            f"Погода в {data['name']}:\n"
            f"☁️ {data['weather'][0]['description'].capitalize()}\n"
            f"🌡 {data['main']['temp']:.1f}°C\n"
            f"💧 Влажность: {data['main']['humidity']}%\n"
            f"🌬 Ветер: {data['wind']['speed']} м/с"
        )
    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())