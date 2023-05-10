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

    ffmpeg_command = f'ffmpeg -hide_banner -loglevel error -i "{input_video_path}" -c:v libx265 -c:a copy -n "{output_video_file}"'
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
    """Generator that yields of all mkv files in a directory."""
    input_dir = Path(input_dir)
    for file in input_dir.iterdir():
        if file.suffix == '.mkv':
            yield file

@time_it
def process_dir(input_dir: str, output_dir: str = None) -> None:
    """Convert all mkv files in a directory to mp4 files.
    args:
        dir: Path to the directory.
    """
    input_dir = Path(input_dir)
    if output_dir is None:
        output_dir = Path(input_dir)
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(exist_ok=True)

    # Ask if the input directory contains subdirectories.
    if any([file.is_dir() for file in input_dir.iterdir()]):
        # If so, process all subdirectories.
        for subdir in input_dir.iterdir():
            if subdir.is_dir():
                process_dir(subdir, output_dir / subdir.name)
        return
    else:
        # If not, process all mkv files in the directory.
        for file in get_mkv_file(input_dir):
            mkv_to_mp4(file.resolve(), output_dir / file.with_suffix('.mp4').name)
        
    # pool = mp.Pool()
    # pool.starmap(mkv_to_mp4, [(file.resolve(), output_dir / file.with_suffix('.mp4').name) for file in get_mkv_file(input_dir)])

@time_it
def main():
    PATH = Path(r'D:\Carhartt')
    process_dir(PATH)

if __name__ == '__main__':
    main()