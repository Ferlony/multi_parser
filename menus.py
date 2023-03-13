from youtube_parser import YoutubeParser
from parser import Parser
import threading
from enums import YoutubeParserOptionsEnum
from depfuns import conformation


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
            print("Choose option:\n"
                  "'1' Download one mp4 video\n"
                  "'2' Download one opus audio\n"
                  "'3' Download playlist mp4 videos\n"
                  "'4' Download playlist opus audio\n"
                  "'0' Back")
            inp = input()
            if inp == "1":
                option = YoutubeParserOptionsEnum.one_video.value
                self.__queue_menu_one(self.youtube_pars)
                if self.youtube_pars.download_from_youtube_check(option):
                    self.youtube_pars.print_queue_title_and_url()
                    if conformation():
                        self.__start_download_menu(option)
                        self.youtube_pars.print_result()
                    else:
                        self.youtube_pars.clear_queue()

            elif inp == "2":
                option = YoutubeParserOptionsEnum.one_audio.value
                self.__queue_menu_one(self.youtube_pars)
                if self.youtube_pars.download_from_youtube_check(option):
                    self.youtube_pars.print_queue_title_and_url()
                    if conformation():
                        self.__start_download_menu(option)
                        self.youtube_pars.print_result()
                    else:
                        self.youtube_pars.clear_queue()

            elif inp == "3":
                option = YoutubeParserOptionsEnum.playlist_video.value
                print("Enter youtube url:")
                url = input()
                if url:
                    if self.youtube_pars.download_from_youtube_check(option, url):
                        self.youtube_pars.print_queue_title_and_url()
                        if conformation():
                            self.__start_download_menu(option)
                            self.youtube_pars.print_result()
                        else:
                            self.youtube_pars.clear_queue()

            elif inp == "4":
                option = YoutubeParserOptionsEnum.playlist_audio.value
                print("Enter youtube url:")
                url = input()
                if url:
                    if self.youtube_pars.download_from_youtube_check(option, url):
                        self.youtube_pars.print_queue_title_and_url()
                        if conformation():
                            self.__start_download_menu(option)
                            self.youtube_pars.print_result()
                        else:
                            self.youtube_pars.clear_queue()

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
        print("Fill the queue:")
        while True:
            print("Enter youtube url:")
            url = input()
            if url:
                some_parser.some_queue.put(url)
            print("Continue?\n"
                  "'1' Yes\n"
                  "'0' No")
            inp = input()
            if inp == "1":
                pass
            elif inp == "0":
                break
            else:
                print("Wrong input")
