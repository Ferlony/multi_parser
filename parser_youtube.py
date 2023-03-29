import time
import pytube
from os import sep
from parser import Parser
from exceptions import CouldNotDownloadError, UnsupportedOptionError
from enums import YoutubeParserOptionsEnum
import decorators


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

    def download_from_youtube(self, option):
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
                        break
                    except CouldNotDownloadError:
                        self.fail_download_queue.put({yt.title, url})
                        break
                except Exception as e:
                    print(e)
                    print("Loop try: ", try_counter)

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

    @decorators.download_youtube_one_file_decorator
    def __download_youtube_one_video(self, yt: pytube.YouTube, save_path):
        yt.streams.get_highest_resolution().download(save_path)

    @decorators.download_youtube_one_file_decorator
    def __download_youtube_one_audio(self, yt: pytube.YouTube, save_path):
        yt.streams.filter(only_audio=True, audio_codec="opus").order_by("abr").last().download(
            save_path,
            yt.title.replace(sep, "") + ".opus")

