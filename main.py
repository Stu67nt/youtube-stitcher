import yt_dlp
import time
import random

"""
Scrape all subtitles
Create db of individual words with video id and time stamps?

"""
def extract_ids():
    download_args = {
        'extract_flat': 'in_playlist',
        'print_to_file': {
            'video': [('id', 'video_ids.txt')]
        }
    }

    with yt_dlp.YoutubeDL(download_args) as ydl:
        info = ydl.extract_info("www.youtube.com/@JackSucksAtLife", download=False)

def extract_subtitles():
    downloader_args = {
        'skip_download': True,
        'subtitleslangs': ['en-orig'],
        'writeautomaticsub': True,
        'writesubtitles': True,
        'outtmpl': {'default': 'JSALsubtitles\\%(id)s'}
    }
    start = 123  # First id not attempted
    with yt_dlp.YoutubeDL(downloader_args) as ydl:
        with open("video_ids.txt", 'r') as f:
            ids = f.readlines()
            for id_num in range(start, len(ids)):
                ydl.download(ids[id_num][:-1])
                print(f"Downloaded subtitle in line {id_num+1}")


