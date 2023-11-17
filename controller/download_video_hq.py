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
from pytube import YouTube, exceptions
from controller.sanitize_path import sanitize_path
from controller.time_it import time_it


@time_it
def download_video_hq(youtube_url: str, output_path: Path = Path()) -> str:
    """Download a youtube video at the highest quality.
    args:
        youtube_url (str): The URL of the video to download.
        output_path (Path): The path to the output directory.
    returns:
        The path to the downloaded video."""

    # Create YouTube object from the url string.
    youtube = YouTube(youtube_url)

    # Get temporal directory for downloading the streams.
    tmp_path = Path(output_path / "tmp")

    try:
        # get all DASH video streams
        dash_streams = youtube.streams.filter(
            type="video", subtype="mp4", progressive=False
        )
    except exceptions.LiveStreamError as error:
        return f"LiveStreamError: {error}"
    except Exception as error:
        return f"Error: {error}"

    # sort by resolution or bitrate to get the highest quality stream
    highest_quality = dash_streams.order_by("resolution").desc().first()
    
    # Add the video_id to the filename
    video_filename = f"{youtube.video_id}_{highest_quality.default_filename}"

    # If there is no stream with resolution, sort by bitrate
    if highest_quality is None:
        highest_quality = dash_streams.order_by("abr").desc().first()

    # Create the output file path
    output_file = f"{youtube.video_id}_{highest_quality.default_filename}"
    output_file_path = Path(output_path, output_file)
    output_file_path = output_file_path.resolve()

    # Check if the file already exists
    if output_file_path.exists():
        print(f"File already exists: {output_file_path}")
        return str(output_file_path)
    else:
        print(f"Downloading output_file_path: {output_file_path}")

    # download the stream
    video_stream = highest_quality.download(output_path=tmp_path, filename=video_filename)

    # get all DASH audio streams
    dash_streams = youtube.streams.filter(
        type="audio", subtype="webm", progressive=False
    )

    # sort by bitrate to get the highest quality stream
    highest_quality = dash_streams.order_by("abr").desc().first()

    # Add the video_id to the filename
    audio_filename = f"{youtube.video_id}_{highest_quality.default_filename}"

    # download the stream
    try:
        audio_stream = highest_quality.download(output_path=tmp_path, filename=audio_filename)
    except AttributeError as error:
        return f"AttributeError: {error}"

    # Validate that both streams were downloaded and have the same duration
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

    # Delete the temporal directory if it is empty
    # if tmp_path.exists() and tmp_path.is_dir() and not list(tmp_path.iterdir()):
    #     tmp_path.rmdir()

    # Return the path to the downloaded video
    return str(output_file_path)


if __name__ == "__main__":
    download_video_hq(
        "https://www.youtube.com/watch?v=U0yFunptU1g&ab_channel=PhonkKawaii",
        output_path=Path(r"E:\YouTube downloads\Phonk playlist"),
    )
