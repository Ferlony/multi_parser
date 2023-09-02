from enum import Enum


class YoutubeParserOptionsEnum(Enum):
    one_video = 1
    one_audio = 2
    playlist_video = 3
    playlist_audio = 4


class SonglyricsOptionsEnum(Enum):
    one_lyric = 1
    all_lyrics = 2


class ParserTypeEnum(Enum):
    youtube = 1
    songlyrics = 2
    js_enums = 3
    with_headers = 4
