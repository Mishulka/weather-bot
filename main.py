from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import asyncio
import requests

TOKEN = '7975662105:AAFNU7izDQK6u6O7hDGMKsL2t783AqmG1HI'
WEATHER_API_KEY = '5d417f360a5292ed2ba1329604e9895e'

bot = Bot(TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command('start'))
async def start_command(message: types.Message):
    await message.answer("Привет! Я бот погоды. Используй /weather Москва или /getid для ID чата")

# Обработчик команды /getid
@dp.message(Command('getid'))
async def get_chat_id(message: types.Message):
    chat_id = message.chat.id
    chat_type = message.chat.type
    await message.reply(
        f"🔍 Информация о чате:\n"
        f"Тип: {chat_type}\n"
        f"ID: `{chat_id}`\n\n"
        f"Для добавления в ALLOWED_GROUPS используйте:\n"
        f"`ALLOWED_GROUPS = [{chat_id}]`",
        parse_mode="Markdown"
    )

# Обработчик команды /weather
@dp.message(Command('weather'))
async def weather_command(message: types.Message):
    try:
        city = message.text.split(maxsplit=1)[1]
        await process_weather_request(message, city)
    except IndexError:
        await message.reply("Пожалуйста, укажите город: /weather Москва")

# Общая функция обработки погоды
async def process_weather_request(message: types.Message, city: str):
    try:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city},RU&appid={WEATHER_API_KEY}&units=metric&lang=ru'
        response = requests.get(url)
        weather_data = response.json()
        
        if weather_data.get('cod') != 200:
            error_msg = weather_data.get('message', 'Неизвестная ошибка')
            await message.reply(f"Ошибка: {error_msg}")
            return
        
        temp = weather_data['main']['temp']
        temp_feel = weather_data['main']['feels_like']
        humidity = weather_data['main']['humidity']
        wind = weather_data['wind']['speed']
        description = weather_data['weather'][0]['description']
        city_name = weather_data.get('name', city)
        
        await message.reply(
            f'Погода в городе {city_name}:\n'
            f'☁️ {description.capitalize()}\n'
            f'🌡 Температура: {temp:.1f}°C (ощущается как {temp_feel:.1f}°C)\n'
            f'💧 Влажность: {humidity}%\n'
            f'🌬 Ветер: {wind:.1f} м/с'
        )
    except Exception as e:
        await message.reply(f"Ошибка: {str(e)}")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())