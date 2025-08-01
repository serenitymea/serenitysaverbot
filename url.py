"""проверяет ссылка на фото или видео"""
import yt_dlp

class ContentTypeChecker:
    """класс для проверки"""
    def __init__(self):
        self.ydl_opts = {'quiet': True, 'skip_download': True}

    def urltype(self, url: str) -> str:
        """проверка"""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                ext = info.get('ext')
                return "video" if ext in ['mp4', 'mkv', 'webm'] else "other"
        except Exception:
            return "unknown"
