# YouTube Video and Playlist Downloader

This Python script allows you to download individual YouTube videos or entire playlists. It also offers an option to convert downloaded videos to MP3 audio files. The script uses `pytube` to handle the video download and `moviepy` for video-to-audio conversion.

## Features
- **Download YouTube videos**: Save videos to a specified directory.
- **Download YouTube playlists**: Batch download all videos in a playlist.
- **Convert videos to audio (MP3)**: Optionally convert downloaded videos to MP3 files.

## Prerequisites
Ensure you have python and pip as well as the following dependencies installed:

1. **pytube**: For downloading YouTube content.
```bash
    pip install pytube
```
2. **moviepy**: For converting videos to audio files.
```bash
    pip install moviepy
```

## Functions Overview

### `download_youtube_video(url: str, video_output_path: str = "", convert_to_audio: bool = False)`
- **Description**: Downloads a YouTube video and, if desired, converts it to an audio file.
- **Parameters**:
    - `url`: The YouTube video URL.
    - `video_output_path`: Directory to save the video. If not provided, the current directory is used.
    - `convert_to_audio`: If `True`, converts the downloaded video to MP3.
- **Exceptions**:
    - Invalid output folder path.
    - Invalid video URL.
    - Download failure.
    - Conversion failure.

### `download_youtube_playlist(url: str, video_output_path: str = "", convert_to_audio: bool = False)`
- **Description**: Downloads all videos in a YouTube playlist. Optionally converts each video to an audio file.
- **Parameters**:
    - `url`: The YouTube playlist URL.
    - `video_output_path`: Directory to save the videos. Defaults to the current directory.
    - `convert_to_audio`: If `True`, converts the videos to MP3 after downloading.
- **Exceptions**:
    - Invalid output folder path.
    - Invalid playlist URL.
    - Download or conversion errors for individual videos.

### `convert_video_to_audio(video_file_path: str, output_path: str = "", video_title: str = 'temp')`
- **Description**: Converts a downloaded video file into an MP3 audio file.
- **Parameters**:
    - `video_file_path`: Path of the video file to convert.
    - `output_path`: Directory to save the audio file. Defaults to the current directory.
    - `video_title`: Name for the audio file.
- **Exceptions**:
    - Conversion failure.

## How to Use

1. **Run the Script**: Execute the Python script.
```bash
   python youtube_downloader.py
 ```