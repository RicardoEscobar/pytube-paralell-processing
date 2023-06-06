"""This module provides a function to download audio from a YouTube video."""

from pathlib import Path

from pytube import YouTube

from controller.time_it import time_it
from controller.to_mp3 import to_mp3


@time_it
def download_audio_yt(youtube_url: str, output_path: Path = Path()):
    """Download a youtube audio."""
    # Create YouTube object from the url string.
    youtube = YouTube(youtube_url)

    # Create tmp directory for downloading the streams.
    tmp_path = Path(output_path / "tmp")
    tmp_path.mkdir(exist_ok=True)

    # get all DASH audio streams
    filename = (
        youtube.streams.filter(only_audio=True)
        .order_by("abr")
        .desc()
        .first()
        .download(output_path=tmp_path)
    )

    to_mp3(Path(filename), output_path)
