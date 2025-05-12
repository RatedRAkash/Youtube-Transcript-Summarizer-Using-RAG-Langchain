import re

def extract_youtube_video_id(url):
    pattern = r"(?:v=|\/embed\/|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None
