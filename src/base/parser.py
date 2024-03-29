from queue import Queue
from os import path
from os import mkdir
from os import sep

from src.base.config_dataclass import ConfigDataclass


class Parser(ConfigDataclass):

    some_queue = Queue()
    fail_download_queue = Queue()

    __queue_size_max = 0

    @property
    def queue_size_max(self):
        return self.__queue_size_max

    @queue_size_max.setter
    def queue_size_max(self, value):
        self.__queue_size_max = value

    def check_dirs(self, title_folder=None):
        if not title_folder:
            title_folder = self.sing_file_folder
        if ConfigDataclass.flag_for_default_path:
            if not path.exists(path.abspath(__file__) + sep + "ParsedFiles"):
                try:
                    mkdir("ParsedFiles")
                except Exception as e:
                    print(e)
            if not path.exists(self.default_full_folder_path):
                try:
                    mkdir(self.default_full_folder_path)
                except Exception as e:
                    print(e)
            if not path.exists(self.default_full_folder_path + title_folder):
                try:
                    mkdir(self.default_full_folder_path + title_folder)
                except Exception as e:
                    print(e)
        return True

    def print_queue_elems(self):
        queue_arr = self.some_queue.queue
        for url, folder in queue_arr:
            print(url)

    def print_queue_status(self):
        print(self.queue_size_max - self.some_queue.qsize(), "/", self.queue_size_max)

    def calculate_queue(self):
        return self.queue_size_max - self.some_queue.qsize() - self.fail_download_queue.qsize()

    def print_result(self):
        print("\n========\nFinished")
        print(f"Downloaded {self.calculate_queue()} / {self.queue_size_max}")
        print(f"Download Failure {self.fail_download_queue.qsize()}")
        for i in self.fail_download_queue.queue:
            print(i)

    def clear_queue(self):
        self.some_queue = Queue()
        self.fail_download_queue = Queue()
