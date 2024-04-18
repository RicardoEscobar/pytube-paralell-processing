"""This script converts all mkv files in the current directory to mp4 files."""

# add the project root directory to the system path
if __name__ == "__main__":
    from pathlib import Path

    project_directory = Path(__file__).parent.parent
    import sys

    # sys.path.insert(0, str(project_directory))
    sys.path.append(str(project_directory))

import time
import concurrent.futures
import threading as th
import os
from pathlib import Path

from tqdm import tqdm

from controller.create_logger import create_logger
from controller.time_it import time_it

# Create a logger for this module.
module_logger = create_logger(
    logger_name="controller.mkv_to_mp4",
    logger_filename="mkv_to_mp4.log",
    log_directory=Path(__file__).parent.parent / "logs",
    add_date_to_filename=False,
)


@time_it
def mkv_to_mp4(
    input_video_path: str, output_video_file: str = None, video_codec: str = "libx264"
) -> str:
    """Convert a mkv file to a mp4 file.
    args:
        input_video_path: Path to the mkv file.
        output_video_file: Path to the output mp4 file.
        video_codec: Video codec to use. Default is 'libx264' or 'libx265'. The difference is that
        'libx265' is a newer codec and produces smaller files but is slower.
    returns:
        Path to the mp4 file.
    """
    input_video_path = Path(input_video_path)

    # If no output file is specified, use the same name as the input file.
    if output_video_file is None:
        output_video_file = input_video_path.with_suffix(".mp4")

    # If video_codec is 'libx265' add the '-x265-params' option to hide header output.
    if video_codec == "libx265":
        video_codec = f"{video_codec} -x265-params log-level=quiet"

    # ffmpeg_command = f'ffmpeg -hide_banner -loglevel error -i "{input_video_path}" -c:v libx264 -preset:v slow -crf 18 -r 60 -vf "scale=-2:1080,format=yuv420p" -c:a aac -b:a 192k -ac 2 -ar 48000 -movflags +faststart -n "{output_video_file}"'
    ffmpeg_command = f'ffmpeg -hide_banner -loglevel error -i "{input_video_path}" -c:v {video_codec} -c:a copy -n "{output_video_file}"'
    module_logger.info(ffmpeg_command)

    try:
        os.system(ffmpeg_command)
    except Exception as exception:
        module_logger.error(exception)
        return None
    else:
        # Delete the input file.
        input_video_path.unlink()
        return output_video_file


def get_mkv_file(input_dir: str = ".") -> str:
    """Generator that yields of all mkv files in a directory and sub directories."""
    input_dir = Path(input_dir)
    for file in input_dir.iterdir():
        if file.is_dir():
            yield from get_mkv_file(file)
        elif file.suffix == ".mkv":
            yield file


@time_it
def process_dir(input_dir, video_codec):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for input_file in get_mkv_file(input_dir):
            output_file = input_file.with_suffix(".mp4")
            futures.append(
                executor.submit(
                    mkv_to_mp4, input_file.resolve(), output_file, video_codec
                )
            )
            module_logger.debug(f"Processing {input_file}")
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                module_logger.debug(f"Completed: {result}")
            except Exception as exception:
                module_logger.error(f"Exception: {exception}")


def calculate_progress(total, current):
    """Calculate the progress of a task given the total and current time."""
    total_parts = total.split(":")
    current_parts = current.split(":")

    total_seconds = (
        int(total_parts[0]) * 3600 + int(total_parts[1]) * 60 + float(total_parts[2])
    )
    current_seconds = (
        int(current_parts[0]) * 3600
        + int(current_parts[1]) * 60
        + float(current_parts[2])
    )

    progress = (current_seconds / total_seconds) * 100
    return progress


def test_progress_bar():
    total = "00:00:10.00"
    pbar = tqdm(total=100)  # Set total progress as 100 (percentage)

    for i in range(10):
        time.sleep(1)  # Simulate work
        current = f"00:00:{i+1:02d}.00"
        progress = calculate_progress(total, current)
        pbar.update(
            progress - pbar.n
        )  # Update the progress bar with the incremental progress

    pbar.close()  # Ensure the progress bar is properly closed after completion


@time_it
def main():
    """Main function."""
    module_logger.info("Starting mkv_to_mp4.py")
    videopath = Path(
        r"F:\FIRECUDA2\grabaciones\Carhartt\2024-04-18\2024-04-17_12-25-51_merge.mkv"
    )
    outputpath = Path(r"F:\FIRECUDA2\grabaciones\Carhartt\2024-04-18\output.mp4")
    # ffmpeg -i input.mp4 output.mp4 1> progress.txt 2>&1
    ffmpeg_command = f'ffmpeg -i "{str(videopath)}" "{str(outputpath)}" 1> "progress_{str(outputpath.stem)}.txt" 2>&1'
    print(ffmpeg_command)
    os.system(ffmpeg_command)


@time_it
def main1():
    """Main function."""

    module_logger.info("Starting mkv_to_mp4.py")
    PATH = Path(r"F:\FIRECUDA2\grabaciones")
    VIDEO_CODEC = "libx265"
    module_logger.debug(f"VIDEO_CODEC: {VIDEO_CODEC}")
    module_logger.debug(f"PATH: {PATH}")
    process_dir(PATH, VIDEO_CODEC)

    # input_video_path = r'E:\grabaciones\Super mario rpg\2023-12-24\2023-12-24_13-41-12.mkv'
    # output_video_file = r'E:\grabaciones\Super mario rpg\2023-12-24\2023-12-24_13-41-12-compressed.mp4'
    # mkv_to_mp4(input_video_path, output_video_file)


if __name__ == "__main__":
    test_progress_bar()
