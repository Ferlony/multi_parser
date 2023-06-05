import time
import os
from web_enum_parser.depfuns import check_dirs, get_file_content, write_content_in_file, check_part_files, create_new_dir, get_program_root
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from pathlib import Path
from selenium.webdriver.firefox.options import Options as Firefox_Options

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
            for each in files:
                if counter == len(files):
                    return True
                if str(each).endswith(".part"):
                    counter = 0
                    time.sleep(self.sleep_time)
                else:
                    counter += 1

    async def __download_with_driver(self, url, folder_path):
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

    async def parse_from_web(self, js_exec=True):
        check_dirs()
        check_part_files(self.default_download_dir)
        i = get_file_content(self.last_enum_file)

        counter = 0
        while True:
            try:
                counter += 1
                print(f"Enum: {i}")
                url = self.link + str(i)
                status_code = requests.get(url).status_code
                if status_code == 200:
                    create_new_dir(self.default_download_dir + self.special_folder_path)
                    # await self.__download_with_driver(url)
                    await self.__download_with_driver(url, self.special_folder_path)
                    counter = 0
                    i += 1
                    write_content_in_file(self.last_enum_file, i)
                    print(f"File downloaded\nnext enum {i} saved")
                    time.sleep(self.sleep_time)
                elif status_code == 500:
                    print(f"Last enum {i}")
                    write_content_in_file(self.last_enum_file, i)
                    print(f"last enum {i} saved")
                    break
                else:
                    if counter >= self.max_try:
                        print("max try reached - out")
                        write_content_in_file(self.last_enum_file, i)
                        print(f"last enum {i} saved")
                        break
                    print(f"Counter: {counter}")
                    time.sleep(self.sleep_time)
            # except KeyboardInterrupt:
            #     write_content_in_file(self.last_enum_file, i)
            #     print(f"last enum {i} saved")
            #     return -1
            except Exception as e:
                print(e)
                return -1
