"""This script downloads a youtube video."""
from pytube import YouTube
import multiprocessing as mp
from pathlib import Path
from time_it import time_it
from url_generator import url_generator

@time_it
def download_video(url):
    """Download a youtube video."""
    yt = YouTube(url)
    yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()

@time_it
def main():
    URL_PATH = 'urls.txt'
    path = Path(URL_PATH)
    for url in url_generator(path):
        mp.Process(target=download_video, args=(url,)).start()


if __name__ == '__main__':    
    main()