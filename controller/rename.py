"""This is a temporary file to rename the already downloaded videos to the new
naming convention."""

from typing import Generator, Tuple
from pathlib import Path
import re

from pytube import YouTube, Playlist


def rename(file: Path, index: int = None) -> Path:
    """Rename the file to the new naming convention."""
    # Get the filename, extension and video id at the start of the filename
    filename = file.stem
    extension = file.suffix
    # Get video id at the start of the filename. The `(?=\b|_)` is a positive
    # lookahead that asserts what immediately follows the current position in
    # the string is either a word boundary or an underscore. This allows the
    # match to succeed when the 11 characters are followed by an underscore.
    match = re.search(r"(\b|-)[\w-]{10,11}(?=\b|_)", filename)
    if match is None:
        raise ValueError(f"No video ID found in filename: {filename}")
    video_id = match.group()

    # Remove the video id from the filename
    filename = filename.replace(video_id, "").strip("_")

    # Return the new filename
    if index:
        result = file.parent / f"{index:02d}_{filename}_{video_id}{extension}"
    else:
        result = file.parent / f"{filename}_{video_id}{extension}"
    return result


def generate_file_index(playlist_url: str):
    """Generate the index for the files in the playlist. Yield the index and
    the video id."""
    playlist = Playlist(playlist_url)
    for index, video in enumerate(playlist.video_urls, start=1):
        yield index, YouTube(video).video_id


def undo_rename(file: Path) -> Generator[Tuple[Path, Path], None, None]:
    """Undo the renaming of the file.
    Args:
        file (Path): The path to the text file containing the video old name ->
        new name.
    Returns:
        Path: The text file with the new name -> old name."""
    # Get the filename, extension and video id at the start of the filename
    with open(file, "r") as f:
        lines = f.readlines()
    # Loop through the lines and get the old name and new name
    for line in lines:
        old_name, new_name = line.split("->")
        old_name = Path(old_name.strip())
        new_name = Path(new_name.strip())
        # Rename the file
        # old_name.rename(new_name)
        yield old_name, new_name


def main():
    """Rename the files in the directory."""
    # Get the directory
    directory = Path("/home/jorge/youtube/Phonk kawaii playlist")
    # Get the files in the directory
    files = directory.glob("*.mp4")
    # Rename the files
    for file in files:
        new_file = rename(file)
        print(f"{file} -> {new_file}")

    # Rename the files with index
    files = directory.glob("*.mp4")
    print("-" * 80)
    for index, file in enumerate(files, start=1):
        new_file = rename(file, index)
        print(f"{file} -> {new_file}")
        # Do the actual renaming
        # file.rename(new_file)

    # Generate the index for the files in the playlist
    playlist_url = "https://www.youtube.com/playlist?list=PL7Vq61n7Z1aV1Q9mZv2Z3pJ3v9DQ2k2QJ"


def undo_rename_main(file: Path = None):
    """Undo the renaming of the files."""
    if file is None:
        file = Path("last_rename.txt")

    # Get the directory
    directory = Path("/home/jorge/youtube/Phonk kawaii playlist")
    # Get the file with the old names
    file = Path("renamed.txt")
    # Undo the renaming
    for old_name, new_name in undo_rename(file):
        print(f"{new_name} -> {old_name}")
        # Do the actual renaming
        new_name.rename(old_name)


def rename_index_from_playlist(playlist_url: str, directory: Path):
    """Rename the files in the directory with the index from the playlist."""
    # Get the files in the directory
    files = list(directory.glob("*.mp4"))
    # Get the index for the files in the playlist
    index_generator = generate_file_index(playlist_url)
    # Loop through the index generator to get the index and video id
    for index, video_id in index_generator:
        # Get the file path and compare the video id
        for file in files:
            if video_id in file.name:
                new_file = rename(file, index)
                print(f"{file} -> {new_file}")
                # Do the actual renaming
                file.rename(new_file)
                break


if __name__ == "__main__":
    playlist_url = "https://youtube.com/playlist?list=PLzuJYcABcR-QrC95jr3P-g9IHgNcP9F2Q&si=qDPbwOVeXDvvXjqq"
    output_dir = Path("/home/jorge/youtube/Phonk kawaii playlist")
    file = Path("last_rename.txt")
    rename_index_from_playlist(playlist_url, output_dir)
