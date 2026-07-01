import yt_dlp
import time
import random
import string
import json
import os
import extract_word_timestamps

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
        'subtitleslangs': ['en.orig'],
        'writeautomaticsub': True,
        'outtmpl': {'default': 'JSALsubtitles\\%(id)s'}
    }
    start = 0  # First id not attempted
    with yt_dlp.YoutubeDL(downloader_args) as ydl:
        with open("video_ids.txt", 'r') as f:
            ids = f.readlines()
            for id_num in range(start, len(ids)):
                ydl.download(ids[id_num][:-1])
                print(f"Downloaded subtitle in line {id_num+1}")
                results = extract_word_timestamps.extract_word_timestamps(f"JSALsubtitles\\{ids[id_num][:-1]}.en-orig.vtt")
                text = json.dumps(results, indent=2)
                with open(f"JSALjsonsubtitles\\{ids[id_num][:-1]}.json", 'w') as f:
                    f.write(text)

def exact_time_stamp_parser(time_stamp):
    time_split = time_stamp.split(':')
    return float((int(time_split[0]) * 3600) + (int(time_split[1]) * 60) + (float(time_split[2])))

def download_vid_timespan(id, start, end):
    # TODO: Account for slight ffmpeg variation
    # start_num = exact_time_stamp_parser(start)
    # end_num = exact_time_stamp_parser(end)
    downloader_args = {
        'download_ranges': yt_dlp.utils.download_range_func([], [[start, end]],),
        'force_keyframes_at_cuts': True,
        'outtmpl': {'default': f'{random.randint(1,100)}'}
    }
    with yt_dlp.YoutubeDL(downloader_args) as ydl:
        ydl.download(id)

def find_word_stamps(text):
    text = text.translate(str.maketrans('', '', string.punctuation)).lower()
    text_lst = list(set(text.split(" ")))
    dir_list = os.listdir("JSALjsonsubtitles")
    for i_1 in range(0, len(text_lst)):
        for f_name in dir_list:
            with open(f"JSALjsonsubtitles\\{f_name}", 'r') as f:
                all_words = json.load(f)
                for i_2 in range(len(all_words)-1):
                    if text_lst[i_1] == all_words[i_2][0]:
                        text_lst[i_1] = [text_lst[i_1], f_name, all_words[i_2][1], all_words[i_2+1][1]]
        if type(text_lst[i_1]) is str:
            text_lst[i_1] = [text_lst[i_1], None, None, None]
    return text_lst


print(find_word_stamps("Bleach cour four is an epic ball man."))