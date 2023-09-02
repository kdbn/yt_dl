# 4320 2160 1440 1080 720 480 360 240 144
DEFAULT_RESOLUTION = 1080

# Output template: https://github.com/yt-dlp/yt-dlp#output-template
SINGLE_FILE    = "%(title)s.%(ext)s"
MULTIPLE_FILES = "%(autonumber)s. %(title)s.%(ext)s"

# yt-dlp (youtube-dl) options
# Options: https://github.com/yt-dlp/yt-dlp#usage-and-options
OPTIONS = [ 
    '--ignore-errors',
    '--no-check-certificates',
    '--embed-thumbnail',
    #'--embed-subs',
    #'--write-link',
    '--write-subs',
    # '--write-auto-subs',
    '--sponsorblock-remove', 'sponsor',
    '--sub-langs', (',').join(["ru", "en", "en-us"]),

    # rtmp/rstp/mms streams
    #'--downloader', 'ffmpeg'
    #'--downloader-args', 'ffmpeg:-loglevel error'
]
