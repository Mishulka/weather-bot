import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import os

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv('BOT_TOKEN', '7975662105:AAFNU7izDQK6u6O7hDGMKsL2t783AqmG1HI')

async def main():
    try:
        logger.info("Starting bot initialization...")
        
        # Инициализация бота внутри главной event loop
        bot = Bot(token=TOKEN)
        dp = Dispatcher()

        @dp.message(Command('start'))
        async def start(message: types.Message):
            await message.answer("Бот работает! Используйте /weather Москва")

        @dp.message(Command('weather'))
        async def weather(message: types.Message):
            try:
                city = message.text.split(maxsplit=1)[1]
                await message.answer(f"Запрос погоды для {city} получен!")
            except IndexError:
                await message.answer("Укажите город: /weather Москва")

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