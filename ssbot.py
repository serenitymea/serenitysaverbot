"""
запуск бота
"""
import os
import asyncio

from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from aiogram.client.bot import DefaultBotProperties
from dotenv import load_dotenv

from url import ContentTypeChecker
from downloadvid import VideoDownloader

load_dotenv()

TOKEN = os.getenv("TOKEN")

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()
router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    """приветствие"""
    fname = message.from_user.full_name
    await message.answer(
        f"Привет, {fname}! Я могу скачивать видео с разных соц. сетей по ссылке!"
    )

@router.message()
async def handle_download(message: Message):
    """хендлер для скачивания видео"""
    if not message.text:
        await message.answer("пожалуйста, отправьте ссылку")
        return

    url = message.text.strip()

    checker = ContentTypeChecker()
    dowvid = VideoDownloader(url, message)

    contenttype = await asyncio.to_thread(checker.urltype, url)

    if contenttype == "video":
        videofilename, videoerror = await asyncio.to_thread(dowvid.download)
        if videofilename and os.path.exists(videofilename):
            await message.answer("загрузка видео...")
            try:
                await message.answer_video(FSInputFile(videofilename))
            except Exception:
                await message.answer("ошибка при отправке видео")
            finally:
                os.remove(videofilename)
        else:
            await message.answer(f"ошибка при скачивании: {videoerror or 'неизвестная ошибка'}")
    else:
        await message.answer("cсылка не на видео")

async def main():
    """запуск бота"""
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
