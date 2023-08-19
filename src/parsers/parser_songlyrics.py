from os import sep

import requests
from bs4 import BeautifulSoup

from src.base.parser import Parser
from src.base.enums import SonglyricsOptionsEnum
from src.base.exceptions import UnsupportedOptionError
from src.base.decorators import *


class SonglyricsParser(Parser):

    def __init__(self):
        self.special_folder = "songlyrics" + sep
        self.default_full_folder_path = Parser.project_dir + Parser.gen_files_folder + self.special_folder

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

    @download_for_threads_decorator
    def download_from_songlyrics(self, option, url=None, title_folder=None):
        if option == SonglyricsOptionsEnum.one_lyric.value:
            if Parser.flag_for_default_path:
                self.__download_songlyrics_one_lyric(url, self.default_full_folder_path + title_folder)
            else:
                self.__download_songlyrics_one_lyric(url, Parser.download_path_single_text_files)
        elif option == SonglyricsOptionsEnum.all_lyrics.value:
            if Parser.flag_for_default_path:
                self.__download_songlyrics_one_lyric(url, self.default_full_folder_path + title_folder)
            else:
                self.__download_songlyrics_one_lyric(url, Parser.download_path_text_files_playlist)

    @download_one_file_decorator
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
