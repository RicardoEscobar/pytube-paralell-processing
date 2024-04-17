# Add root folder to path
import sys
from pathlib import Path

from pytube import YouTube

from controller.to_mp3 import to_mp3

project_directory = Path(__file__).resolve().parents[2]
sys.path.append(str(project_directory))

import unittest
from controller.download_playlist_mp3 import download_playlist_mp3


class TestDownloadPlaylist(unittest.TestCase):
    """TestDownloadPlaylist"""

    @unittest.skip("Skip test_download_playlist")
    def test_download_playlist_mp3(self):
        """test_download_playlist"""
        url = "https://youtube.com/playlist?list=PL9o_SWfAR6v23YhW4PEzFIgFicPblvbC4&si=AwhG3DBEPpLSvByo"

        download_playlist_mp3(url)

    def test_download_as_mp3(self):
        """test_download_as_mp3"""
        url = "https://youtu.be/6m6M83rKfZ8?si=Bzv26REEiu1BMRTl"
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        output_path = Path(f"E:/YouTube downloads/{stream.default_filename}")
        stream.download(output_path=output_path, skip_existing=True)
        print(output_path)
        # Convert to mp3
        mp3_path = to_mp3(output_path)
        print(mp3_path)


if __name__ == "__main__":
    unittest.main()
