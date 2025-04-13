from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import asyncio
import requests

TOKEN = 'ВАШ_ТОКЕН'
WEATHER_API_KEY = 'ВАШ_КЛЮЧ'

bot = Bot(TOKEN)
dp = Dispatcher()

@dp.message(Command('start'))
async def start_command(message: types.Message):
    await message.answer("Привет! Я бот погоды. Используй /weather Москва")

@dp.message(Command('weather'))
async def weather_command(message: types.Message):
    try:
        city = message.text.split(maxsplit=1)[1]
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru'
        response = requests.get(url)
        data = response.json()

        if data.get('cod') != 200:
            await message.answer(f"Ошибка: {data.get('message', 'Неизвестная ошибка')}")
            return

        weather_info = (
            f"Погода в {data['name']}:\n"
            f"☁️ {data['weather'][0]['description'].capitalize()}\n"
            f"🌡 Температура: {data['main']['temp']:.1f}°C\n"
            f"💧 Влажность: {data['main']['humidity']}%\n"
            f"🌬 Ветер: {data['wind']['speed']:.1f} м/с"
        )
        await message.answer(weather_info)

    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())