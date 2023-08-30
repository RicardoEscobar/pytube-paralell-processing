"""
This module provides a function to download a YouTube video at the highest quality.
"""
if __name__ == "__main__":
    from pathlib import Path

    project_directory = Path(__file__).parent.parent
    import sys

    # sys.path.insert(0, str(project_directory))
    sys.path.append(str(project_directory))

import os
from pathlib import Path
from pytube import YouTube
from controller.sanitize_path import sanitize_path
from controller.time_it import time_it


@time_it
def download_video_hq(youtube_url: str, output_path: Path = Path()):
    """Download a youtube video at the highest quality."""

    # Create YouTube object from the url string.
    youtube = YouTube(youtube_url)

    # Get temporal directory for downloading the streams.
    tmp_path = Path(output_path / "tmp")

    # get all DASH video streams
    dash_streams = youtube.streams.filter(
        type="video", subtype="mp4", progressive=False
    )

    # sort by resolution or bitrate to get the highest quality stream
    highest_quality = dash_streams.order_by("resolution").desc().first()

    # download the stream
    video_stream = highest_quality.download(output_path=tmp_path)

    # get all DASH audio streams
    dash_streams = youtube.streams.filter(
        type="audio", subtype="webm", progressive=False
    )

    # sort by bitrate to get the highest quality stream
    highest_quality = dash_streams.order_by("abr").desc().first()

    # download the stream
    audio_stream = highest_quality.download(output_path=tmp_path)

    # Merge the audio and video streams
    output_file_path = Path(output_path, sanitize_path(youtube.title) + ".mp4")
    output_file_path = output_file_path.resolve()

    # Call ffmpeg to merge the streams
    ffmpeg_command = (
        f"ffmpeg -hide_banner -loglevel error -i "
        f'"{video_stream}" -i "{audio_stream}" -c copy "{output_file_path}"'
    )
    os.system(ffmpeg_command)

    # Delete the temporal files
    Path(video_stream).unlink()
    Path(audio_stream).unlink()
    tmp_path.rmdir()


if __name__ == "__main__":
    download_video_hq(
        "https://www.youtube.com/watch?v=TOoC7aXkpMs&list=PLZOGNlgi8GGncx1etrSzhrHM1GqoFindD&index=4&pp=gAQBiAQB8AUB",
        output_path=Path("./downloads"),
    )
