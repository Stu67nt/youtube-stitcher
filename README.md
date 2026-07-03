# YouTube Stitcher

Have you ever seen those videos where people edit clips of YouTubers saying things to make it sound like they are saying
something else? Well that is what this project is! You can clip together videos of things said in Veritasium videos 
together to say whatever!

---
## Video Demo

---

## Usage Tutorial
Download the zip from the GitHub releases section and then extract it and run the main.exe!  
Once running Just enter the phrase you want to be clipped together and it will do everything for you!  
Note that once it is running it can take quite a while to process (due to needing to download lots of clips) especially 
for longer clips, so I reccomend only doing short sentences containing common phases if you just want to see it work.


## AI Usage
The enitre "extract_word_timestamps.py" file was vibe coded by claude as it required a shit ton of regex and file filtering which I do NOT want to touch with a 10-foot pole. Other solutions for this such as subititling the videos using whisper myself are too slow due to no dedicated GPU. I also used it for helping me with the algorithm to comb through the time stamps and decide the best rolling window of words. 
