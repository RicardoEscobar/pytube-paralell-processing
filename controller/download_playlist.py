"""
This module provides functionality for downloading a YouTube playlist using
PyTube and multiprocessing.
"""

import concurrent.futures
from pathlib import Path

from pytube import Playlist
from typing import List, Union

from controller.sanitize_path import sanitize_path
from controller.time_it import time_it
from controller.download_video_hq import download_video_hq


@time_it
def download_playlist(
    playlist_url: str,
    output_dir: Union[str, Path] = ".",
    start: int = 0,
    end: int = None,
    show_index: bool = False,
) -> List[str]:
    """
    Download a youtube playlist.

    Args:
        playlist_url (str): The URL of the playlist to download.
        output_dir (str, Path): The path to the output directory.
        start (int): The index of the first video to download.
        end (int): The index of the last video to download.
        show_index (bool): Whether to include the index on the playlist at the
        start of the filename.
    Returns:
        A list of the paths of the downloaded videos.
    """
    # Create Playlist object from the url string.
    playlist = Playlist(playlist_url)

    # Create the index for the videos if required.
    if show_index:
        # Save playlist indexes to a list.
        playlist_indexes = list(range(1, len(playlist.video_urls) + 1))
    else:
        playlist_indexes = [None] * len(playlist.video_urls)

    # Set the start index to 0 if it is None.
    if start is None:
        start = 0

    # Set the end index to the length of the playlist if it is None.
    if end is None:
        end = len(playlist.video_urls)

    # If the output directory is a string, convert it to a Path object.
    if isinstance(output_dir, str):
        output_dir = Path(output_dir)

    # If the output directory does not exist, create it.
    output_dir.mkdir(parents=True, exist_ok=True)

    # Print how many videos are in the playlist.
    print(f"Number of videos in playlist: {len(playlist.videos)}")

    # Create a directory for the playlist
    playlist_name = playlist.title + " [" + playlist.owner + "]"
    playlist_path = output_dir / sanitize_path(playlist_name)

    # Get the URLs of all the videos in the playlist.
    video_urls = playlist.video_urls[start:end]

    # Download the videos in parallel.
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(
            download_video_hq,
            video_urls,
            [playlist_path] * len(video_urls),
            playlist_indexes,
        )

    # Return the paths of the downloaded videos.
    return list(results)
