"""This module provides a function to download a youtube playlist in mp3 format."""

if __name__ == "__main__":
    from pathlib import Path

    project_directory = Path(__file__).parent.parent
    import sys

    # sys.path.insert(0, str(project_directory))
    sys.path.append(str(project_directory))


from pathlib import Path
from threading import Thread

from pytube import Playlist
from typing import List
from tqdm import tqdm

from controller.sanitize_path import sanitize_path
from controller.time_it import time_it
from controller.download_video_hq import download_video_hq
from controller.to_mp3 import to_mp3


@time_it
def download_playlist_mp3(
    playlist_url: str, output_dir: str = None, start: int = 0, end: int = None
) -> List[Path]:
    """
    Download a youtube playlist as audio files in mp3 format.

    Args:
        playlist_url (str): The URL of the playlist to download.
        output_dir (str): The path to the output directory.
        start (int): The index of the first video to download.
        end (int): The index of the last video to download.
    Returns:
        A list of the paths of the downloaded mp3 files.
    """

    # Create Playlist object from the url string.
    playlist = Playlist(playlist_url)
    number_of_videos = len(playlist.videos)

    # Print how many videos are in the playlist.
    print(f"Number of videos in playlist: {number_of_videos}")

    # Get the output directory.
    output_dir = Path(output_dir).resolve()

    # Create a directory for the playlist.
    playlist_dir = Path(output_dir / sanitize_path(playlist.title))
    playlist_dir.mkdir(parents=True, exist_ok=True)

    # Set the end index to the length of the playlist if it is None.
    if end is None:
        end = len(playlist.video_urls)

    # Initialize the results list.
    results = []

    # Download the audio of each video in the playlist.
    for video in playlist.videos:
        # sort by bitrate to get the highest quality stream
        highest_quality = video.streams.get_audio_only()
        # Download the audio stream.
        highest_quality.download(output_dir=playlist_dir)
        # Add the path of the downloaded video to the results list.
        results.append(
            playlist_dir / f"{sanitize_path({highest_quality.default_filename})}"
        )

    # Return the paths of the downloaded videos.
    return list(results)

@time_it
def basic_usage(playlist_url = "https://youtube.com/playlist?list=PLZOGNlgi8GGk-0vti9hobdkq4hW4tHfzx&si=aqKzj6ZMFSjCop5N", output_dir = "/home/jorge/youtube"):
    # Test the function with a playlist URL.
    playlist = Playlist(playlist_url)
    output_dir = Path(output_dir) / sanitize_path(playlist.title + ' ' + playlist.playlist_id)
    output_dir.mkdir(parents=True, exist_ok=True)
    print("----------------------------------------")
    print(f"Downloading playlist: {repr(playlist.title)}")
    print(f"Number of videos in playlist: {len(playlist.videos)}")
    print(f"Output directory: {repr(str(output_dir.resolve()))}")
    print("----------------------------------------")
    for video in playlist.videos:
        filename = Path(video.streams.get_audio_only().default_filename)
        filename = filename.stem + " " + video.video_id + filename.suffix
        filename = output_dir / sanitize_path(str(filename))
        # Download the audio stream.
        # video.streams.get_audio_only().download(filename=filename)
        lambda_function = lambda: (
            video.streams.get_audio_only().download(filename=filename),
            to_mp3(filename),
        )[0]
        # Download the videos in parallel.
        thread = Thread(target=lambda_function)
        thread.start()
    thread.join()

    # Return the paths of the downloaded videos.
    


if __name__ == "__main__":
    basic_usage()
