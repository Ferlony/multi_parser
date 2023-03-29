from parser import Parser
from os import sep
from bs4 import BeautifulSoup
import requests
from enums import SonglyricsOptionsEnum
from exceptions import UnsupportedOptionError, CouldNotDownloadError
import decorators


class SonglyricsParser(Parser):

    special_folder = "songlyrics" + sep
    full_folder_path = Parser.current_working_dir + Parser.gen_files_folder + special_folder

    group_title_folder = None

    def download_from_songlyrics_check(self, option, url=None):
        if option == SonglyricsOptionsEnum.one_lyric.value:
            self.check_dirs()
            return True
        elif option == SonglyricsOptionsEnum.all_lyrics.value:
            group_title = self.__extract_group_title(url)
            self.group_title_folder = group_title + sep
            return self.__check_group_songs(url)
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
                            self.__download_songlyrics_one_lyric(url, self.full_folder_path + title_folder)
                        elif option == SonglyricsOptionsEnum.all_lyrics.value:
                            self.__download_songlyrics_one_lyric(url, self.full_folder_path + title_folder)
                        break
                    except CouldNotDownloadError:
                        self.fail_download_queue.put(url)
                        break
                except Exception as e:
                    print(e)
                    print("Loop try: ", try_counter)

    @decorators.download_one_file_decorator
    def __download_songlyrics_one_lyric(self, url, save_path):
        self.__download_lyric(url, save_path)

    def __check_group_songs(self, url):
        songs = self.__extract_songs_from_group_url(url)
        print("Chosen group: ", url)
        print("Group title: ", self.group_title_folder.replace(sep, ""))
        print("Number of songs in group page: ", len(songs))

        self.check_dirs(self.group_title_folder)

        for each in songs:
            self.some_queue.put([each, self.group_title_folder])
        return True

    @staticmethod
    def __extract_songs_from_group_url(group_url):
        songs = []
        page = requests.get(group_url)
        soup = BeautifulSoup(page.text, "html.parser")

        song_urls = soup.find("table", class_="tracklist").findAll("a")
        for each in song_urls:
            songs.append(each.get("href"))

        return songs

    @staticmethod
    def __extract_group_title(url):
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")

        group_name = soup.find('div', class_='pagetitle').find('h1').get_text('\n', strip=True)
        return str(group_name).replace(sep, "")

    @staticmethod
    def __download_lyric(url, save_path):
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")

        song_name = soup.find('div', class_='pagetitle').find('h1').get_text('\n', strip=True).replace(sep, "")
        song = soup.find('p', id="songLyricsDiv").get_text()

        with open(save_path + str(song_name) + ".txt", "w") as file:
            file.write(song)
