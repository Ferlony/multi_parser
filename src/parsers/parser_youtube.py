import time
from os import sep

import pytube

from src.base.parser import Parser
from src.base.exceptions import CouldNotDownloadError, UnsupportedOptionError
from src.base.enums import YoutubeParserOptionsEnum
from src.base.decorators import *


class YoutubeParser(Parser):

    special_folder = "YouTubeFiles" + sep
    full_folder_path = Parser.current_working_dir + Parser.gen_files_folder + special_folder

    playlist_title_folder = None

    def __check_playlist(self, playlist: pytube.Playlist):
        print("Chosen playlist: ", playlist)
        print("Playlist title: ", playlist.title)
        amount_playlist_videos = len(playlist.video_urls)
        print('Number of videos in playlist: %s' % amount_playlist_videos)

        self.check_dirs(self.playlist_title_folder)

        for i in playlist:
            self.some_queue.put([i, playlist.title])
        return True

    def print_queue_elems(self):
        queue_arr = self.some_queue.queue
        title_and_url = []
        for url, folder in queue_arr:
            try_counter = 0
            while True:
                if try_counter > 4:
                    print("Loop tries out")
                    break
                try:
                    try_counter += 1
                    title_and_url.append([url, pytube.YouTube(url).title])
                    break
                except Exception as e:
                    print("Title adding ex: ", e)
                    time.sleep(self.sleep_time_error)
        for i in title_and_url:
            print(i)

    @download_for_threads_shorten_decorator
    def download_from_youtube(self, option, url=None, title_folder=None):
        yt = pytube.YouTube(url)
        print(yt.title)
        try:
            if option == YoutubeParserOptionsEnum.one_video.value:
                self.__download_youtube_one_video(yt, self.full_folder_path + title_folder)
            elif option == YoutubeParserOptionsEnum.one_audio.value:
                self.__download_youtube_one_audio(yt, self.full_folder_path + title_folder)
            elif option == YoutubeParserOptionsEnum.playlist_video.value:
                new_title_folder = title_folder + "_video" + sep
                self.__download_youtube_one_video(yt, self.full_folder_path + new_title_folder)
            elif option == YoutubeParserOptionsEnum.playlist_audio.value:
                new_title_folder = title_folder + "_audio" + sep
                self.__download_youtube_one_audio(yt, self.full_folder_path + new_title_folder)

        except CouldNotDownloadError:
            self.fail_download_queue.put({yt.title, url})

    def download_from_youtube_check(self, option, url=None):
        if option == YoutubeParserOptionsEnum.one_video.value:
            self.check_dirs()
            return True
        elif option == YoutubeParserOptionsEnum.one_audio.value:
            self.check_dirs()
            return True
        elif option == YoutubeParserOptionsEnum.playlist_video.value:
            playlist = pytube.Playlist(url)
            playlist_title_folder = playlist.title + "_video" + sep
            self.playlist_title_folder = playlist_title_folder
            return self.__check_playlist(playlist)
        elif option == YoutubeParserOptionsEnum.playlist_audio.value:
            playlist = pytube.Playlist(url)
            playlist_title_folder = playlist.title + "_audio" + sep
            self.playlist_title_folder = playlist_title_folder
            return self.__check_playlist(playlist)
        else:
            raise UnsupportedOptionError

    @download_youtube_one_file_decorator
    def __download_youtube_one_video(self, yt: pytube.YouTube, save_path):
        yt.streams.get_highest_resolution().download(save_path)

    @download_youtube_one_file_decorator
    def __download_youtube_one_audio(self, yt: pytube.YouTube, save_path):
        yt.streams.filter(only_audio=True, audio_codec="opus").order_by("abr").last().download(
            save_path,
            yt.title.replace(sep, "") + ".opus")
