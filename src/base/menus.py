import threading
from asyncio import run

from src.parsers.parser_youtube import YoutubeParser
from src.parsers.parser_songlyrics import SonglyricsParser
from src.parsers.parser_get_with_headers import GetWithHeadersParser

from src.base.parser import Parser
from src.base.enums import YoutubeParserOptionsEnum, SonglyricsOptionsEnum
from src.base.depfuns import confirmation
from src.base.decorators import *

from src.web_enum_parser.main import main as web_enum_parser_main
from src.base.config_dataclass import ConfigDataclass


class Menu:
    youtube_pars = YoutubeParser()
    songlyrics_pars = SonglyricsParser()
    get_with_headers_pars = GetWithHeadersParser()

    threads_max_number = ConfigDataclass.threads_number
    threads_list = []

    def main_menu(self):
        while True:
            print("Choose action:\n"
                  "'1' Download from youtube\n"
                  "'2' Download lyrics from songlyrics.com\n"
                  "'3' Download from site with js and enum\n"
                  "'4' Download from site with get and headers\n"
                  "'0' Close program")
            inp = input()
            if inp == "1":
                try:
                    self.__youtube_playlist_menu()
                except Exception as e:
                    print(e)
            elif inp == "2":
                try:
                    self.__songlyrics_menu()
                except Exception as e:
                    print(e)
            elif inp == "3":
                try:
                    run(web_enum_parser_main())
                except Exception as e:
                    print(e)
            elif inp == "4":
                try:
                    run(self.get_with_headers_pars.menu())
                except Exception as e:
                    print(e)
            elif inp == "0":
                print("Closing program")
                break
            else:
                print("Wrong input")

    def __songlyrics_menu(self):
        while True:
            self.songlyrics_pars.clear_queue()
            self.threads_list = []
            print("Choose option:\n"
                  "'1' Download one group lyric\n"
                  "'2' Download all group lyrics\n"
                  "'0' Back")
            inp = input()
            if inp == "1":
                option = SonglyricsOptionsEnum.one_lyric.value
                self.__download_options_songlyrics_one(option)

            elif inp == "2":
                option = SonglyricsOptionsEnum.all_lyrics.value
                self.__download_options_songlyrics_group(option)

            elif inp == "0":
                break
            else:
                print("Wrong input")

    def __youtube_playlist_menu(self):
        while True:
            self.youtube_pars.clear_queue()
            self.threads_list = []
            print("Choose option:\n"
                  "'1' Download one mp4 video\n"
                  "'2' Download one opus audio\n"
                  "'3' Download playlist mp4 videos\n"
                  "'4' Download playlist opus audio\n"
                  "'0' Back")
            inp = input()
            if inp == "1":
                option = YoutubeParserOptionsEnum.one_video.value
                self.__download_options_youtube_one(option)

            elif inp == "2":
                option = YoutubeParserOptionsEnum.one_audio.value
                self.__download_options_youtube_one(option)

            elif inp == "3":
                option = YoutubeParserOptionsEnum.playlist_video.value
                self.__download_options_youtube_playlist(option)

            elif inp == "4":
                option = YoutubeParserOptionsEnum.playlist_audio.value
                self.__download_options_youtube_playlist(option)

            elif inp == "0":
                break
            else:
                print("Wrong input")

    def start_download_menu(self, some_parser: Parser):
        threads_number = 1
        queue_size = some_parser.some_queue.qsize()
        some_parser.queue_size_max = queue_size
        if queue_size < self.threads_max_number + 1:
            threads_number = queue_size
        else:
            threads_number = self.threads_max_number

        return threads_number

    def __download_options_songlyrics_one(self, option):
        self.__queue_menu_one(self.songlyrics_pars, None)
        if self.songlyrics_pars.download_from_songlyrics_check(option):
            self.songlyrics_pars.print_queue_elems()
            self.songlyrics_pars.queue_size_max = self.songlyrics_pars.some_queue.qsize()
            print(self.songlyrics_pars.queue_size_max)
            if confirmation():
                self.__songlyrics_start_downloading(self.start_download_menu(self.songlyrics_pars), option)
                self.songlyrics_pars.print_result()

    def __download_options_songlyrics_group(self, option):
        self.__songlyrics_queue_menu_group(self.songlyrics_pars, option)
        self.songlyrics_pars.print_queue_elems()
        self.songlyrics_pars.queue_size_max = self.songlyrics_pars.some_queue.qsize()
        print(self.songlyrics_pars.queue_size_max)
        if confirmation():
            self.__songlyrics_start_downloading(self.start_download_menu(self.songlyrics_pars), option)
            self.songlyrics_pars.print_result()

    def __download_options_youtube_one(self, option):
        self.__queue_menu_one(self.youtube_pars, None)
        if self.youtube_pars.download_from_youtube_check(option):
            self.youtube_pars.print_queue_elems()
            print(self.youtube_pars.some_queue.qsize())
            if confirmation():
                self.__youtube_start_downloading(self.start_download_menu(self.youtube_pars), option)
                self.youtube_pars.print_result()

    def __download_options_youtube_playlist(self, option):
        self.__youtube_queue_menu_playlist(self.youtube_pars, option)
        self.youtube_pars.print_queue_elems()
        print(self.youtube_pars.some_queue.qsize())
        if confirmation():
            self.__youtube_start_downloading(self.start_download_menu(self.youtube_pars), option)
            self.youtube_pars.print_result()

    @start_downloading_decorator
    def __get_with_headers_pars_start_downloading(self, threads_number, option):
        thr = threading.Thread(target=self.get_with_headers_pars.download_from_url,
                               args=[option],
                               daemon=False)
        self.threads_list.append(thr)

    @start_downloading_decorator
    def __songlyrics_start_downloading(self, threads_number, option):
        thr = threading.Thread(target=self.songlyrics_pars.download_from_songlyrics,
                               args=[option],
                               daemon=False)
        self.threads_list.append(thr)

    @start_downloading_decorator
    def __youtube_start_downloading(self, threads_number, option):
        thr = threading.Thread(target=self.youtube_pars.download_from_youtube,
                               args=[option],
                               daemon=False)
        self.threads_list.append(thr)

    @staticmethod
    @queue_menu_decorator
    def __queue_menu_one(some_parser: Parser, option, url=None):
        some_parser.some_queue.put([url, some_parser.sing_file_folder])

    @staticmethod
    @queue_menu_decorator
    def __songlyrics_queue_menu_group(some_parser: SonglyricsParser, option, url=None):
        print(some_parser.download_from_songlyrics_check(option, url))

    @staticmethod
    @queue_menu_decorator
    def __youtube_queue_menu_playlist(some_parser: YoutubeParser, option, url=None):
        print(some_parser.download_from_youtube_check(option, url))
