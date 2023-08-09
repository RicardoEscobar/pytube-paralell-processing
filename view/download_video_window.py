"""This module creates a window to download videos from YouTube."""

from pathlib import Path
import tkinter as tk
from tkinter import ttk
from threading import Thread
from controller.download_video_yt import download_video_yt


def main():
    """Create the main window and run the app."""

    def download_video():
        """Download a youtube video."""

        if youtube_url.get() == "":
            status.set("Please enter a YouTube URL")
            return

        # Disable the download button.
        download_button["state"] = "disabled"

        percent_complete.set(0.00)
        progress_bar["value"] = percent_complete.get()
        progress_bar.update()

        # Update progress bar graphically with update_idletasks()
        progress_bar.update_idletasks()

        # Execute the download in a separate thread.
        download_video_thread = Thread(
            target=download_video_yt,
            args=(youtube_url.get(), output_path),
            kwargs={
                "on_progress": on_progress_callback,
                "on_complete": on_complete_callback,
            },
        )
        download_video_thread.start()

    def download_audio():
        """Download a youtube audio and convert to mp3."""
        if youtube_url.get() == "":
            status.set("Please enter a YouTube URL")
            return

        # Disable the download button.
        download_audio_button["state"] = "disabled"

        percent_complete.set(0.00)
        progress_bar["value"] = percent_complete.get()
        progress_bar.update()

        # Update progress bar graphically with update_idletasks()
        progress_bar.update_idletasks()

        # Execute the download in a separate thread.
        download_audio_thread = Thread(
            target=download_audio_yt,
            args=(youtube_url.get(), output_path),
            kwargs={
                "on_progress_callback": on_progress_callback,
                "on_complete_callback": on_complete_callback,
            },
        )
        download_audio_thread.start()

    def on_progress_callback(
        chunk,
        file_handler,
        bytes_remaining: int,
        bytes_total: int = None,
        filename: str = None,
    ):
        """Show the progress of the download."""

        if bytes_total is None:
            raise ValueError("Total bytes is None")

        if filename is None:
            raise ValueError("Filename is None")

        bytes_downloaded = bytes_total - bytes_remaining

        # Calculate the percent complete
        percent_complete_calculate = round((bytes_downloaded / bytes_total * 100), 2)
        percent_complete.set(percent_complete_calculate)
        percent_complete_label_text.set(f"{percent_complete_calculate}%")
        progress_bar.update()

        # Update progress bar graphically with update_idletasks()
        progress_bar.update_idletasks()

        # Show the progress in the status bar.
        status.set(f"Downloading {filename}")

    def on_complete_callback(stream, file_path):
        """Show the completion of the download."""
        BYTES_IN_GIGABYTE = 1073741824
        BYTES_IN_MEGABYTE = 1048576

        if stream.filesize > BYTES_IN_GIGABYTE:
            filesize = f"[{round(stream.filesize / BYTES_IN_GIGABYTE, 2)} GB]"
        else:
            filesize = f"[{round(stream.filesize / BYTES_IN_MEGABYTE, 2)} MB]"

        file_path = Path(file_path)
        complete_message = f"Completed: {file_path.name} {filesize} downloaded."

        status.set(complete_message)

        # Enable the download button.
        download_button["state"] = "enabled"
        download_audio_button["state"] = "enabled"

    root = tk.Tk()
    root.title("YouTube Downloader")

    # Make column 1 expandable, this is the middle column with the entry box.
    root.grid_columnconfigure(1, weight=1)
    # Make row 2 expandable, this is the row with the status bar.
    root.grid_rowconfigure(2, weight=1)

    youtube_url = tk.StringVar()
    percent_complete = tk.DoubleVar()
    percent_complete_label_text = tk.StringVar()
    status = tk.StringVar()

    status.set("Waiting for URL, running like a champ!")
    output_path = "downloads/"

    # YouTube URL label and entry
    url_label = ttk.Label(root, text="YouTube URL")
    url_label.grid(row=0, column=0, sticky=tk.W)
    url_entry = ttk.Entry(root, width=50, textvariable=youtube_url)
    url_entry.grid(row=0, column=1, sticky=tk.EW)

    # Download button
    download_button = ttk.Button(root, text="Video", command=download_video)
    download_button.grid(row=0, column=2, sticky=tk.E)

    # Download audio button
    download_audio_button = ttk.Button(root, text="MP3", command=download_audio)
    download_audio_button.grid(row=0, column=3, sticky=tk.E)

    # Progress bar
    progress_bar = ttk.Progressbar(
        root,
        orient=tk.HORIZONTAL,
        length=100,
        mode="determinate",
        variable=percent_complete,
    )
    progress_bar.grid(row=1, column=0, columnspan=3, sticky=tk.EW)
    progress_bar_label = ttk.Label(
        root, text="Progress Bar", textvariable=percent_complete_label_text
    )
    progress_bar_label.grid(row=1, column=2, sticky=tk.E)

    # Status bar
    status_bar = ttk.Label(root, textvariable=status)
    status_bar.grid(row=2, column=0, columnspan=3, sticky=tk.EW)

    root.mainloop()


if __name__ == "__main__":
    main()
