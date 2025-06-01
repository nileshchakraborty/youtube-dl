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
# Defaults to ~/Downloads/YouTube/<Video Uploader>
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
        info = ydl.extract_info(video_url)
        video_title = info.get('title', 'video')
        video_uploader = info.get('uploader', 'Unknown')
        downloaded_file = ydl.prepare_filename(info)

    # Create the download directory if it doesn't exist
    video_uploader = re.sub(r'[\\/*?:"<>|]', '', video_uploader)  # Remove invalid characters
    download_path = os.path.join(DOWNLOAD_DIR, video_uploader)
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    new_path = os.path.join(download_path, downloaded_file)
    os.rename(downloaded_file, new_path)  # Move the downloaded file to the new path


    print(f'Video "{video_title}" downloaded successfully!')
    print(f'Video saved in: {new_path}')

    # After downloading the videos from playslist, ask if user wants to move the downloaded videos to the download directory
    move_to_downloads = input("Do you want to move the downloaded video to the Downloads directory? (y/n): ")
    if move_to_downloads.lower() == 'y':
        # List all video files in the download new_path
        
        video_file_names_list = []
        for root, dirs, files in os.walk(download_path):
            for file in files:
                if file.endswith(('.mp4', '.mkv', '.avi', '.mov', '.flv')):
                    video_file_names_list.append(os.path.basename(file))
        # Move the files to folders based on their names
        if not video_file_names_list:
            print("No video files found to move.")
            return
        print(f'Moving {len(video_file_names_list)} video files to folders...')
        # Move the files to folders based on their names    
        move_files_to_folders(video_file_names_list)
        print(f'Video moved to: {download_path}')

    else:
        print('Video not moved.')

import moviepy.editor as mp

def extract_audio(file_path):
    # Load video file using MoviePy
    video = mp.VideoFileClip(file_path)
    
    # Extract audio from the video
    audio = video.audio
    
    # Save the extracted audio to a new file
    audio_file_path = os.path.splitext(file_path)[0] + '.mp3'
    audio.write_audiofile(audio_file_path)
    print(f'Audio extracted and saved to: {audio_file_path}')

# Function to move files to folders based on their names
def move_files_to_folders(video_file_names_list):
    """Moves each video file to a folder with the same name."""
    folder_path = DOWNLOAD_DIR
    common_part = ''
    for file in video_file_names_list:
        # Get the file name without the extension
        file_name, _ = os.path.splitext(file)
        
        # Extract the common part of the file names and create a directory name
        common_part = os.path.commonprefix([common_part, file_name])
        folder_path = os.path.join(DOWNLOAD_DIR, common_part) if common_part else DOWNLOAD_DIR

        
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    # Move the file to the folder
    source_path = os.path.join(DOWNLOAD_DIR, file)
    destination_path = os.path.join(folder_path, file)
    if os.path.exists(source_path):
        os.rename(source_path, destination_path)
        print(f'Moved {file} to {folder_path}')
    else:
        print(f'File {file} does not exist in the download directory.')
    # Reset the common part for the next file
    common_part = ''
    # Reset the folder path for the next file
    folder_path = ''

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
    print("4. Move downloaded videos to Downloads directory")
    print("5. Extract audio from downloaded video")
    print("6. Exit")
    choice = input("Enter your choice: ")
    if choice == '1':
        download_video()
    elif choice == '2':
        download_audio()
    elif choice == '3':
        downloader()
    elif choice == '4':
        video_file_names_list = []
        for root, dirs, files in os.walk(DOWNLOAD_DIR):
            for file in files:
                if file.endswith(('.mp4', '.mkv', '.avi', '.mov', '.flv')):
                    video_file_names_list.append(os.path.basename(file))
        if not video_file_names_list:
            print("No video files found to move.")
            return
        print(f'Moving {len(video_file_names_list)} video files to folders...')
        move_files_to_folders(video_file_names_list)
    elif choice == '5':
        video_file_path = input("Enter the path of the downloaded video file: ")
        if os.path.exists(video_file_path):
            extract_audio(video_file_path)
        else:
            print("File does not exist. Please check the path and try again.")
    elif choice == '6':
        print("Exiting the program. Goodbye!")
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
