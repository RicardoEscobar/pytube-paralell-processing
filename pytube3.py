import multiprocessing as mp
import os
from pathlib import Path

from pytube import Playlist, YouTube

from controller.sanitize_path import sanitize_path
from controller.time_it import time_it
from controller.to_mp3 import to_mp3


@time_it
def download_video_yt(yt: YouTube, output_path: Path = Path()):
    """Download a youtube video."""
    yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(output_path=output_path)

@time_it
def download_video_hq(yt: YouTube, output_path: Path = Path()):
    """Download a youtube video at the highest quality."""
    # Get temporal directory for downloading the streams.
    tmp_path = Path(output_path / 'tmp')

    # get all DASH video streams
    dash_streams = yt.streams.filter(type='video', subtype='mp4', progressive=False)

    # sort by resolution or bitrate to get the highest quality stream
    highest_quality = dash_streams.order_by('resolution').desc().first()

    # download the stream
    video_stream = highest_quality.download(output_path=tmp_path)

    # get all DASH audio streams
    dash_streams = yt.streams.filter(type='audio', subtype='webm', progressive=False)

    # sort by bitrate to get the highest quality stream
    highest_quality = dash_streams.order_by('abr').desc().first()

    # download the stream
    audio_stream = highest_quality.download(output_path=tmp_path)

    # Merge the audio and video streams
    output_file_path = Path(output_path, sanitize_path(yt.title) + '.mp4')
    output_file_path = output_file_path.resolve()
    
    os.system(f'ffmpeg -hide_banner -loglevel error -i "{video_stream}" -i "{audio_stream}" -c copy "{output_file_path}"')

    # Delete the temporal files
    Path(video_stream).unlink()
    Path(audio_stream).unlink()

@time_it
def download_audio_yt(yt: YouTube, output_path: Path = Path()):
    """Download a youtube audio."""
    
    
    # Create tmp directory for downloading the streams.
    tmp_path = Path(output_path / 'tmp')
    tmp_path.mkdir(exist_ok=True)

    # get all DASH audio streams
    filename = yt.streams.filter(only_audio=True).order_by('abr').desc().first().download(output_path=tmp_path)

    to_mp3(Path(filename), output_path)

@time_it
def download_playlist(url):
    """Download a youtube playlist."""
    playlist = Playlist(url)
    output_path = Path(sanitize_path(playlist.title) + ' - ' + playlist.playlist_id)
    output_path.mkdir(exist_ok=True)

    # Make temporal directory for downloading the streams.
    tmp_path = Path(output_path / 'tmp')
    tmp_path.mkdir(exist_ok=True)

    print(f'Downloading {len(playlist.videos)} videos from {playlist.title}')
    pool = mp.Pool()
    pool.starmap(download_video_hq, [(video, output_path) for video in playlist.videos])

    # Delete the temporal directory
    tmp_path.rmdir()

def download_playlist_mp3(url):
    """Download a youtube playlist."""
    playlist = Playlist(url)
    output_path = Path(sanitize_path(playlist.title) + ' - ' + playlist.playlist_id)
    output_path.mkdir(exist_ok=True)

    # Make temporal directory for downloading the streams.
    tmp_path = Path(output_path / 'tmp')
    tmp_path.mkdir(exist_ok=True)

    print(f'Downloading {len(playlist.videos)} videos from {playlist.title}')
    pool = mp.Pool()
    pool.starmap(download_audio_yt, [(video, output_path) for video in playlist.videos])

    # Delete the temporal directory
    print('Deleting temporal files...')
    tmp_path.rmdir()

@time_it
def main():
    print('Number of processors: ', mp.cpu_count())
    URL_PATH = 'https://youtu.be/4I71ln-rImk'
    # download_playlist(URL_PATH)
    download_audio_yt(YouTube(URL_PATH))
    # download_playlist_mp3(URL_PATH)


if __name__ == '__main__':
    main()
