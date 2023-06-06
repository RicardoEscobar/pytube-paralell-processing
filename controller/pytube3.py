import multiprocessing as mp
from pathlib import Path
from pytube import Playlist, YouTube

from controller.sanitize_path import sanitize_path
from controller.time_it import time_it
from controller.to_mp3 import to_mp3


@time_it
def download_playlist(playlist_url: str):
    """Download a youtube playlist."""
    playlist = Playlist(playlist_url)
    output_path = Path(sanitize_path(playlist.title) + " - " + playlist.playlist_id)
    output_path.mkdir(exist_ok=True)

    # Make temporal directory for downloading the streams.
    tmp_path = Path(output_path / "tmp")
    tmp_path.mkdir(exist_ok=True)

    print(f"Downloading {len(playlist.videos)} videos from {playlist.title}")
    pool = mp.Pool()
    pool.starmap(download_video_hq, [(video, output_path) for video in playlist.videos])

    # Delete the temporal directory
    tmp_path.rmdir()


def download_playlist_mp3(playlist_url: str):
    """Download a youtube playlist."""
    playlist = Playlist(playlist_url)
    output_path = Path(sanitize_path(playlist.title) + " - " + playlist.playlist_id)
    output_path.mkdir(exist_ok=True)

    # Make temporal directory for downloading the streams.
    tmp_path = Path(output_path / "tmp")
    tmp_path.mkdir(exist_ok=True)

    print(f"Downloading {len(playlist.videos)} videos from {playlist.title}")
    pool = mp.Pool()
    pool.starmap(download_audio_yt, [(video, output_path) for video in playlist.videos])

    # Delete the temporal directory
    print("Deleting temporal files...")
    tmp_path.rmdir()


@time_it
def main():
    print("Number of processors: ", mp.cpu_count())
    URL_PATH = "https://youtu.be/4I71ln-rImk"
    # download_playlist(URL_PATH)
    download_audio_yt(YouTube(URL_PATH))
    # download_playlist_mp3(URL_PATH)


if __name__ == "__main__":
    main()
