import streamlit as st
import yt_dlp
import os

# Set the default download directory
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def download_video(url, output_path, audio_only=False):
    try:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best' if not audio_only else 'bestaudio/best',  # Download best video and audio or just audio
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4' if not audio_only else None,  # Merge video and audio into MP4 or just download audio
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192' if audio_only else None,
            }] if audio_only else [],
            'noplaylist': True,  # Download only the single video
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return "Download successful!"
    except Exception as e:
        return f"Error: {e}"

# Streamlit app
st.title("YouTube Video and Audio Downloader")

# Input field for the YouTube video URL
video_url = st.text_input("Enter the URL of the YouTube video you want to download:")

# Option to choose between video and audio
download_type = st.radio("Choose the download type:", ("Video", "Audio"))

# Button to start the download
if st.button("Download"):
    if video_url:
        audio_only = download_type == "Audio"
        result = download_video(video_url, DOWNLOAD_FOLDER, audio_only)
        st.write(result)
    else:
        st.write("Please enter a valid YouTube URL.")
