from os import path, sep
from queue import Queue


class Parser:

    some_queue = Queue()
    fail_download_queue = Queue()

    __queue_size_max = None

    @property
    def queue_size_max(self):
        return self.__queue_size_max

    @queue_size_max.setter
    def queue_size_max(self, value):
        self.__queue_size_max = value

    current_working_dir = path.dirname(__file__) + sep
    gen_files_folder = "ParsedFiles" + sep
    sing_file_folder = "GenFolder" + sep

    special_folder = "SomeSpecialFolder" + sep

    download_tries_number = 5
    sleep_time_error = 5

    def clear_queue(self):
        self.some_queue = Queue()
        self.fail_download_queue = Queue()
