import time
import pytube
from depfuns import conformation, create_dir, create_new_dir
from os import path, sep


class CouldNotDownloadError(Exception):
    def __init__(self, message="CouldNotDownloadError"):
        super().__init__(message)


class Parser:
    current_working_dir = path.dirname(__file__) + sep
    gen_files_folder = "ParsedFiles" + sep
    sing_file_folder = "GenFolder" + sep

    youtube_files_folder = "YouTubeFiles" + sep
    full_youtube_files_path = current_working_dir + gen_files_folder + youtube_files_folder + sep

    download_tries_number = 5
    sleep_time_error = 5

    def download_youtube_one_video(self, url):
        yt = pytube.YouTube(url)
        print("Url:\n", url)
        print(yt.title)
        if conformation():
            if not path.exists(self.full_youtube_files_path):
                create_dir(self.gen_files_folder, self.gen_files_folder, self.youtube_files_folder)
            if not path.exists(self.full_youtube_files_path + self.sing_file_folder):
                create_new_dir(self.full_youtube_files_path, self.sing_file_folder)
            self.__download_youtube_one_video(yt, self.full_youtube_files_path + self.sing_file_folder)

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
            # except FileNotFoundError as e:
            #     print(e)
            #     raise FileNotFoundError
            except Exception as e:
                print(e, "\nDownload try: ", counter)
                time.sleep(self.sleep_time_error)

    def download_youtube_one_audio(self, url):
        yt = pytube.YouTube(url)
        print("Url:\n", url)
        print(yt.title)
        if conformation():
            if not path.exists(self.full_youtube_files_path):
                create_dir(self.gen_files_folder, self.gen_files_folder, self.youtube_files_folder)
            if not path.exists(self.full_youtube_files_path + self.sing_file_folder):
                create_new_dir(self.full_youtube_files_path, self.sing_file_folder)
            self.__download_youtube_one_audio(yt, self.full_youtube_files_path + self.sing_file_folder)

    def __download_youtube_one_audio(self, yt: pytube.YouTube, save_path):
        counter = 0
        while True:
            if counter >= self.download_tries_number:
                print("Couldn't download ", yt.title)
                raise CouldNotDownloadError
            try:
                counter += 1
                # print(yt.streams.filter(only_audio=True, audio_codec="opus").order_by("abr").last())
                yt.streams.filter(only_audio=True, audio_codec="opus").order_by("abr").last().download(
                    save_path,
                    yt.title.replace(sep, "") + ".opus")
                print("##########")
                print("Downloaded\n", yt.title)
                break
            # except FileNotFoundError as e:
            #     print(e)
            #     raise FileNotFoundError
            except Exception as e:
                print(e, "\nDownload try: ", counter)
                time.sleep(self.sleep_time_error)

    def download_youtube_playlist_video(self, url):
        playlist = pytube.Playlist(url)
        playlist_title_folder = playlist.title + "_video" + sep
        print("Chosen playlist: ", playlist)
        print("Playlist title: ", playlist.title)
        amount_playlist_videos = len(playlist.video_urls)
        current_amount_playlist_videos = 0
        print('Number of videos in playlist: %s' % amount_playlist_videos)
        if conformation():
            if not path.exists(self.full_youtube_files_path):
                create_dir(self.gen_files_folder, self.gen_files_folder, self.youtube_files_folder)
            if not path.exists(self.full_youtube_files_path + playlist_title_folder):
                create_new_dir(self.full_youtube_files_path, playlist_title_folder)
            try_counter = 0
            fail_download_list = []
            while True:
                if try_counter >= self.download_tries_number:
                    break
                try:
                    try_counter += 1
                    for i in range(current_amount_playlist_videos, len(playlist)):
                        yt = pytube.YouTube(playlist[i])
                        print("Current", current_amount_playlist_videos + 1, "/", amount_playlist_videos, "\n", yt.title)
                        try:
                            self.__download_youtube_one_video(yt, self.full_youtube_files_path + playlist_title_folder)
                            try_counter = 0
                            current_amount_playlist_videos += 1
                        # except FileNotFoundError:
                        #     fail_download_list.append({yt.title, playlist[i]})
                        #     current_amount_playlist_videos += 1
                        #     i += 1
                        except CouldNotDownloadError:
                            fail_download_list.append({yt.title, playlist[i]})
                            current_amount_playlist_videos += 1
                            i += 1

                    print("========\nFinished")
                    print(f"Downloaded {amount_playlist_videos - len(fail_download_list)}/{amount_playlist_videos}")
                    print(f"Download Failure {len(fail_download_list)}")
                    for i in fail_download_list:
                        print(i)
                    break
                except Exception as e:
                    print(e)
                    print("Loop try: ", try_counter)

    def download_youtube_playlist_audio(self, url):
        playlist = pytube.Playlist(url)
        playlist_title_folder = playlist.title + "_audio" + sep
        print("Chosen playlist: ", playlist)
        print("Playlist title: ", playlist.title)
        amount_playlist_videos = len(playlist.video_urls)
        current_amount_playlist_videos = 0
        print('Number of videos in playlist: %s' % amount_playlist_videos)
        if conformation():
            if not path.exists(self.full_youtube_files_path):
                create_dir(self.gen_files_folder, self.gen_files_folder, self.youtube_files_folder)
            if not path.exists(self.full_youtube_files_path + playlist_title_folder):
                create_new_dir(self.full_youtube_files_path, playlist_title_folder)
            try_counter = 0
            fail_download_list = []
            while True:
                if try_counter >= self.download_tries_number:
                    break
                try:
                    try_counter += 1
                    for i in range(current_amount_playlist_videos, len(playlist)):
                        yt = pytube.YouTube(playlist[i])
                        print("Current", current_amount_playlist_videos + 1, "/", amount_playlist_videos, "\n", yt.title)
                        try:
                            self.__download_youtube_one_audio(yt, self.full_youtube_files_path + playlist_title_folder)
                            try_counter = 0
                            current_amount_playlist_videos += 1
                        # except FileNotFoundError:
                        #     fail_download_list.append({yt.title, playlist[i]})
                        #     current_amount_playlist_videos += 1
                        #     i += 1
                        except CouldNotDownloadError:
                            fail_download_list.append({yt.title, playlist[i]})
                            current_amount_playlist_videos += 1
                            i += 1

                    print("========\nFinished")
                    print(f"Downloaded {amount_playlist_videos - len(fail_download_list)}/{amount_playlist_videos}")
                    print(f"Download Failure {len(fail_download_list)}")
                    for i in fail_download_list:
                        print(i)
                    break
                except Exception as e:
                    print(e)
                    print("Loop try: ", try_counter)
