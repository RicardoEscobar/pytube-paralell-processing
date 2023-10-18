"""
This module provides functionality for downloading a YouTube playlist using
PyTube and multiprocessing.
"""

import concurrent.futures
from pathlib import Path

from pytube import Playlist
from typing import List

from controller.sanitize_path import sanitize_path
from controller.time_it import time_it
from controller.download_video_hq import download_video_hq


@time_it
def download_playlist(playlist_url: str, output_dir: str = None) -> List[str]:
    """
    Download a youtube playlist.

    Args:
        playlist_url (str): The URL of the playlist to download.
        output_dir (str): The path to the output directory.
    Returns:
        A list of the paths of the downloaded videos.
    """

    # Create Playlist object from the url string.
    playlist = Playlist(playlist_url)

    # Get the output directory.
    output_dir = Path(output_dir)
    output_dir = output_dir.resolve()

    # Create a directory for the playlist.
    playlist_dir = Path(output_dir / sanitize_path(playlist.title))
    playlist_dir.mkdir(parents=True, exist_ok=True)

    # Get the URLs of all the videos in the playlist.
    video_urls = playlist.video_urls

    # Download the videos in parallel.
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(
            download_video_hq, video_urls, [playlist_dir] * len(video_urls)
        )

    # Return the paths of the downloaded videos.
    return list(results)
