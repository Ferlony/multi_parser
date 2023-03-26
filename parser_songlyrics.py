from parser import Parser
from os import sep
from bs4 import BeautifulSoup
import requests
from enums import SonglyricsOptionsEnum
from exceptions import UnsupportedOptionError, CouldNotDownloadError
import time


class SonglyricsParser(Parser):

    special_folder = "songlyrics" + sep
    full_folder_path = Parser.current_working_dir + Parser.gen_files_folder + special_folder

    group_title_folder = None

    def download_from_songlyrics_check(self, option):
        if option == SonglyricsOptionsEnum.one_lyric.value:
            self.check_dirs()
            return True
        elif option == SonglyricsOptionsEnum.all_lyrics.value:
            pass
        else:
            raise UnsupportedOptionError

    def download_from_songlyrics(self, option):
        while not self.some_queue.empty():
            queue_list = self.some_queue.get()
            url, title_folder = queue_list

            try_counter = 0
            while True:
                if try_counter >= self.download_tries_number:
                    break
                try:
                    try_counter += 1
                    self.print_queue_status()
                    print("Url:\n", url)
                    try:
                        if option == SonglyricsOptionsEnum.one_lyric.value:
                            """
                            self.__download_youtube_one_video(yt, self.full_folder_path + title_folder)
                            """
                            self.__download_lyric(url, self.full_folder_path + title_folder)
                        elif option == SonglyricsOptionsEnum.all_lyrics.value:
                            """
                            new_title_folder = title_folder + "_video" + sep
                            self.__download_youtube_one_video(yt, self.full_folder_path + new_title_folder)
                            """
                            pass
                        break
                    except CouldNotDownloadError:
                        self.fail_download_queue.put(url)
                        break
                except Exception as e:
                    print(e)
                    print("Loop try: ", try_counter)

    def __download_songlyrics_one_lyric(self, url, save_path):
        counter = 0
        while True:
            if counter >= self.download_tries_number:
                print("Couldn't download ", url)
                raise CouldNotDownloadError
            try:
                counter += 1
                self.__download_lyric(url, save_path)
                print("##########")
                print("Downloaded\n", url)
                break
            except Exception as e:
                print(e, "\nDownload try: ", counter)
                time.sleep(self.sleep_time_error)

    @staticmethod
    def __download_lyric(url, save_path):
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")

        song_name = soup.find('div', class_='pagetitle').find('h1').get_text('\n', strip=True)
        song = soup.find('p', id="songLyricsDiv").get_text()

        with open(save_path + str(song_name) + ".txt", "w") as file:
            file.write(song)
