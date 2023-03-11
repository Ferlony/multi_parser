from parser import Parser


class Menu:
    parser = Parser()

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
                print("Enter youtube url:")
                url = input()
                if url:
                    self.parser.download_youtube_one_video(url)
            elif inp == "2":
                print("Enter youtube url:")
                url = input()
                if url:
                    self.parser.download_youtube_one_audio(url)
            elif inp == "3":
                print("Enter youtube url:")
                url = input()
                if url:
                    self.parser.download_youtube_playlist_video(url)
            elif inp == "4":
                print("Enter youtube url:")
                url = input()
                if url:
                    self.parser.download_youtube_playlist_audio(url)
            elif inp == "0":
                break
            else:
                print("Wrong input")
