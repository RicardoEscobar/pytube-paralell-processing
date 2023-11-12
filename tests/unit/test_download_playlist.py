import unittest
from controller.download_playlist import download_playlist


class TestDownloadPlaylist(unittest.TestCase):
    """TestDownloadPlaylist"""

    def test_download_playlist(self):
        """test_download_playlist"""
        url = "https://youtube.com/playlist?list=PLzuJYcABcR-TXJ2jy5xX-MvmiO-YIRiag&si=sWwC1EPvjiqL_KvC"
        output_dir = r"E:\YouTube downloads"

        result = download_playlist(url, output_dir)
        for path in result:
            print(path)


if __name__ == "__main__":
    unittest.main()
