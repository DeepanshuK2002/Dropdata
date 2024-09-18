import os
from pytube import Playlist

# URL of the YouTube playlist to download
playlist_url = ""

# Create a Playlist object from the playlist URL
playlist = Playlist(playlist_url)

# Loop through each video in the playlist and download it
for video in playlist.videos:
    print(f"Downloading {video.title}...")
    video.streams.first().download()
    print("Download complete!\n")

# Combine all downloaded videos into a single file
video_files = [file for file in os.listdir(".") if file.endswith(".mp4")]
if len(video_files) > 1:
    print("Combining downloaded videos...")
    with open(f"{playlist.title}.mp4", "wb") as output:
        for file in video_files:
            with open(file, "rb") as input:
                output.write(input.read())
    print("Video download complete!")
else:
    print("Playlist downloaded successfully!")
