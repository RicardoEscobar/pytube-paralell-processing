"""This script converts all mkv files in the current directory to mp4 files."""
from pathlib import Path
import multiprocessing as mp
import os
from time_it import time_it

@time_it
def mkv_to_mp4(input_video_path: str, output_video_file: str = None) -> str:
    """Convert a mkv file to a mp4 file.
    args:
        video_file: Path to the mkv file.
    returns:
        Path to the mp4 file.
    """
    input_video_path = Path(input_video_path)

    if output_video_file is None:
        output_video_file = input_video_path.with_suffix('.mp4')

    # ffmpeg_command = f'ffmpeg -hide_banner -loglevel error -i "{input_video_path}" -c:v libx264 -preset:v slow -crf 18 -r 60 -vf "scale=-2:1080,format=yuv420p" -c:a aac -b:a 192k -ac 2 -ar 48000 -movflags +faststart -n "{output_video_file}"'
    ffmpeg_command = f'ffmpeg -hide_banner -loglevel error -i "{input_video_path}" -c:v libx264 -c:a copy -n "{output_video_file}"'
    print(ffmpeg_command)

    try:
        os.system(ffmpeg_command)
    except Exception as e:
        print(e)
        return None
    else:
        # Delete the input file.
        input_video_path.unlink()            
        return output_video_file

def get_mkv_file(input_dir: str = '.') -> str:
    """Generator that yields of all mkv files in a directory and sub directories."""
    input_dir = Path(input_dir)
    for file in input_dir.iterdir():
        if file.is_dir():
            yield from get_mkv_file(file)
        elif file.suffix == '.mkv':
            yield file

@time_it
def process_dir(input_dir: str) -> None:
    """Convert all mkv files in a directory to mp4 files.
    args:
        dir: Path to the directory.
    """

    # Use pool to parallelize the conversion.
    pool = mp.Pool()
    pool.starmap(mkv_to_mp4, [(file.resolve(), file.with_suffix('.mp4')) for file in get_mkv_file(input_dir)])


@time_it
def main():
    PATH = Path(r'E:\grabaciones')
    process_dir(PATH)

if __name__ == '__main__':
    main()