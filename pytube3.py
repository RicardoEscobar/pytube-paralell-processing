from typing import List
import multiprocessing as mp
from pytube import YouTube, Playlist
from pathlib import Path
from time_it import time_it
from to_mp3 import to_mp3
from sanitize_filename import sanitize_filename

@time_it
def download_video_yt(yt: YouTube, output_path: Path = Path()):
    """Download a youtube video."""
    yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(output_path=output_path)

@time_it
def download_audio_yt(yt: YouTube, output_path: Path = Path()):
    """Download a youtube audio."""
    filename = yt.streams.filter(only_audio=True).order_by('abr').desc().first().download(output_path=output_path)
    to_mp3(Path(filename))

    
@time_it
def download_playlist(url):
    """Download a youtube playlist."""
    playlist = Playlist(url)
    output_path = Path(playlist.title + ' - ' + playlist.playlist_id)
    output_path.mkdir(exist_ok=True)

    print(f'Downloading {len(playlist.videos)} videos from {playlist.title}')
    pool = mp.Pool()
    pool.starmap(download_audio_yt, [(video, output_path) for video in playlist.videos])

@time_it
def main():
    print('Number of processors: ', mp.cpu_count())
    URL_PATH = 'https://youtube.com/playlist?list=PLZOGNlgi8GGncx1etrSzhrHM1GqoFindD'
    download_playlist(URL_PATH)


if __name__ == '__main__':
    main()
