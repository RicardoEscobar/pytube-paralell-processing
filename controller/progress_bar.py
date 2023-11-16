from tqdm import tqdm


progress_bar = None


def on_progress(
    chunk,
    file_handler,
    bytes_remaining: int,
    bytes_total: int = None,
    filename: str = None,
):
    """Show progress of the download."""
    global progress_bar

    if progress_bar is None:
        progress_bar = tqdm(
            total=bytes_total, unit="B", unit_scale=True, ncols=100, desc=filename
        )

    bytes_downloaded = bytes_total - bytes_remaining
    percent_complete_calculate = round((bytes_downloaded / bytes_total * 100), 2)

    # Update the progress bar
    progress_bar.update(bytes_downloaded - progress_bar.n)

    # Update the description of the progress bar
    progress_bar.set_description(
        f"{filename} {percent_complete_calculate}% ({bytes_downloaded}/{bytes_total})"
    )
