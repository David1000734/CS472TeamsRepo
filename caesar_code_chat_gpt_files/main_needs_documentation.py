# TODO Add documentation for this code using chat gpt
from pytube import YouTube, Playlist
from pytube.exceptions import VideoUnavailable
import os
import moviepy.editor as mp


# function to download YouTube video and convert to audio if desired
# by default will download in current directory and not convert to audio
def download_youtube_video(url: str, video_output_path: str = "", convert_to_audio: bool = False):
    # seeing if the file path is valid or exists first to put the video download in
    if video_output_path != "" and not os.path.exists(video_output_path):
        raise Exception("Invalid output folder path!")

    # seeing if url for video is valid to create object
    try:
        # creating YouTube video object
        youtube_video = YouTube(url)
        print("Downloading: " + str(youtube_video.title) + "\n")
    except VideoUnavailable:
        raise Exception(f'Invalid video url: {url}')

    # video url was valid need to try to download stream of the video
    try:
        print('Downloading video ...\n')
        stream = youtube_video.streams.first()
        stream.download(output_path=video_output_path)
        print('Done downloading video!\n')
    except:
        raise Exception("Error occurred while downloading video!")

    # check if we need to convert the video file to an audio file
    if convert_to_audio:
        # setting path of the video clip
        path_of_video_clip = fr"{video_output_path}\{stream.default_filename}"
        if video_output_path == '':
            path_of_video_clip = stream.default_filename

        # converting the video file to an audio file
        print("Converting video to audio ...")
        convert_video_to_audio(path_of_video_clip, output_path=video_output_path, video_title=stream.title)
        print("Done converting video to mp3!")

        # try to delete video file after converting to audio file
        try:
            os.remove(path_of_video_clip)
        except OSError as error:
            raise Exception(error)


# function to download YouTube playlist and convert each video to an audio file is so desired
# by default will download in current directory and not convert to audio
def download_youtube_playlist(url: str, video_output_path: str = "", convert_to_audio: bool = False):
    # seeing if the file path is valid or exists first to put the video download in
    if video_output_path != "" and not os.path.exists(video_output_path):
        raise Exception("Invalid output folder path!")

    # seeing if url for playlist is valid to create object
    try:
        # creating YouTube video object
        youtube_playlist = Playlist(url)
        print("Downloading: " + str(youtube_playlist.title) + "\n")
    except:
        raise Exception("Invalid playlist url!")

    # downloading all the videos in the playlist
    for youtube_url in youtube_playlist.video_urls:
        # playlist url was valid need to try to download a stream of each of the videos
        streams = None
        try:
            youtube_video = YouTube(youtube_url)

        except VideoUnavailable:
            print(f'Video {youtube_url} is unavailable, skipping.')

        else:
            # now to try actually downloading the video
            try:
                print("Downloading: " + str(youtube_video.title) + "\n")
                print("Downloading video ...\n")
                streams = youtube_video.streams.first()
                streams.download(output_path=video_output_path)
                print("Done downloading video!\n")

            except:
                raise Exception("Error occurred while downloading video!")

        # check if we need to convert the video file to an audio file
        if convert_to_audio:
            # setting path of the video clip
            path_of_video_clip = fr"{video_output_path}\{streams.default_filename}"
            if video_output_path == '':
                path_of_video_clip = streams.default_filename

            # converting the video file to an audio file
            print("Converting video to audio ...")
            convert_video_to_audio(path_of_video_clip, output_path=video_output_path,
                                   video_title=streams.title)
            print("Done converting video to mp3!")

            # try to delete video file after converting to audio file
            try:
                os.remove(path_of_video_clip)
            except OSError as error:
                raise Exception(error)


# function to convert a video file to an audio file mp3
def convert_video_to_audio(video_file_path: str, output_path="", video_title='temp'):
    try:
        clip = mp.VideoFileClip(video_file_path)
        # setting path of audio file
        path_of_audio_file = fr"{output_path}\{video_title}.mp3"
        if output_path == '':
            path_of_audio_file = video_title + ".mp3"
        # writing the audio file
        clip.audio.write_audiofile(path_of_audio_file)
        # wait till audio file is written then close clip and then can delete video in functions above
        clip.close()
    except:
        raise Exception("Error occurred while converting video file!")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("--------------- Running Youtube video and playlist downloader script ---------------")

    run_script = True
    while run_script:
        print("Please choose an option: \n")
        # asking user to download a YouTube video or playlist
        print("Enter 'v': to download a YouTube video")
        print("Enter 'p': to download a YouTube playlist")
        print(">: ")
        user_input = str(input())
        print("\n")

        if user_input == "v" or user_input == "V":
            print("Please enter the url of the Youtube video >: ")
            video_url = str(input())
            print("\n")

            print(
                "Please enter the folder path to store the Youtube video (If nothing is entered will use current "
                "directory)" ">: ")
            video_path = str(input())
            # getting rid of any leading and ending quotation marks " ' in the folder path if there are any
            video_path = video_path.strip('"')
            video_path = video_path.strip("'")
            print("\n")

            # asking user if they want the videos converted as mp3 files
            print("Enter 'y': to convert YouTube video to an audio file (.mp3)")
            print("Enter anything else to leave the youtube video as a video file: ")
            print(">: ")
            audio_input = str(input())
            print("\n")
            # changing the audio bool flag depending on what the user enters
            want_audio = False
            if audio_input == "y" or audio_input == "Y":
                want_audio = True

            # now calling the function to download the YouTube video
            download_youtube_video(video_url, video_path, want_audio)
            print("\n")

        elif user_input == "p" or user_input == "P":
            print("Please enter the url of the Youtube playlist >: ")
            playlist_url = str(input())
            print("\n")

            print(
                "Please enter the folder path to store the Youtube videos (If nothing is entered will use current "
                "directory)" ">: ")
            video_path = str(input())
            # getting rid of any leading and ending quotation marks " ' in the folder path if there are any
            video_path = video_path.strip('"')
            video_path = video_path.strip("'")
            print("\n")

            # asking user if they want the videos converted as mp3 files
            print("Enter 'y': to convert YouTube videos to audio files (.mp3) ")
            print("Enter anything else to leave the youtube videos as video files: ")
            print(">: ")
            audio_input = str(input())
            print("\n")
            # changing the audio bool flag depending on what the user enters
            want_audio = False
            if audio_input == "y" or audio_input == "Y":
                want_audio = True

            # now calling the function to download the YouTube video
            download_youtube_playlist(playlist_url, video_path, want_audio)
            print("\n")

        else:
            print("Please select a valid option!\n")
            continue

        # asking if user wants to end script or convert another video or playlist
        print("Enter 'y': to download another YouTube video or playlist ")
        print("Enter anything else to exit the script: ")
        print(">: ")
        exit_input = str(input())
        print("\n")
        # if the user input wants to exit then exit otherwise repeat
        if exit_input != "y" and exit_input != "Y":
            run_script = False
            print("--------------- Exiting Youtube video and playlist downloader script ---------------")