# Add root folder to path
import sys
from pathlib import Path

project_directory = Path(__file__).resolve().parents[2]
sys.path.append(str(project_directory))

import unittest
from controller.download_playlist import download_playlist


class TestDownloadPlaylist(unittest.TestCase):
    """TestDownloadPlaylist"""

    def test_download_playlist(self):
        """test_download_playlist"""
        url = "https://youtube.com/playlist?list=PLzuJYcABcR-QrC95jr3P-g9IHgNcP9F2Q&si=qDPbwOVeXDvvXjqq"
        output_dir = r"/home/jorge/youtube"

        download_playlist(url, output_dir)


if __name__ == "__main__":
    unittest.main()
