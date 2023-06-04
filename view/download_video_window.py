"""This module creates a window to download videos from YouTube."""
import tkinter as tk
from tkinter import ttk
from controller.pytube3 import 


root = tk.Tk()

youtube_url = tk.StringVar()

url_label = ttk.Label(root, text='YouTube URL')
url_label.grid(row=0, column=0, sticky=tk.W)
url_entry = ttk.Entry(root, width=50, textvariable=youtube_url)
url_entry.grid(row=0, column=1, sticky=tk.W)

# Download button
download_button = ttk.Button(root, text='Download', command=lambda: print('Download'))
download_button.grid(row=0, column=2, sticky=tk.W)


root.mainloop()