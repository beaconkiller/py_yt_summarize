from faster_whisper import WhisperModel
import os
import asyncio
from services.SrvRecord import SrvRecord
from services.SrvTranslate import SrvTranslate
from services.SrvYtDownload import SrvYtDownload
from services.SrvHelper import SrvHelper

def main():

    # SrvTranslate.runTest()
    
    arr_to_search = [
        "ribu",
        "harga",
        "menit",
        "jam",
        "operasional",
        "buka",
        "tutup",
        "tiket",
        # ============
        "price",
        "close",
        "closes",
        "open",
        "opens",
        "rupiah",
        "rupees",
        "ticket",        
    ]
    
    arr_links = [
        "https://www.youtube.com/watch?v=Tq0EHwRYnmg",
        "https://www.youtube.com/watch?v=j_pxrIv7vCk",
        "https://www.youtube.com/watch?v=upnbKrYa7BE"
        # "https://www.youtube.com/watch?v=u-AUW72Rs1o" # DEBUG VIDEO        
    ]

    SrvTranslate.processVideo(arr_links, arr_to_search)
    


main()