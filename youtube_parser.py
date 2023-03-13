import time
import pytube
from depfuns import create_dir, create_new_dir
from os import path, sep
from parser import Parser
from exceptions import CouldNotDownloadError, UnsupportedOptionError
from enums import YoutubeParserOptionsEnum


class YoutubeParser(Parser):

    special_folder = "YouTubeFiles" + sep
    full_folder_path = Parser.current_working_dir + Parser.gen_files_folder + special_folder

    playlist_title_folder = None

    def __print_status(self, url, yt: pytube.YouTube):
        print(self.queue_size_max - self.some_queue.qsize(), "/", self.queue_size_max)
        print("Url:\n", url)
        print(yt.title)

    def __check_dirs(self, title_folder=None):
        if not title_folder:
            title_folder = self.sing_file_folder
        if not path.exists(self.full_folder_path):
            create_dir(self.gen_files_folder, self.gen_files_folder, self.special_folder)
        if not path.exists(self.full_folder_path + title_folder):
            create_new_dir(self.full_folder_path, title_folder)

    def __check_playlist(self, playlist: pytube.Playlist):
        print("Chosen playlist: ", playlist)
        print("Playlist title: ", playlist.title)
        amount_playlist_videos = len(playlist.video_urls)
        print('Number of videos in playlist: %s' % amount_playlist_videos)

        self.__check_dirs(self.playlist_title_folder)

        for i in playlist:
            self.some_queue.put(i)
        return True

    def print_result(self):
        print("\n========\nFinished")
        print(f"Downloaded {self.queue_size_max - self.some_queue.qsize() - self.fail_download_queue.qsize()} /",
              self.queue_size_max)
        print(f"Download Failure {self.fail_download_queue.qsize()}")
        for i in self.fail_download_queue.queue:
            print(i)

    def print_queue_title_and_url(self):
        queue_arr = self.some_queue.queue
        title_and_url = []
        for i in queue_arr:
            try_counter = 0
            while True:
                if try_counter > 4:
                    print("Loop tries out")
                    break
                try:
                    try_counter += 1
                    title_and_url.append({i: pytube.YouTube(i).title})
                    break
                except Exception as e:
                    print("Title adding ex: ", e)
                    time.sleep(self.sleep_time_error)
        for i in title_and_url:
            print(i)

    def download_from_youtube(self, option):
        while not self.some_queue.empty():
            url = self.some_queue.get()

            try_counter = 0
            while True:
                if try_counter >= self.download_tries_number:
                    break
                try:
                    try_counter += 1
                    yt = pytube.YouTube(url)
                    self.__print_status(url, yt)
                    try:
                        if option == YoutubeParserOptionsEnum.one_video.value:
                            self.__download_youtube_one_video(yt, self.full_folder_path + self.sing_file_folder)
                        elif option == YoutubeParserOptionsEnum.one_audio.value:
                            self.__download_youtube_one_audio(yt, self.full_folder_path + self.sing_file_folder)
                        elif option == YoutubeParserOptionsEnum.playlist_video.value:
                            self.__download_youtube_one_video(yt, self.full_folder_path + self.playlist_title_folder)
                        elif option == YoutubeParserOptionsEnum.playlist_audio.value:
                            self.__download_youtube_one_audio(yt, self.full_folder_path + self.playlist_title_folder)
                        break
                    except CouldNotDownloadError:
                        self.fail_download_queue.put({yt.title, url})
                        break
                except Exception as e:
                    print(e)
                    print("Loop try: ", try_counter)

    def download_from_youtube_check(self, option, url=None):
        if option == YoutubeParserOptionsEnum.one_video.value:
            self.__check_dirs()
            return True
        elif option == YoutubeParserOptionsEnum.one_audio.value:
            self.__check_dirs()
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

    def __download_youtube_one_video(self, yt: pytube.YouTube, save_path):
        counter = 0
        while True:
            if counter >= self.download_tries_number:
                print("Couldn't download ", yt.title)
                raise CouldNotDownloadError
            try:
                counter += 1
                yt.streams.get_highest_resolution().download(save_path)
                print("##########")
                print("Downloaded\n", yt.title)
                break
            except Exception as e:
                print(e, "\nDownload try: ", counter)
                time.sleep(self.sleep_time_error)

    def __download_youtube_one_audio(self, yt: pytube.YouTube, save_path):
        counter = 0
        while True:
            if counter >= self.download_tries_number:
                print("Couldn't download ", yt.title)
                raise CouldNotDownloadError
            try:
                counter += 1
                yt.streams.filter(only_audio=True, audio_codec="opus").order_by("abr").last().download(
                    save_path,
                    yt.title.replace(sep, "") + ".opus")
                print("##########")
                print("Downloaded\n", yt.title)
                break
            except Exception as e:
                print(e, "\nDownload try: ", counter)
                time.sleep(self.sleep_time_error)
