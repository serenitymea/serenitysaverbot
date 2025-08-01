"""скачать видео"""
import os
import asyncio
import yt_dlp
from yt_dlp.utils import DownloadError, ExtractorError, UnsupportedError
from aiogram import types

class VideoDownloader:
    """класс для закачки"""
    def __init__(self, url: str, message: types.Message):
        self.url = url
        self.message = message

    def download(self) -> tuple[str | None, str | None]:
        """закачка"""
        videoerror = None
        videofilename = None

        os.makedirs("downloads", exist_ok=True)
        output = os.path.join("downloads", 'video.%(ext)s')

        ydlo = {
            'outtmpl': output,
            'format': 'best',
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            }]
        }

        try:
            with yt_dlp.YoutubeDL(ydlo) as ydl:
                info = ydl.extract_info(self.url, download=True)
                filename = ydl.prepare_filename(info)
                ffilename = os.path.splitext(filename)[0] + '.mp4'
                if os.path.exists(ffilename):
                    videofilename = ffilename
        except (DownloadError, ExtractorError, UnsupportedError):
            videoerror = "ошибка при загр"
        except asyncio.TimeoutError:
            videoerror = "превышено время ожидания при загр"

        return videofilename, videoerror
