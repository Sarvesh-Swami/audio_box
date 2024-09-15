import yt_dlp


def download_audio(url, file_name):
    ydl_opts = {
        'format': 'bestaudio/best',  # Download the best audio quality available
        'outtmpl': "/home/sarvesh/Documents/personal/audio_box/box_/audio/" + file_name + ".%(ext)s",      # Save the file with a specified name
        'quiet': True,               # Suppress output for a cleaner execution
        'ffmpeg_location': '/usr/bin/ffmpeg',  # Specify ffmpeg location if needed
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  # Use FFmpeg to extract audio
            'preferredcodec': 'mp3',      # Preferred audio codec
            'preferredquality': '320K',    # Preferred audio quality
        }],
        # 'ffmpeg_location': --ffmpeg-location  # Specify the location if not in PATH

    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print("Downloading....")
        ydl.download([url])
        print("Downloaded")

# URL of the YouTube video
# video_url = 'https://www.youtube.com/watch?v=YOUR_VIDEO_ID'

# Download the audio
# download_audio(video_url)
