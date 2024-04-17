"""This module contains functions to merge video files."""

"""This script removes a section of the video given a start and an end time."""

# If this file runs as a script, run add the parent directory to the sys.path.
if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.append(str(Path(__file__).resolve().parent.parent))

from pathlib import Path
import os
from typing import List, Union

from controller.time_it import time_it


@time_it
def join_videos(videofilepaths: List[str], output_video_file: Union[str, Path]) -> Path:
    with open("temp.txt", "w") as f:
        for path in videofilepaths:
            f.write(f"file '{path}'\n")

    ffmpeg_command = (
        f'ffmpeg -hide_banner -loglevel error -f concat -safe 0 -i "temp.txt" '
        f'-codec copy "{output_video_file}"'
    )

    try:
        os.system(ffmpeg_command)
    finally:
        os.remove("temp.txt")

    return Path(output_video_file).resolve()


if __name__ == "__main__":
    videos = [
        r"F:\FIRECUDA2\grabaciones\Carhartt\2024-04-17\2024-04-17_11-11-22.mkv",
        r"F:\FIRECUDA2\grabaciones\Carhartt\2024-04-17\2024-04-17_12-25-51_clip.mkv",
    ]
    OUTPUT_VIDEO = (
        r"F:\FIRECUDA2\grabaciones\Carhartt\2024-04-17\2024-04-17_12-25-51_merge.mkv"
    )

    output_filepath = join_videos(videos, OUTPUT_VIDEO)
    print(output_filepath)
