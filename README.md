# YouTube Stitcher

Have you ever seen those videos where people edit clips of YouTubers saying things to make it sound like they are saying
something else? Well, that is what this project is! You can clip together videos of things said in Veritasium videos 
together to say whatever!

Why did I make it? I just thought it would be funny after seeing people spend ages making those "YouTuber sings X song videos"
to try to automate making those. Turns out MUCH harder than I anticipated to completely automate.

---
## Example Output Demo
https://github.com/user-attachments/assets/79b1e1f2-163a-405a-9940-8038619dcdae

---

## Usage Tutorial
Download the zip from the GitHub releases section, and then extract it and run the main.exe!  
Once running Just enter the phrase you want to be clipped together, and it will do everything for you!  
Note that once it is running, it can take quite a while to process (due to needing to download lots of clips), especially 
for longer clips, so I recommend only doing short sentences containing common phrases if you just want to see it work.

## Limitations
 - Right now, the build version only supports Veritasium versions; the code does exist to allow it to support more with a bit of modification. Could be a future upgrade, but as of right now, I don't intend to keep working on this.
 - The program is kinda shit at detecting silences in the clips and splicing the clips properly, which is another significant issue I tried and gave up on solving. The easiest fix is to increase the dataset, but it won't solve the core underlying issue, which is much more work. This program has already gone through quite a few iterations of improvement.

## AI Usage
The entire "extract_word_timestamps.py" file was vibe-coded by Claude as it required a shit ton of regex and file filtering, which I do NOT want to touch with a 10-foot pole. Other solutions for this, such as subtitling the videos using Whisper myself, are too slow due to no dedicated GPU. I also used it to help me with the algorithm to comb through the time stamps and decide the best rolling window of words. 
