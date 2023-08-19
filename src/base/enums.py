from enum import Enum


class YoutubeParserOptionsEnum(Enum):
    one_video = 1
    one_audio = 2
    playlist_video = 3
    playlist_audio = 4


class SonglyricsOptionsEnum(Enum):
    one_lyric = 1
    all_lyrics = 2
