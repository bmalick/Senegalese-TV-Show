import os
from argparse import ArgumentParser
import yt_dlp

def download_playlist(name, playlist_url, download_type, base_dir="data"):
    save_dir = os.path.join(base_dir, name)
    os.makedirs(base_dir, exist_ok=True)
    # Set download options based on the type (audio or video)
    if download_type == 'audio':
        ydl_opts = {
            'outtmpl': os.path.join(save_dir, '%(title)s.%(ext)s'),  # Save each audio with its title
            'format': 'bestaudio',  # Download the best audio quality available
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',  # Corrected the key
                'preferredcodec': 'mp3',  # Convert audio to MP3
                'preferredquality': '0',  # Set the audio quality
            }],
            'quiet': False,  # Show download progress
        }
    elif download_type == 'video':
        ydl_opts = {
            'outtmpl': os.path.join(save_dir, '%(title)s.%(ext)s'),  # Save each video with its title
            'format': 'bestvideo+bestaudio',  # Download best video + best audio
            'merge_output_format': 'mp4',  # Merge audio and video into an mp4 file
            'quiet': False,  # Show download progress
        }
    else:
        raise ValueError("Invalid download type. Choose either 'audio' or 'video'.")

    # Download the playlist
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])

