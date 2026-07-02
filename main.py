import yt_dlp
import time
import random
import string
import json
import os
import extract_word_timestamps
import moviepy

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
    start = 142
    with yt_dlp.YoutubeDL(downloader_args) as ydl:
        with open("video_ids.txt", 'r') as f:
            ids = f.readlines()
            for id_num in range(start, len(ids)):
                ydl.download(ids[id_num][:-1])
                print(f"Downloaded subtitle in line {id_num+1}")
                try:
                    results = extract_word_timestamps.extract_word_timestamps(f"JSALsubtitles\\{ids[id_num][:-1]}.en-orig.vtt")
                    text = json.dumps(results, indent=2)
                    with open(f"JSALjsonsubtitles\\{ids[id_num][:-1]}.json", 'w') as f:
                        f.write(text)
                except Exception as e:
                    print(e)

def exact_time_stamp_parser(time_stamp):
    time_split = time_stamp.split(':')
    return float((int(time_split[0]) * 3600) + (int(time_split[1]) * 60) + (float(time_split[2])))

def download_vid_timespan(id, start, end, word):
    # TODO: Account for slight ffmpeg variation
    # start_num = exact_time_stamp_parser(start)
    # end_num = exact_time_stamp_parser(end)
    downloader_args = {
        'download_ranges': yt_dlp.utils.download_range_func([], [[start, end]],),
        'force_keyframes_at_cuts': True,
        'outtmpl': {'default': f'temp_clips\\{word}'}
    }
    with yt_dlp.YoutubeDL(downloader_args) as ydl:
        ydl.download(id)

def find_word_stamps(text):
    text = text.translate(str.maketrans('', '', string.punctuation)).lower()
    text_lst = list(set(text.split(" ")))
    print(text_lst)
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

def create_clip_sequence_list(text, text_lst):
    filt_text = text.translate(str.maketrans('', '', string.punctuation)).lower()
    filt_text_lst = list(filt_text.split(" "))
    clip_seq = []
    for word in filt_text_lst:
        for entry in text_lst:
            if word == entry[0]:
                clip_seq.append(entry)
    return clip_seq

def compile_clips(clips_times_lst):
    for clip in clips_times_lst:
        dir_list = os.listdir("temp_clips")
        print(dir_list)
        if clip[1] != None:
            word = clip[0]
            id = clip[1][:-5]
            start = clip[2]
            end = clip[3]
            if f"{word}.webm" not in dir_list:
                download_vid_timespan(id, start, end, word)

def merge_clips(text):
    filt_text = text.translate(str.maketrans('', '', string.punctuation)).lower()
    filt_text_lst = list(filt_text.split(" "))
    dir_list = os.listdir("temp_clips")
    clip_lst = []
    print()
    for word in filt_text_lst:
        if f"{word}.webm" in dir_list:
            clip_lst.append(moviepy.VideoFileClip(f"temp_clips\\{word}.webm"))
    print(len(clip_lst))
    final = moviepy.concatenate_videoclips(clip_lst)
    final.write_videofile(f"{random.randint(1000,9999)}.mp4")

def make_clip(text):
    word_dic = find_word_stamps(text)
    clip_seq = create_clip_sequence_list(text, word_dic)
    compile_clips(clip_seq)
    merge_clips(text)


make_clip()