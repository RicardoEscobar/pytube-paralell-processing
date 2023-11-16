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
def download_playlist(
    playlist_url: str, output_dir: str = None, start: int = 0, end: int = None
) -> List[str]:
    """
    Download a youtube playlist.

    Args:
        playlist_url (str): The URL of the playlist to download.
        output_dir (str): The path to the output directory.
        start (int): The index of the first video to download.
        end (int): The index of the last video to download.
    Returns:
        A list of the paths of the downloaded videos.
    """

    # Create Playlist object from the url string.
    playlist = Playlist(playlist_url)

    # Print how many videos are in the playlist.
    print(f"Number of videos in playlist: {len(playlist.video_urls)}")

    # Get the output directory.
    output_dir = Path(output_dir)
    output_dir = output_dir.resolve()

    # Create a directory for the playlist.
    playlist_dir = Path(output_dir / sanitize_path(playlist.title))
    playlist_dir.mkdir(parents=True, exist_ok=True)

    # Set the end index to the length of the playlist if it is None.
    if end is None:
        end = len(playlist.video_urls)

    # Get the URLs of all the videos in the playlist.
    video_urls = playlist.video_urls[start:end]

    # Download the videos in parallel.
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(
            download_video_hq, video_urls, [playlist_dir] * len(video_urls)
        )

    # Return the paths of the downloaded videos.
    return list(results)
