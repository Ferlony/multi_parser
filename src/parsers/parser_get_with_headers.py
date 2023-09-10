from os import sep, path, makedirs, remove
from asyncio import run

import requests
from bs4 import BeautifulSoup
import aiofiles
import aiohttp

from src.base.parser import Parser
from src.base.decorators import download_for_threads_decorator
from src.base.depfuns import add_string_to_file


class GetWithHeadersParser(Parser):
    def __init__(self, site_url=Parser.download_default_url):
        self.HEADERS = {"User-Agent": Parser.user_agent}
        self.site_url = site_url

    __title_folder = None

    @property
    def title_folder(self):
        return self.__title_folder

    @title_folder.setter
    def title_folder(self, value):
        self.__title_folder = value

    def download_check(self):
        return self.check_dirs()

    @staticmethod
    def __put_in_parser_queue(items):
        for each in items:
            Parser.some_queue.put(each)

    def menu(self):
        while True:
            print("Choose option:\n"
                  "'1' Download from url\n"
                  "'0' Back")
            inp = input()
            if inp == "1":
                url = input("Enter url:\n")
                links, uniq_name = self.get_links(url)
                for i in range(0, len(links)):
                    link_items = list(links[i].items())[0]
                    name = link_items[0]
                    link = link_items[1]
                    run(self.download_video(link, uniq_name, name))
            elif inp == "0":
                break
            else:
                print("Wrong input")

    def no_menu(self, url):
        run(self.download_links(url))

    def get_links(self, url):
        print("headers:\n", self.HEADERS)
        # Очистка URL
        if url[:5] == "https":
            url = "/" + url.split("/")[3]

        elif url[:6] == self.site_url:
            url = "/" + url.split("/")[1]

        if url[0] != "/":
            url = "/" + url

        if url[-4:] == "html":
            url = "/" + url.split("/")[1]
        print("")

        # Получаем html страницу со всеми видива материаломи
        html = requests.get(f"{self.site_url}{url}", headers=self.HEADERS)
        content = BeautifulSoup(html.content, "lxml")

        # Оригинальное название
        uniq_name = content.find("div", class_="under_video_additional the_hildi").text.split(".")[-1:][0][
                    23:-24].replace(" ", "-")
        name_exceptions = [":", "/", "*", "\"", "<", ">", "|", " "]
        for i in range(len(name_exceptions)):
            uniq_name = uniq_name.replace(name_exceptions[i], "")

        # Находим ссылки на все страницы серий и также фильмов
        links_to_page = []
        # Определяем класс первых серий
        if content.find("div", class_="watch_l").find_all("a")[0].get("href")[:-4] == "html":
            video_class = " ".join(content.find("div", class_="watch_l").find("a").get("class"))
        else:
            video_class = " ".join(content.find("div", class_="watch_l").find_all("a")[1].get("class"))

        # Находим ссылки видео первого класса
        block = content.find_all("a", class_=video_class)
        for item in block:
            links_to_page.append(f"{self.site_url}{item.get('href')}")

        # Меняем класс
        if video_class == "short-btn black video the_hildi":
            video_class = "short-btn green video the_hildi"
        elif video_class == "short-btn green video the_hildi":
            video_class = "short-btn black video the_hildi"

        # Находим ссылки видео второго класса
        block = content.find_all("a", class_=video_class)
        for item in block:
            links_to_page.append(f"{self.site_url}{item.get('href')}")

        # Офомляем красивые имена видеов
        video_name = []
        for i in range(len(links_to_page)):
            video_name.append(links_to_page[i][len(self.site_url + url) + 1:-5].replace("/", " "))

        quick_parsing = False
        file_name = f"{Parser.download_path_playlists_videos}{sep}{uniq_name}-1080p.txt"

        # quick_parsing = True
        # file_name = f"catalog/{uniq_name}-480p.txt"
        print("")

        # Получаем ссылки на все видео
        links_to_vidio = []
        for i in range(len(links_to_page)):
            print(f"Parse {i + 1} video link...")
            # Подгоняем адресс под серию
            site_url = links_to_page[i]
            html = requests.get(site_url, headers=self.HEADERS)
            content = BeautifulSoup(html.content, "lxml")

            # Определяем конкретный блок видео
            block = content.find("div", class_="border_around_video no-top-right-border")
            if block is None:
                block = content.find("div", class_="border_around_video")

            # Останавливаемся если запрещенно в России или его нет на сайте
            if i == 0:
                if block.find("source") is None:
                    input(f"\nSorry, {uniq_name} is not available in Russia :(\nEnter anything to exit > ")
                    raise GeneratorExit("WE DIDN'T FIND THIS CONTENT")
                    pass

            # Находим ссылку
            if not quick_parsing:
                video_resolution = block.find("source").get("src")
            elif quick_parsing:
                video_resolution = block.find("source", res="480").get("src")

            # Запихиваем найденую ссылку в общий тер. лист
            links_to_vidio.append({video_name[i]: video_resolution})

            # Завершение
            if i == len(links_to_page) - 1:
                print("finished!\n")

        # Выводим все ссылки на все серии
        for i in range(len(links_to_vidio)):
            print("\n", links_to_vidio[i])

        # Создаем католог
        # try:
        #     os.mkdir("catalog")
        # except FileExistsError: pass

        # Добовляем в нашу папку текст. файл со всеми ссылками
        # with open(file_name, "w") as file:
        #     for i in range(len(links_to_vidio)):
        #         file.write(f"{links_to_vidio[i]}\n")

        # link_items = list(links_to_vidio[i].items())[0]
        # name = link_items[0]
        # link = link_items[1]

        return links_to_vidio, uniq_name

    async def download_links(self, url):
        links, uniq_name = self.get_links(url)


        if not path.exists(Parser.download_path_playlists_videos + uniq_name + sep):
            makedirs(Parser.download_path_playlists_videos + uniq_name + sep)

        last_name_index = 0
        for i in range(0, len(links)):
            link_items = list(links[i].items())[0]
            name = link_items[0]
            link = link_items[1]

            if not path.exists(Parser.download_path_playlists_videos + uniq_name + sep + name + ".mp4"):
                if i > 0:
                    remove(Parser.download_path_playlists_videos + uniq_name + sep + list(links[i - 1].items())[0][0] + ".mp4")
                    last_name_index = i - 1
                    break
                else:
                    last_name_index = i
                    break

        add_string_to_file(str(uniq_name) + "\n==========\n")
        for i in range(last_name_index, len(links)):
            link_items = list(links[i].items())[0]
            name = link_items[0]
            link = link_items[1]

            print(f"started {i}: {name}.mp4")
            async with aiohttp.ClientSession(raise_for_status=True, headers=self.HEADERS) as cli:
                async with cli.get(link, timeout=None) as r:
                    async with aiofiles.open(Parser.download_path_playlists_videos + uniq_name + sep + name + ".mp4", "wb+") as f:
                        async for d in r.content.iter_any():
                            await f.write(d) if d else None
            add_string_to_file(str(i) + '.' + " " + str(name) + ".mp4")


            print(f"{Parser.download_path_playlists_videos + uniq_name + sep + name + '.mp4'} downloaded!")

    @staticmethod
    def check_title_folder_exist(title_folder):
        if not path.exists(Parser.download_path_playlists_videos + title_folder + sep):
            makedirs(Parser.download_path_playlists_videos + title_folder + sep)

    async def download_video_threads(self):
        while not self.some_queue.empty():
            queue_list = self.some_queue.get()
            name, link = queue_list

            

            async with aiohttp.ClientSession(raise_for_status=True, headers=self.HEADERS) as cli:
                async with cli.get(link, timeout=None) as r:
                    async with aiofiles.open(
                            Parser.download_path_playlists_videos + self.title_folder + sep + name + ".mp4", "wb+") as f:
                        async for d in r.content.iter_any():
                            await f.write(d) if d else None


            print(f"{Parser.download_path_playlists_videos + self.title_folder + sep + name + '.mp4'} downloaded!")
