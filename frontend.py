import os
import sys
import argparse
import pyperclip as clipboard
import yt_dlp as youtube_dl
from distutils.util import strtobool
import config


def query_yes_no(question, default=True):
    prompt = " [Y/n] " if default else " [y/N] "
    sys.stdout.write(question + prompt)

    while True:
        choice = input().lower()
        if choice.strip() == "":
            return default

        try:
            return strtobool(choice)
        except ValueError:
            sys.stdout.write("Please respond with (Y)ES or (N)O: ")


def ffmpeg_path():
    expected_path = os.path.join(os.path.dirname(__file__), "thirdparty")

    if (os.path.exists(expected_path)):
        return expected_path
    else:
        return None; 


# Quality video/audio selector
def video_format(resolution):
    if (ffmpeg_path()):
        return 'bestvideo[height<=%s][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' % resolution
    else:
        return '[height<=%s]' % resolution


# Do links contain playlists
def contain_playlist(links):
    for item in links:
        if item.__contains__("/playlist"): # it should be direct link to playlist
            return True
        if item.__contains__("list="):
            if query_yes_no("Do you want to download related playlists?", default=False):
                return True
            else:
                return False
    return False


# Download links from clipboard
def download():
    parser = argparse.ArgumentParser(
        description='Frontend for youtube-dl (yt-dlp). Supports all default yt-dlp --flags.',
        add_help=True
    )
    parser.add_argument(
        '--res', '-r', dest='resolution', type=int, default=config.DEFAULT_RESOLUTION,
        help="Desirable resolution of videos"
    )
    
    args, cmd_opts = parser.parse_known_args()
    opts = []

    # Get links from clipboard
    links = clipboard.paste().replace(",", "\n").splitlines()
    no_playlists = not contain_playlist(links)

    if no_playlists:
        opts.append("--no-playlist")


    if (len(links) <= 1 and no_playlists):
        output = config.SINGLE_FILE # Output format for single file
    else:
        output = config.MULTIPLE_FILES # For multiple files


    ffmpeg = ffmpeg_path()
    if(ffmpeg):
        opts.extend(['--ffmpeg-location', ffmpeg])
        #opts.extend(['--downloader', 'ffmpeg'])
        #opts.extend(['--downloader-args', 'ffmpeg:-loglevel error'])

    opts.extend(['-P', os.getcwd()]) # directory output path
    opts.extend(['-o', output])
    opts.extend(['-f', video_format(args.resolution)])

    try:
        args = opts + config.OPTIONS + cmd_opts + ['--'] + links
        #print(args)
        youtube_dl.main(args)
    except (KeyboardInterrupt) as err:
        print("\n")


if __name__ == "__main__":
    download()
