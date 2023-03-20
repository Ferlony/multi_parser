from youtube_parser import YoutubeParser
from parser import Parser
import threading
from enums import YoutubeParserOptionsEnum
from depfuns import confirmation


class Menu:
    youtube_pars = YoutubeParser()

    threads_max_number = 10
    threads_list = []

    def main_menu(self):
        while True:
            print("Choose action:\n"
                  "'1' Download from youtube\n"
                  "'0' Close program")
            inp = input()
            if inp == "1":
                try:
                    self.__youtube_playlist_menu()
                except Exception as e:
                    print(e)
            elif inp == "t":
                pass
            elif inp == "0":
                print("Closing program")
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
                  "'5' Set number of threads (10 by default)\n"
                  "'0' Back")
            inp = input()
            if inp == "1":
                option = YoutubeParserOptionsEnum.one_video.value
                self.__queue_menu_one(self.youtube_pars)
                if self.youtube_pars.download_from_youtube_check(option):
                    self.youtube_pars.print_queue_title_and_url()
                    if confirmation():
                        self.__start_download_menu(option)
                        self.youtube_pars.print_result()

            elif inp == "2":
                option = YoutubeParserOptionsEnum.one_audio.value
                self.__queue_menu_one(self.youtube_pars)
                if self.youtube_pars.download_from_youtube_check(option):
                    self.youtube_pars.print_queue_title_and_url()
                    if confirmation():
                        self.__start_download_menu(option)
                        self.youtube_pars.print_result()

            elif inp == "3":
                option = YoutubeParserOptionsEnum.playlist_video.value
                self.__queue_menu_playlist(self.youtube_pars, option)
                self.youtube_pars.print_queue_title_and_url()
                if confirmation():
                    self.__start_download_menu(option)
                    self.youtube_pars.print_result()

            elif inp == "4":
                option = YoutubeParserOptionsEnum.playlist_audio.value
                self.__queue_menu_playlist(self.youtube_pars, option)
                self.youtube_pars.print_queue_title_and_url()
                if confirmation():
                    self.__start_download_menu(option)
                    self.youtube_pars.print_result()

            elif inp == "5":
                print("Enter number of threads from 1 to 10")
                try:
                    thr_number = int(input())
                    if thr_number in range(1, 11):
                        self.threads_max_number = thr_number
                        print(f"Threads number successfully set {thr_number}")
                    else:
                        print("Wrong input")
                except Exception as e:
                    print("Wrong input")
                    print(e)

            elif inp == "0":
                break
            else:
                print("Wrong input")

    def __start_download_menu(self, option):
        threads_number = 1
        queue_size = self.youtube_pars.some_queue.qsize()
        self.youtube_pars.queue_size_max = queue_size
        if queue_size < self.threads_max_number + 1:
            threads_number = queue_size
        else:
            threads_number = self.threads_max_number
        for i in range(0, threads_number):
            thr = threading.Thread(target=self.youtube_pars.download_from_youtube,
                                   args=[option],
                                   daemon=False)
            self.threads_list.append(thr)

        for i in self.threads_list:
            i.start()

        for j in self.threads_list:
            j.join()

    @staticmethod
    def __queue_menu_one(some_parser: Parser):
        while True:
            print("Fill the queue\n"
                  "'1' Add in queue\n"
                  "'0' Finish")
            inp = input()
            if inp == "1":
                print("Enter youtube url:")
                url = input()
                if url:
                    try_counter = 0
                    while True:
                        if try_counter > some_parser.download_tries_number:
                            print("Couldn't add")
                            break
                        try:
                            try_counter += 1
                            some_parser.some_queue.put([url, some_parser.sing_file_folder])
                            break
                        except Exception as e:
                            print("try count: ", try_counter)
                            print(e)
            elif inp == "0":
                break
            else:
                print("Wrong input")

    @staticmethod
    def __queue_menu_playlist(some_parser: YoutubeParser, option):
        while True:
            print("Fill the queue\n"
                  "'1' Add in queue\n"
                  "'0' Finish")
            inp = input()
            if inp == "1":
                print("Enter youtube url:")
                url = input()
                if url:
                    try_counter = 0
                    while True:
                        if try_counter > some_parser.download_tries_number:
                            print("Couldn't add")
                            break
                        try:
                            try_counter += 1
                            print(some_parser.download_from_youtube_check(option, url))
                            break
                        except Exception as e:
                            print("try count: ", try_counter)
                            print(e)
            elif inp == "0":
                print("Please wait confirmation")
                break
            else:
                print("Wrong input")
