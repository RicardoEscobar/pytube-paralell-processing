"""This module provides a function to download audio from a YouTube video."""

from pathlib import Path

from pytube import YouTube

from controller.time_it import time_it
from controller.to_mp3 import to_mp3
from functools import partial


@time_it
def download_audio_yt(
    youtube_url: str,
    output_path: str = None,
    on_progress_callback=None,
    on_complete_callback=None,
):
    """Download a youtube audio."""

    # Create tmp directory for downloading the streams.
    if output_path is None:
        output_path = Path(".") / "downloads"
    else:
        output_path = Path(output_path)

    # Create tmp directory for downloading the streams.
    tmp_path = Path(output_path) / "tmp"
    tmp_path.mkdir(exist_ok=True)

    # Create Stream object from the url string.
    stream = (
        YouTube(youtube_url)
        .streams.filter(only_audio=True)
        .order_by("abr")
        .desc()
        .first()
    )

    # Generate actual callback function with 'partial', to pass the bytes_total argument.
    partial_on_progress_callback = partial(
        on_progress_callback, bytes_total=stream.filesize, filename=stream.title
    )

    # Create YouTube object from the url string.
    youtube = YouTube(
        youtube_url,
        on_progress_callback=partial_on_progress_callback,
        on_complete_callback=on_complete_callback,
    )

    # Download the audio
    try:
        file_path = (
            youtube.streams.filter(only_audio=True)
            .order_by("abr")
            .desc()
            .first()
            .download()
        )

        # Make a Path object from the file_path string.
        file_path = Path(file_path)
    except Exception as e:
        print(type(e).__name__)
        print(e)
        import traceback

        traceback.print_tb(e.__traceback__)
    else:
        # Convert to mp3
        to_mp3(Path(file_path), output_path)
