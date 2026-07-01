# THIS ENTIRE FILE WAS VOBE CODED BECAUSE I FUCKING HATE REGEX AND THE OTHER SOLUTIONS
# ARE TOO SLOW BECAUSE I DON'T HAVE A GPU.

import re
import sys
import json

TIME_TAG_RE = re.compile(r'<(\d{2}:\d{2}:\d{2}\.\d{3})>')
CUE_TIME_RE = re.compile(r'^(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})')
TS_RE = re.compile(r'(\d{2}):(\d{2}):(\d{2})\.(\d{3})')

def ts_to_seconds(ts):
    h, m, s, ms = TS_RE.match(ts).groups()
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000

def parse_line_to_words(line, cue_start):
    """Parse one caption line (may contain <c> word tags) into [(word, ts_seconds), ...]"""
    parts = re.split(r'(<\d{2}:\d{2}:\d{2}\.\d{3}>)', line)
    current_ts = cue_start
    words = []
    buf = ''
    for part in parts:
        m = TIME_TAG_RE.match(part)
        if m:
            if buf.strip():
                for w in re.sub(r'</?c>', '', buf).split():
                    words.append((w, current_ts))
            current_ts = m.group(1)
            buf = ''
        else:
            buf += part
    if buf.strip():
        for w in re.sub(r'</?c>', '', buf).split():
            words.append((w, current_ts))
    return words

def extract_word_timestamps(vtt_path):
    with open(vtt_path, encoding='utf-8') as f:
        content = f.read()

    blocks = content.split('\n\n')
    result = []
    prev_words = []  # plain word list (lowercased) from the last processed growing line

    for block in blocks:
        lines = [l for l in block.strip().split('\n') if l.strip()]
        if not lines or '-->' not in lines[0]:
            continue
        m = CUE_TIME_RE.match(lines[0])
        if not m:
            continue
        cue_start = m.group(1)
        text_lines = lines[1:]
        if not text_lines:
            continue
        last_line = text_lines[-1]

        parsed = parse_line_to_words(last_line, cue_start)
        plain = [w.lower() for w, _ in parsed]

        # Does the new line continue the previous growing line (prefix match)?
        if plain[:len(prev_words)] != prev_words:
            prev_words = []  # new paragraph/context; start counting from scratch

        new_words = parsed[len(prev_words):]
        for word, ts in new_words:
            result.append((word, ts_to_seconds(ts)))
        prev_words = plain

    return result
