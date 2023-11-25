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
        url = "https://youtube.com/playlist?list=PLzuJYcABcR-TXJ2jy5xX-MvmiO-YIRiag&si=BXDQ-BGu1ttAcGJu"
        output_dir = r"E:\YouTube downloads"

        result = download_playlist(url, output_dir)
        for path in result:
            print(path)


if __name__ == "__main__":
    unittest.main()
