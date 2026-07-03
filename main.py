import yt_dlp
import time
import random
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
        info = ydl.extract_info("https://www.youtube.com/@veritasium", download=False)

def extract_subtitles():
    downloader_args = {
        'skip_download': True,
        'subtitleslangs': ['en.orig'],
        'writeautomaticsub': True,
        'outtmpl': {'default': 'subtitles\\%(id)s'}
    }
    with yt_dlp.YoutubeDL(downloader_args) as ydl:
        with open("video_ids.txt", 'r') as f:
            ids = f.readlines()
            for id_num in range(0, len(ids)):
                try:
                    ydl.download(ids[id_num][:-1])
                    print(f"Downloaded subtitle in line {id_num+1}")
                    results = extract_word_timestamps.extract_word_timestamps(f"subtitles\\{ids[id_num][:-1]}.en-orig.vtt")
                    text = json.dumps(results, indent=2)
                    with open(f"jsonsubtitles\\{ids[id_num][:-1]}.json", 'w') as f:
                        f.write(text)
                except Exception as e:
                    print(e)
                time.sleep(random.uniform(1.5, 4))

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

def calc_best_duration(all_words, start_i, match_len):
    end_i = start_i + match_len
    if end_i < len(all_words):
        return all_words[end_i][1] - all_words[start_i][1]
    return (all_words[-1][1] - all_words[start_i][1]) + 1

def find_word_stamps(text):
    text = text.translate(str.maketrans('', '', "%&()*+,-./:;<=>?@[\]^_`{|}~")).lower()
    text_lst = list(text.split(" "))
    dir_list = os.listdir("jsonsubtitles")
    clip_seq = []

    words_complete = 0
    while words_complete < len(text_lst):
        best_len = 0
        best_duration = -1
        best_fname = None
        best_start_i = None

        for f_name in dir_list:
            with open(f"jsonsubtitles\\{f_name}", 'r') as f:
                all_words = json.load(f)
                for i, word in enumerate(all_words):
                    if word[0] == text_lst[words_complete]:
                        match_len = 0
                        while ((words_complete+match_len < len(text_lst) and i+match_len < len(all_words) and
                                text_lst[words_complete+match_len] == all_words[i+match_len][0])):
                            match_len += 1
                        if match_len > best_len and match_len > 1:
                            best_len = match_len
                            best_fname = f_name
                            best_start_i = i
                            best_duration = calc_best_duration(all_words, i, match_len)
                        elif best_len <= 1:
                            duration = calc_best_duration(all_words, i, match_len)
                            if best_duration <= duration <= (match_len * 0.8):
                                best_len = match_len
                                best_duration = duration
                                best_fname = f_name
                                best_start_i = i

        if best_len == 0:
            clip_seq.append([text_lst[words_complete], None, None, None])
            print(f"failed to find {text_lst[words_complete]}")
            words_complete += 1
        else:
            words = json.load(open(f"jsonsubtitles\\{best_fname}", 'r'))
            start_time = words[best_start_i][1]
            end_i = best_start_i + best_len
            if end_i < len(words):
                end_time = words[end_i][1]
            else:
                end_time = words[end_i - 1][1] + 1
            phrase = " ".join(text_lst[words_complete:words_complete+best_len])
            clip_seq.append([phrase, best_fname, start_time, end_time])
            words_complete += best_len

        print(f"{words_complete}/{len(text_lst)}")
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
                try:
                    download_vid_timespan(id, start, end, word)
                    time.sleep(random.randint(2,8))
                except Exception as e:
                    time.sleep(25)
                    print(e)
                    download_vid_timespan(id, start, end, word)
                    time.sleep(random.randint(2, 8))

def merge_clips(clip_seq):
    dir_list = os.listdir("temp_clips")
    clip_lst = []
    for phrase_key in clip_seq:
        phrase = phrase_key[0]
        for i in range(len(dir_list)):
            if dir_list[i].split(".")[0] == phrase:
                clip_lst.append(moviepy.VideoFileClip(f"temp_clips\\{dir_list[i]}"))
    final = moviepy.concatenate_videoclips(clip_lst)
    final.write_videofile(f"{random.randint(1000,9999)}.mp4")
    files_to_delete = os.listdir("temp_clips")
    for file in files_to_delete:
        os.remove(f"temp_clips/{file}")

def make_clip(text):
    print("Finding word locations")
    clip_seq = find_word_stamps(text)
    print("Downloading the clips")
    compile_clips(clip_seq)
    print("Creating the video")
    merge_clips(clip_seq)

def main():
    while True:
        print("Click CRTL+C to exit!")
        message = input("Enter the message you would like to be generated in video form: ")
        make_clip(message)

if __name__ == "__main__":
    main()