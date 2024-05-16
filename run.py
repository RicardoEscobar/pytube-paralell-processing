from controller.download_playlist import download_playlist


def main():
    """test_download_playlist"""
    url = "https://youtube.com/playlist?list=PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU&si=svyTc4jJjN9VsQrC"
    output_dir = r"/home/jorge/youtube"

    result = download_playlist(url, output_dir, show_index=True)
    for path in result:
        print(path)


if __name__ == "__main__":
    main()
