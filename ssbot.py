"""
запуск бота
"""
import os
import logging
import asyncio
import sys

from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from aiogram.client.bot import DefaultBotProperties

from config import TOKEN
from url import ContentTypeChecker
from downloadvid import VideoDownloader

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format='%(asctime)s %(levelname)s %(message)s'
)

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
    logging.info("User started: %s", fname)
    await message.answer(
        f"Привет, {fname}! Я могу скачивать видео с разных соц. сетей по ссылке!"
        )

@router.message()
async def handle_download(message: Message):
    """хендлер для скачивания видео"""
    if not message.text:
        await message.answer("Пожалуйста, отправьте ссылку в виде текста.")
        return

    url = message.text.strip()
    logging.info("Received URL: %s", url)

    checker = ContentTypeChecker()
    dowvid = VideoDownloader(url, message)

    contenttype = await asyncio.to_thread(checker.urltype, url)
    logging.info("Content type detected: %s", contenttype)

    if contenttype == "video":
        videofilename, videoerror = await asyncio.to_thread(dowvid.download)
        logging.info("Download video returned: filename=%s, error=%s", videofilename, videoerror)
        if videofilename and os.path.exists(videofilename):
            await message.answer("Загрузка видео...")
            try:
                await message.answer_video(FSInputFile(videofilename))
                logging.info("Video file sent successfully: %s", videofilename)
            except (OSError, ValueError) as e:
                logging.error("Failed to send video file: %s", e)
                await message.answer("Ошибка при отправке видео.")
            finally:
                os.remove(videofilename)
                logging.info("Video file removed: %s", videofilename)
        else:
            await message.answer(
                f"Ошибка при скачивании видео: {videoerror or 'неизвестная ошибка'}"
            )
    else:
        await message.answer("Ссылка не является видео.")

async def main():
    """запуск бота"""
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
