import threading
from asyncio import run

from src.parsers.parser_youtube import YoutubeParser
from src.parsers.parser_songlyrics import SonglyricsParser
from src.base.parser import Parser
from src.parsers.parser_get_with_headers import GetWithHeadersParser
from src.base.config_dataclass import ConfigDataclass
from src.base.enums import YoutubeParserOptionsEnum
from src.base.decorators import *


class ParserWorker:
    def __init__(self, parser_type: int, action: int, url: str):
        self.parser_type = parser_type
        self.action = action
        self.url = url

    threads_max_number = ConfigDataclass.threads_number
    threads_list = []

    youtube_pars = YoutubeParser()
    songlyrics_pars = SonglyricsParser()
    get_with_headers_pars = GetWithHeadersParser()



    def start_songlyrics(self):
        pass

    def start_jsenums(self):
        pass

# Youtube
    def start_youtube(self):
        if self.action == YoutubeParserOptionsEnum.one_video.value:
            self.__download_options_youtube_one(self.action)
        elif self.action == YoutubeParserOptionsEnum.one_audio.value:
            self.__download_options_youtube_one(self.action)
        elif self.action == YoutubeParserOptionsEnum.playlist_video.value:
            self.__download_options_youtube_playlist(self.action)
        elif self.action == YoutubeParserOptionsEnum.playlist_audio.value:
            self.__download_options_youtube_playlist(self.action)
        else:
            return

    def __download_options_youtube_one(self, option):
        self.__queue_menu_one(self.youtube_pars, None, self.url)
        if self.youtube_pars.download_from_youtube_check(option):
            self.youtube_pars.print_queue_elems()
            self.__youtube_start_downloading(self.start_download_menu(self.youtube_pars), option)
            self.youtube_pars.print_result()

    def __download_options_youtube_playlist(self, option):
        self.__youtube_queue_menu_playlist(self.youtube_pars, option, self.url)
        self.youtube_pars.print_queue_elems()
        self.__youtube_start_downloading(self.start_download_menu(self.youtube_pars), option)
        self.youtube_pars.print_result()

    def start_download_menu(self, some_parser: Parser):
        threads_number = 1
        queue_size = some_parser.some_queue.qsize()
        some_parser.queue_size_max = queue_size
        if queue_size < self.threads_max_number + 1:
            threads_number = queue_size
        else:
            threads_number = self.threads_max_number

        return threads_number

    @staticmethod
    def __queue_menu_one(some_parser: Parser, option, url=None):
        some_parser.some_queue.put([url, some_parser.sing_file_folder])

    @staticmethod
    def __youtube_queue_menu_playlist(some_parser: YoutubeParser, option, url=None):
        some_parser.download_from_youtube_check(option, url)

    @start_downloading_decorator
    def __youtube_start_downloading(self, threads_number, option):
        thr = threading.Thread(target=self.youtube_pars.download_from_youtube,
                               args=[option],
                               daemon=False)
        self.threads_list.append(thr)
# ===========================================

# With headers
    def start_with_headers(self):
        self.get_with_headers_pars.no_menu(self.url)
