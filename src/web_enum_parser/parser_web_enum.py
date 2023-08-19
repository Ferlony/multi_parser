import time
import os
import signal
from pathlib import Path

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as Firefox_Options

from src.web_enum_parser.depfuns import (check_dirs, get_file_content, write_content_in_file,
                                     check_part_files, create_new_dir, get_program_root)
from src.web_enum_parser.enums_classes import LinkType, VideoQuality


class ParserWebEnum:
    def __init__(self, link: str):
        self.__link = link
        self.link_without_spec_signs = self.link.replace(os.sep, "").replace(":", "")
        self.last_enum_file = os.path.dirname(os.path.abspath(__file__)) + os.sep + "Logs" + os.sep + self.link_without_spec_signs
        self.special_folder_path = self.link_without_spec_signs + os.sep

    @property
    def link(self):
        return self.__link

    @link.setter
    def link(self, value):
        self.__link = value

    max_try = 5
    sleep_time = 5
    download_await_time = 3600
    window_size = {"x": 200, "y": 1600}
    default_download_dir = get_program_root() + os.sep + "ParsedFiles" + os.sep + "WebEnum" + os.sep

    def __driver_creator(self, folder_path):
        my_firefox_profile = webdriver.FirefoxProfile()

        firefox_options = Firefox_Options()
        firefox_options.headless = True

        my_firefox_profile.set_preference("browser.download.folderList", 2)
        my_firefox_profile.set_preference("browser.download.manager.showWhenStarting", False)
        my_firefox_profile.set_preference("browser.download.dir", self.default_download_dir + folder_path)
        my_firefox_profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")

        driver = webdriver.Firefox(firefox_profile=my_firefox_profile, options=firefox_options)
        # driver.set_window_size(self.window_size.get("x"), self.window_size.get("y"))
        # driver.set_window_position(1920 - self.window_size.get("x") * 2 - 50, 0)
        # driver.minimize_window()

        return driver

    async def __await_download_file(self, folder_path):
        counter = 0
        time.sleep(self.sleep_time)
        while True:
            files = sorted(Path(folder_path).iterdir(), key=os.path.getmtime)
            check_counter = 0
            out_check_counter = 10
            for each in files:
                if counter == len(files):
                    return True
                if str(each).endswith(".part"):
                    counter = 0
                    time.sleep(self.sleep_time)
                else:
                    check_counter += 1
                    time.sleep(0.5)
                    if check_counter == out_check_counter:
                        check_counter = 0
                        counter += 1

    async def __download_file_type_en(self, url, folder_path):
        driver = self.__driver_creator(folder_path)
        driver.implicitly_wait(self.sleep_time)
        driver.get(url)

        js = "showDownload()"
        driver.execute_script(js)
        driver.implicitly_wait(self.sleep_time)

        download_link_best_quality = driver.find_elements(By.CLASS_NAME, 'download')
        download_link_best_quality[-1].click()

        # Wait for the file to download
        # wait = WebDriverWait(self.driver, self.download_await_time)
        # wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, '.txt')))
        driver.implicitly_wait(self.sleep_time)
        if await self.__await_download_file(self.default_download_dir + folder_path):
            driver.close()

    async def __download_file_type_ru(self, url, folder_path):
        driver = self.__driver_creator(folder_path)
        driver.implicitly_wait(self.sleep_time)
        driver.get(url)

        list_of_videos = driver.find_elements(By.ID, "my-player")
        print(list_of_videos)
        os.kill(os.getpid(), signal.SIGKILL)

        # for each in VideoQuality:
        #     try:
        #         list_of_videos.
        #         # str(each.value)

    async def parse_from_web(self, link_type):
        check_dirs()
        check_part_files(self.default_download_dir)

        i = int(get_file_content(self.last_enum_file, "1"))

        counter = 0
        while True:
            try:
                counter += 1
                print(f"Enum: {i}")

                url = ""
                if link_type == LinkType.ru.value:
                    url = self.link + str(i)
                elif link_type == LinkType.en.value:
                    url = self.link + "episode-" + str(i) + ".html"
                else:
                    raise Exception("Unknown link_type")

                status_code = requests.get(url).status_code

                if status_code == 200:
                    create_new_dir(self.default_download_dir + self.special_folder_path)

                    if link_type == LinkType.ru.value:
                        await self.__download_file_type_en(url, self.special_folder_path)
                    elif link_type == LinkType.en.value:
                        await self.__download_file_type_ru(url, self.special_folder_path)
                    else:
                        raise Exception("Unknown link_type")

                    counter = 0
                    i += 1
                    write_content_in_file(self.last_enum_file, i)
                    print(f"File downloaded\nnext enum {i} saved")
                    time.sleep(self.sleep_time)

                elif (status_code == LinkType.en_not_found_status_code.value) or \
                        (status_code == LinkType.ru_not_found_status_code.value):
                    print(f"Last enum {i}")
                    write_content_in_file(self.last_enum_file, i)
                    print(f"last enum {i} saved")
                    break
                else:
                    print(status_code)
                    if counter >= self.max_try:
                        print("max try reached - out")
                        write_content_in_file(self.last_enum_file, i)
                        print(f"last enum {i} saved")
                        break
                    print(f"Counter: {counter}")
                    time.sleep(self.sleep_time)
            except Exception as e:
                print(e)
                return -1
