from os import path, sep
from dataclasses import dataclass


@dataclass
class ParserDataClass:
    current_working_dir = path.dirname(__file__) + sep

    gen_files_folder = "ParsedFiles" + sep
    sing_file_folder = "GenFolder" + sep
    special_folder = "SomeSpecialFolder" + sep
    full_folder_path = current_working_dir + gen_files_folder + special_folder

    download_tries_number = 5
    sleep_time_error = 5
