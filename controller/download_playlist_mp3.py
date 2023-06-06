"""This module provides a function to download a youtube playlist in mp3 format."""

import multiprocessing as mp
from pathlib import Path

from pytube import Playlist

from controller.download_audio_yt import download_audio_yt
from controller.sanitize_path import sanitize_path
from controller.time_it import time_it


@time_it
def download_playlist_mp3(playlist_url: str):
    """Download a youtube playlist."""
    playlist = Playlist(playlist_url)
    output_path = Path(sanitize_path(playlist.title) + " - " + playlist.playlist_id)
    output_path.mkdir(exist_ok=True)

    # Make temporal directory for downloading the streams.
    tmp_path = Path(output_path / "tmp")
    tmp_path.mkdir(exist_ok=True)

    print(f"Downloading {len(playlist.videos)} videos from {playlist.title}")
    with mp.Pool() as pool:
        pool.starmap(
            download_audio_yt, [(video, output_path) for video in playlist.videos]
        )

    # Delete the temporal directory
    print("Deleting temporal files...")
    tmp_path.rmdir()
