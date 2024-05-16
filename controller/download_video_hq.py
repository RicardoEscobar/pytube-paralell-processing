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
import traceback
from pathlib import Path
from pytube import YouTube, exceptions
from controller.sanitize_path import sanitize_path
from controller.time_it import time_it


@time_it
def download_video_hq(
    youtube_url: str, output_path: Path = None, index: int = None
) -> Path:
    """Download a youtube video at the highest quality.
    args:
        youtube_url (str): The URL of the video to download.
        output_path (Path): The path to the output directory.
        index (int): The index of the video in the playlist.
    returns:
        The path to the downloaded video."""
    # If the output directory is a string, convert it to a Path object.
    if isinstance(output_path, str):
        output_path = Path(output_path)

    # If the output directory does not exist, create it.
    output_path.mkdir(parents=True, exist_ok=True)

    # Create YouTube object from the url string.
    youtube = YouTube(youtube_url)

    # Form the output file path
    try:
        # Get the highest quality video stream.
        highest_quality = (
            youtube.streams.filter(adaptive=True)
            .order_by("resolution")
            .desc()
            .first()
        )
    except exceptions.LiveStreamError as error:
        return f"LiveStreamError: {error}"
    except Exception as error:
        tb = traceback.format_exc()
        print(tb)
        return f"Error: {error}. Youtube URL: {repr(youtube_url)}, Output path: {repr(output_path)}"

    # sort by resolution or bitrate to get the highest quality stream

    # Get the video id, file name, extension and index
    default_filename = highest_quality.default_filename
    video_id = youtube.video_id
    extension = Path(default_filename).suffix
    filename = Path(default_filename).stem
    video_index = f"{index:02d}" if index else ""

    # Form the video filename
    if index:
        output_file_path = (
            output_path / f"{video_index}_{filename}_{video_id}.mp4"
        )
    else:
        output_file_path = output_path / f"{filename}_{video_id}.mp4"

    # Check if the file already exists, if so, return the path
    if output_file_path.exists():
        print(f"File already exists: {output_file_path}")
        return output_file_path

    # Get temporal directory for downloading the streams.
    tmp_path = Path(output_path / "tmp")

    # Create the temporal directory if it does not exist.
    tmp_path.mkdir(parents=True, exist_ok=True)

    # Form the video filename
    if index:
        video_path = (
            tmp_path / f"{video_index}_{filename}_{video_id}{extension}"
        )
    else:
        video_path = tmp_path / f"{filename}_{video_id}{extension}"

    # download the video stream
    video_stream = highest_quality.download(
        output_path=tmp_path, filename=video_path.name
    )

    # get highest quality audio stream
    highest_quality_audio = youtube.streams.get_audio_only()

    # Get the audio filename
    default_filename = highest_quality_audio.default_filename
    audio_path = Path(default_filename).stem
    audio_extension = Path(default_filename).suffix
    audio_id = youtube.video_id
    audio_index = f"{index:02d}" if index else ""

    # Form the audio filename
    if index:
        audio_path = (
            tmp_path
            / f"{audio_index}_{audio_path}_{audio_id}{audio_extension}"
        )
    else:
        audio_path = tmp_path / f"{audio_path}_{audio_id}{audio_extension}"

    # download the audio stream
    try:
        audio_stream = highest_quality_audio.download(
            output_path=tmp_path,
            filename=highest_quality_audio.default_filename,
        )
    except AttributeError as error:
        return f"AttributeError: {error}"

    # Validate that both streams were downloaded
    if not video_stream or not audio_stream:
        return "Error: Could not download the streams"

    # Call ffmpeg to merge the streams
    ffmpeg_command = (
        f"ffmpeg -hide_banner -loglevel error -y -i "
        f'"{video_stream}" -i "{audio_stream}" -c copy "{output_file_path}"'
    )

    try:
        os.system(ffmpeg_command)
    except Exception as error:
        return f"Error: {error}"
    else:
        print(f"Downloaded: {output_file_path}")

        # Delete the temporal files
        Path(video_stream).unlink()
        Path(audio_stream).unlink()

    # Return the path to the downloaded video
    return str(output_file_path)


if __name__ == "__main__":
    result = download_video_hq(
        "https://youtu.be/R0tTsdQ_9Vw?si=IC6hT_THWfVXEydj",
        output_path=Path(r"/home/jorge/youtube/test"),
        index=1,
    )
    print(result)
