from os import path, sep

from dataclasses import dataclass
import configparser

import src
from src.base.exceptions import InappropriateThreadsNumberError


@dataclass
class ConfigDataclass:
    # base download path
    project_dir = path.dirname(src.__file__)

    # default download structure path
    gen_files_folder = "ParsedFiles" + sep
    sing_file_folder = "GenFolder" + sep
    special_folder = "SomeSpecialFolder" + sep
    default_full_folder_path = project_dir + gen_files_folder + special_folder

    # init config
    config = configparser.ConfigParser()
    config_path = project_dir + sep + "config.ini"
    config.read(config_path)

    # threads configure
    threads_number = int(config["DEFAULT"]["threads_number"])
    max_possible_threads = int(config["DEFAULT"]["max_possible_threads"])
    if threads_number not in range(1, max_possible_threads + 1):
        raise InappropriateThreadsNumberError

    # on errors
    download_tries_number = int(config["DEFAULT"]["download_tries_number"])
    sleep_time_error = int(config["DEFAULT"]["sleep_time_error"])

    # for parser_get_with_headers
    user_agent = str(config["DEFAULT"]["user_agent"])
    download_default_url = str(config["DEFAULT"]["download_default_url"])

    # not default paths
    flag_for_default_path = int(config["DOWNLOAD_PATH"]["flag_for_default_path"])
    if flag_for_default_path == 0:
        flag_for_default_path = False
    else:
        flag_for_default_path = True

    download_path_playlists_videos = str(config["DOWNLOAD_PATH"]["download_path_playlists_videos"])
    download_path_single_videos = str(config["DOWNLOAD_PATH"]["download_path_single_videos"])

    download_path_playlists_music = str(config["DOWNLOAD_PATH"]["download_path_playlists_music"])
    download_path_single_music = str(config["DOWNLOAD_PATH"]["download_path_single_music"])

    download_path_text_files_playlist = str(config["DOWNLOAD_PATH"]["download_path_text_files_playlist"])
    download_path_single_text_files = str(config["DOWNLOAD_PATH"]["download_path_single_text_files"])
