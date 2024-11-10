if __name__ == "__main__":
    from pathlib import Path

    project_directory = Path(__file__).parent.parent
    import sys

    # sys.path.insert(0, str(project_directory))
    sys.path.append(str(project_directory))

from controller.time_it import time_it
from pathlib import Path
from pytubefix import YouTube
from functools import partial

from controller.progress_bar import on_progress


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


if __name__ == "__main__":
    download_video_yt(
        "https://youtu.be/CmKzYVcfulA?si=ozvLodXI4V0Rpi49",
        output_path=Path(r"E:\YouTube downloads\Phonk playlist"),
        on_progress=on_progress,
    )
