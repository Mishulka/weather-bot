import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import os
import requests

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv('BOT_TOKEN', '7975662105:AAFNU7izDQK6u6O7hDGMKsL2t783AqmG1HI')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', '5d417f360a5292ed2ba1329604e9895e')

async def main():
    try:
        logger.info("Starting bot initialization...")
        
        bot = Bot(token=TOKEN)
        dp = Dispatcher()

        @dp.message(Command('start'))
        async def start(message: types.Message):
            await message.answer("Привет! Напиши /погода Москва")

        @dp.message(Command('погода'))
        async def weather(message: types.Message):
            try:
                city = message.text.split(maxsplit=1)[1]
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
                data = requests.get(url).json()
                
                if data['cod'] != 200:
                    return await message.answer("Город не найден")
                
                await message.answer(
                    f"Погода в {data['name']}:\n"
                    f"{data['weather'][0]['description'].capitalize()}\n"
                    f"Температура: {data['main']['temp']:.1f}°C\n"
                    f"Ощущается как: {data['main']['feels_like']:.1f}°C\n"
                    f"Влажность: {data['main']['humidity']}%\n"
                    f"Ветер: {data['wind']['speed']} м/с"
                )
                
            except IndexError:
                await message.answer("Укажите город: /weather Москва")
            except Exception as e:
                logger.error(f"Ошибка: {e}")
                await message.answer("Ошибка при запросе погоды")

        logger.info("Bot starting polling...")
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
        raise
    finally:
        logger.info("Bot stopped")
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())