"""
скачать видео

"""
import os
import asyncio
import yt_dlp
from yt_dlp.utils import DownloadError, ExtractorError, UnsupportedError
from aiogram import types

class VideoDownloader:
    """клас для закачки"""
    def __init__(self, url: str, message: types.Message):
        self.url = url
        self.message = message

    def download(self) -> tuple[str | None, str | None]:
        """закачка"""
        videoerror = None
        videofilename = None

        download_dir = "downloads"
        print(f"Пытаемся создать папку: {download_dir}")
        os.makedirs(download_dir, exist_ok=True)
        print(f"Папка {download_dir} успешно создана или уже существует.")

        output = os.path.join(download_dir, 'video.%(ext)s')

        ydl_opts = {
            'outtmpl': output,
            'format': 'best',
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            }]
        }
        try:
            print(f"Начинаем загрузку видео: {self.url}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=True)
                filename = ydl.prepare_filename(info)
                print(f"Полученное имя файла: {filename}")
                ffilename = os.path.splitext(filename)[0] + '.mp4'
                if os.path.exists(ffilename):
                    videofilename = ffilename
                    print(f"Файл найден: {ffilename}")

        except (DownloadError, ExtractorError, UnsupportedError) as e:
            videoerror = f"Ошибка при загрузке видео: {e}"
            print(videoerror)
        except asyncio.TimeoutError:
            videoerror = "Превышено время ожидания при загрузке видео."
            print(videoerror)
        return videofilename, videoerror
