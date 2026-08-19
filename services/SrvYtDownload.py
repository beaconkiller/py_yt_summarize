import asyncio
from datetime import datetime
import os
import time
import yt_dlp
import asyncio
from pathlib import Path 

class SrvYtDownload:    
    
    async def getAudioBatch(self, arr_url):
        # arr_url = [
        #     "https://www.youtube.com/watch?v=Tq0EHwRYnmg",
        #     "https://www.youtube.com/watch?v=j_pxrIv7vCk",
        #     "https://www.youtube.com/watch?v=upnbKrYa7BE"
        # ]
        
        tasks = [
            asyncio.to_thread(self.getAudio, url) 
            for url in arr_url
        ]
        
        await asyncio.gather(*tasks)
    
    
    
    
    
    
    async def getAudioBatchWithSessId(self, arr_url, session_id):

        target_dir = os.path.join(os.getcwd(), "file_storage", "session_result", session_id)
        
        Path(target_dir).mkdir(parents=True, exist_ok=True)
        
        # arr_url = [
        #     "https://www.youtube.com/watch?v=Tq0EHwRYnmg",
        #     "https://www.youtube.com/watch?v=j_pxrIv7vCk",
        #     "https://www.youtube.com/watch?v=upnbKrYa7BE"
        # ]
        
        tasks = [
            asyncio.to_thread(self.getAudioWithSessId, url, session_id) 
            for url in arr_url
        ]
        
        await asyncio.gather(*tasks)
    
    
    
    
    
    
    def getAudioWithSessId(self, video_url, session_id):
        url = video_url

        options = {
            "format": "bestaudio",
            "outtmpl": "file_storage/session_result/"+session_id+"/%(id)s(__)%(title)s.%(ext)s",

            "extractor_args": {
                "youtube": {
                    "player_client": ["web_embedded", "web", "tv"]
                }
            },

            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])
    
    
    
    
    
    
    def getAudio(self, video_url):
        url = video_url

        options = {
            "format": "bestaudio",
            "outtmpl": "file_storage/audio_result/%(id)s(__)%(title)s.%(ext)s",

            "extractor_args": {
                "youtube": {
                    "player_client": ["web_embedded", "web", "tv"]
                }
            },

            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])






SrvYtDownload = SrvYtDownload()