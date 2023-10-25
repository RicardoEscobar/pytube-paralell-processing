"""This script removes a section of the video given a start and an end time."""

# If this file runs as a script, run add the parent directory to the sys.path.
if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.append(str(Path(__file__).resolve().parent.parent))

from pathlib import Path
import os
from controller.time_it import time_it


@time_it
def remove_clip(
    input_video_path: str, start_time: str, end_time: str, output_video_file: str = None
) -> str:
    """Given a start and an end time, remove that section of the video.
    args:
        video_file: Path to the video file.
        start_time: Start time of the clip to remove.
        end_time: End time of the clip to remove.
    returns:
        Path to the output video file.
    """
    input_video_path = Path(input_video_path)

    # Use the same video file name as input, but change the extension to .mp4
    if output_video_file is None:
        output_video_file = input_video_path.with_suffix(".mp4")
    else:
        output_video_file = Path(output_video_file)

    ffmpeg_command = f'ffmpeg -hide_banner -loglevel error -i "{input_video_path}" -c copy -ss {start_time} -to {end_time} -n "{output_video_file}"'
    print(ffmpeg_command)

    try:
        os.system(ffmpeg_command)
    except Exception as e:
        print(e)
        return None
    else:
        # input_video_path.unlink() # Removed temporarily for testing.
        return output_video_file.resolve()


def get_video_file(input_dir: str = ".") -> str:
    """Generator that yields of all video files in a directory."""
    input_dir = Path(input_dir)
    for file in input_dir.iterdir():
        if file.suffix in [".mp4", ".mkv"]:
            yield file


@time_it
def main():
    VIDEO = r"E:\grabaciones\Carhartt\2023-10-20\2023-10-20_11-05-02.mkv"
    START_TIME = "00:09:44"
    END_TIME = "00:11:37"
    OUTPUT_VIDEO_FILE = (
        r"E:\grabaciones\Carhartt\2023-10-20\2023-10-20_no_quiero_heroes_clip.mkv"
    )
    remove_clip(VIDEO, START_TIME, END_TIME, OUTPUT_VIDEO_FILE)


if __name__ == "__main__":
    main()
