"""This script converts all mkv files in the current directory to mp4 files."""
import multiprocessing as mp
import os
from pathlib import Path

from time_it import time_it


@time_it
def mkv_to_mp4(input_video_path: str, output_video_file: str = None, video_codec: str = 'libx264') -> str:
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
    if video_codec == 'libx265':
        video_codec = f'{video_codec} -x265-params log-level=quiet'

    # ffmpeg_command = f'ffmpeg -hide_banner -loglevel error -i "{input_video_path}" -c:v libx264 -preset:v slow -crf 18 -r 60 -vf "scale=-2:1080,format=yuv420p" -c:a aac -b:a 192k -ac 2 -ar 48000 -movflags +faststart -n "{output_video_file}"'
    ffmpeg_command = f'ffmpeg -hide_banner -loglevel error -i "{input_video_path}" -c:v {video_codec} -c:a copy -n "{output_video_file}"'
    print(ffmpeg_command)

    try:
        os.system(ffmpeg_command)
    except Exception as exception:
        print(exception)
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
def process_dir(input_dir: str, video_codec: str = 'libx264') -> None:
    """Convert all mkv files in a directory to mp4 files.
    args:
        dir: Path to the directory.
        video_codec: Video codec to use. Default is 'libx264' or 'libx265'. The difference is that
        'libx265' is a newer codec and produces smaller files but is slower.
    """

    # Use pool to parallelize the conversion.
    pool = mp.Pool()
    pool.starmap(
        mkv_to_mp4,
        [
            (file.resolve(), file.with_suffix(".mp4"), video_codec)
            for file in get_mkv_file(input_dir)
        ],
    )


@time_it
def main():
    PATH = Path(r"E:\grabaciones")
    VIDEO_CODEC = 'libx265'
    process_dir(PATH, VIDEO_CODEC)
    # output_video_file = r'E:\grabaciones\Carhartt\2023-05-29\2023-05-29_12-00-27-compressed.mp4'
    # mkv_to_mp4(PATH, output_video_file)


if __name__ == "__main__":
    main()
