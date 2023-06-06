"""
This module provides functionality for downloading a YouTube playlist using
PyTube and multiprocessing.
"""

import multiprocessing as mp
from pathlib import Path

from pytube import Playlist

from controller.sanitize_path import sanitize_path
from controller.time_it import time_it
from controller.download_video_hq import download_video_hq


@time_it
def download_playlist(playlist_url: str):
    """
    Download a youtube playlist.

    Args:
        playlist_url (str): The URL of the playlist to download.

    Returns:
        None
    """
    playlist = Playlist(playlist_url)
    output_path = Path(sanitize_path(playlist.title) + " - " + playlist.playlist_id)
    output_path.mkdir(exist_ok=True)

    # Make temporal directory for downloading the streams.
    tmp_path = Path(output_path / "tmp")
    tmp_path.mkdir(exist_ok=True)

    print(f"Downloading {len(playlist.videos)} videos from {playlist.title}")
    with mp.Pool() as pool:
        pool.starmap(
            download_video_hq, [(video, output_path) for video in playlist.videos]
        )

    # Delete the temporal directory
    tmp_path.rmdir()
