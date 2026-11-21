from settings import TOKEN
import asyncio
from aiogram import Bot, Dispatcher
from handlers.routes import router


dp = Dispatcher()

dp.include_router(router)


async def main():
    bot = Bot(token=TOKEN)

    print("start")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())