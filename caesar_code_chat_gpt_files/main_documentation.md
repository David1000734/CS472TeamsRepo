# YouTube Video and Playlist Downloader

This Python script allows you to download individual YouTube videos or entire playlists, with the option to convert downloaded videos to MP3 audio files. It utilizes the `pytube` library for downloading and `moviepy` for conversion.

## Features
- **Download YouTube Videos**: Save videos to a specified directory.
- **Download YouTube Playlists**: Batch download all videos in a playlist.
- **Convert Videos to Audio (MP3)**: Optionally convert downloaded videos to MP3 files.

## Prerequisites
Ensure you have Python and pip installed, along with the following dependencies:

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
- **Description**: Downloads a YouTube video and converts it to an audio file if desired.
- **Parameters**:
    - `url`: The YouTube video URL.
    - `video_output_path`: Directory to save the video. Defaults to the current directory if not provided.
    - `convert_to_audio`: If `True`, converts the downloaded video to MP3.
- **Exceptions**:
    - Raises an exception for invalid output folder paths, invalid video URLs, download failures, and conversion failures.

### `download_youtube_playlist(url: str, video_output_path: str = "", convert_to_audio: bool = False)`
- **Description**: Downloads all videos in a YouTube playlist and optionally converts them to audio files.
- **Parameters**:
    - `url`: The YouTube playlist URL.
    - `video_output_path`: Directory to save the videos. Defaults to the current directory if not provided.
    - `convert_to_audio`: If `True`, converts the videos to MP3 after downloading.
- **Exceptions**:
    - Raises an exception for invalid output folder paths, invalid playlist URLs, and download or conversion errors for individual videos.

### `convert_video_to_audio(video_file_path: str, output_path: str = "", video_title: str = 'temp')`
- **Description**: Converts a video file into an MP3 audio file.
- **Parameters**:
    - `video_file_path`: Path of the video file to convert.
    - `output_path`: Directory to save the audio file. Defaults to the current directory if not provided.
    - `video_title`: Name for the audio file.
- **Exceptions**:
    - Raises an exception if conversion fails.

## How to Use

1. **Run the Script**: Execute the Python script.
    ```bash
    python youtube_downloader.py
    ```
2. **Follow Prompts**: The script will prompt you to enter options for downloading videos or playlists, specifying output paths, and deciding whether to convert to MP3.

### Example Usage
Here’s a simple interaction with the script:

```plaintext
--------------- Running Youtube video and playlist downloader script ---------------

Please choose an option: 

Enter 'v': to download a YouTube video
Enter 'p': to download a YouTube playlist
>: v

Please enter the url of the Youtube video >: https://www.youtube.com/watch?v=example

Please enter the folder path to store the Youtube video (If nothing is entered will use current directory) >: /path/to/download

Enter 'y': to convert YouTube video to an audio file (.mp3)
Enter anything else to leave the youtube video as a video file: 
>: y

Done downloading video!
Converting video to audio ...
Done converting video to mp3!
