from time import sleep

from src.base.exceptions import CouldNotDownloadError


def download_youtube_one_file_decorator(fun):
    def gen_fun(self, yt, save_path):
        counter = 0
        while True:
            if counter >= self.download_tries_number:
                print("Couldn't download ", yt.title)
                raise CouldNotDownloadError
            try:
                counter += 1
                fun(self, yt, save_path)
                print("##########")
                print("Downloaded\n", yt.title)
                break
            except Exception as e:
                print(e, "\nDownload try: ", counter)
                sleep(self.sleep_time_error)
    return gen_fun


def download_one_file_decorator(fun):
    def gen_fun(self, url, save_path):
        counter = 0
        while True:
            if counter >= self.download_tries_number:
                print("Couldn't download ", url)
                raise CouldNotDownloadError
            try:
                counter += 1
                fun(self, url, save_path)
                print("##########")
                print("Downloaded\n", url)
                break
            except Exception as e:
                print(e, "\nDownload try: ", counter)
                sleep(self.sleep_time_error)
    return gen_fun


def start_downloading_decorator(fun):
    def gen_fun(self, threads_number, option):
        for i in range(0, threads_number):
            fun(self, threads_number, option)

        for i in self.threads_list:
            i.start()

        for j in self.threads_list:
            j.join()
    return gen_fun


def queue_menu_decorator(fun):
    def gen_fun(some_parser, option):
        while True:
            print("Fill the queue\n"
                  "'1' Add in queue\n"
                  "'0' Finish")
            inp = input()
            if inp == "1":
                print("Enter url:")
                url = input()
                if url:
                    try_counter = 0
                    while True:
                        if try_counter > some_parser.download_tries_number:
                            print("Couldn't add")
                            break
                        try:
                            try_counter += 1
                            fun(some_parser, option, url)
                            break
                        except Exception as e:
                            print("try count: ", try_counter)
                            print(e)
            elif inp == "0":
                print("Please wait confirmation")
                break
            else:
                print("Wrong input")
    return gen_fun


def download_for_threads_decorator(fun):
    def gen_fun(self, option):
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
                    try:
                        fun(self, option, url, title_folder)
                        break
                    except CouldNotDownloadError:
                        self.fail_download_queue.put(url)
                        break
                except Exception as e:
                    print(e)
                    print("Loop try: ", try_counter)
    return gen_fun


def download_for_threads_shorten_decorator(fun):
    def gen_fun(self, option):
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
                    fun(self, option, url, title_folder)
                    break
                except Exception as e:
                    print(e)
                    print("Loop try: ", try_counter)
    return gen_fun
