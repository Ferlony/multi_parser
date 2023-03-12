from os import path, sep


class CouldNotDownloadError(Exception):
    def __init__(self, message="CouldNotDownloadError"):
        super().__init__(message)


class Parser:
    current_working_dir = path.dirname(__file__) + sep
    gen_files_folder = "ParsedFiles" + sep
    sing_file_folder = "GenFolder" + sep

    special_folder = "SomeSpecialFolder" + sep

    download_tries_number = 5
    sleep_time_error = 5
