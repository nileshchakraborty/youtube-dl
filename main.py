# Install the required libraries
# pip install pytube
# pip install youtube-dl

# Import the required libraries
from pytube import Playlist
import os
import youtube_dl
from time import sleep

import re

YOUTUBE_STREAM_AUDIO = '140' # modify the value to download a different stream

# Set the download directory
DOWNLOAD_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "YouTube")
# Create the download directory if it doesn't exist
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)
# Function to download videos from a YouTube playlist
def downloader():

    # Prompt the user for the playlist URL
    playlist_url = input("Enter the YouTube playlist URL: ")
    playlist = Playlist(playlist_url)

    # this fixes the empty playlist.videos list
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

    print(len(playlist.video_urls))

    # Loop through each video in the playlist and download it
    for video_url in playlist.video_urls:
        download_video(video_url)
        sleep(1)  # Sleep for 1 second between downloads to avoid overwhelming the server
        

# Function to download a single video from YouTube
def download_video():
    # download video from youtube
    video_url = input("Enter the YouTube video URL: ")
    download_video(video_url)


# filepath: /Users/nileshchakraborty/workspace/python/youtube_downloader/main.py
import yt_dlp as youtube_dl  # Replace youtube_dl with yt_dlp

# Function to download a single video from YouTube
def download_video(video_url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4'
        }]
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    print('Video downloaded successfully!')

# Function to download audio from YouTube
# install ffmpeg (https://ffmpeg.org/download.html)
# and add it to the PATH
# or set the ffmpeg_location in the ydl_opts
def download_audio():
    video_url = input("Enter the YouTube video URL: ")
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
        # 'ffmpeg_location': ''  # Update this path if ffmpeg is not in PATH
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    print('Audio downloaded successfully!')

# Function to display the menu
def menu():
    print("1. Download video from YouTube")
    print("2. Download audio from YouTube")
    print("3. Download videos from YouTube playlist")
    print("4. Exit")
    choice = input("Enter your choice: ")
    if choice == '1':
        download_video()
    elif choice == '2':
        download_audio()
    elif choice == '3':
        downloader()
    
    elif choice == '4':
        print("Exiting...")
        exit()
    else:
        print("Invalid choice! Please try again.")
        menu()
# Main function
def main():
    print("Welcome to YouTube Downloader!")
    while True:
        menu()
# Run the main function
if __name__ == '__main__':
    main()
# This code is a simple YouTube downloader that allows you to download videos, audio, and playlists from YouTube.
# It uses the pytube and youtube-dl libraries to download videos and audio from YouTube.
# The code is divided into several functions:
# 1. downloader(): This function downloads videos from a YouTube playlist.
# 2. download_video(): This function downloads a single video from YouTube.
# 3. download_audio(): This function downloads audio from a YouTube video.
# 4. menu(): This function displays the menu and allows the user to choose an option.


