"""This script downloads the audio from a Twitch stream and saves it as an MP3 file."""
import ffmpeg

# Replace with the actual input video URL
input_url = "https://www.twitch.tv/honey_goblin"

# Replace with your desired output audio file name
output_filename = "honey_goblin_stream.mp3"

input_stream = ffmpeg.input(input_url)
output_stream = ffmpeg.output(input_stream["a"], output_filename)
ffmpeg.run(output_stream)
