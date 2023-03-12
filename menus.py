from youtube_parser import YoutubeParser
from queue import Queue


class Menu:
    def __init__(self, youtube_pars: YoutubeParser, queue: Queue):
        self.youtube_pars = youtube_pars
        self.some_queue = queue

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
                  "'t' Test\n"
                  "'0' Back")
            inp = input()
            if inp == "1":
                print("Enter youtube url:")
                url = input()
                if url:
                    self.youtube_pars.download_youtube_one_video(url)
            elif inp == "2":
                print("Enter youtube url:")
                url = input()
                if url:
                    self.youtube_pars.download_youtube_one_audio(url)
            elif inp == "3":
                print("Enter youtube url:")
                url = input()
                if url:
                    self.youtube_pars.download_youtube_playlist_video(url)
            elif inp == "4":
                print("Enter youtube url:")
                url = input()
                if url:
                    self.youtube_pars.download_youtube_playlist_audio(url)
            elif inp == "t":
                self.youtube_pars.test()
            elif inp == "0":
                break
            else:
                print("Wrong input")

    def __queue_menu(self):
        print("Fill the queue:")
        while True:
            print("Enter youtube url:")
            url = input()
            if url:
                self.some_queue.put(url)
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
