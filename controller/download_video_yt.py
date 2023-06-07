from controller.time_it import time_it
from pathlib import Path
from pytube import YouTube
from functools import partial


@time_it
def download_video_yt(
    youtube_url: str, output_path: Path = Path(), on_progress=None, on_complete=None
):
    """Download a youtube video."""

    # Generate actual callback function with 'partial', to pass the bytes_total argument.
    stream = (
        YouTube(youtube_url)
        .streams.filter(progressive=True, file_extension="mp4")
        .order_by("resolution")
        .desc()
        .first()
    )
    filesize = stream.filesize
    filename = stream.default_filename
    partial_on_progress = partial(on_progress, bytes_total=filesize, filename=filename)

    # Create YouTube object from the url string.
    youtube = YouTube(
        youtube_url,
        on_progress_callback=partial_on_progress,
        on_complete_callback=on_complete,
    )

    try:
        # Download the video
        youtube.streams.filter(progressive=True, file_extension="mp4").order_by(
            "resolution"
        ).desc().first().download(output_path=output_path)
    except Exception as e:
        print(type(e).__name__)
        print(e)
        import traceback

        traceback.print_tb(e.__traceback__)
