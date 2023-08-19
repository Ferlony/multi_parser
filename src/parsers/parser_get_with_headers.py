from os import sep

import requests
from bs4 import BeautifulSoup

from src.base.parser import Parser


class GetWithHeadersParser(Parser):
    def __init__(self, site_url=Parser.download_default_url):
        self.HEADERS = {"User-Agent": Parser.user_agent}
        self.site_url = site_url

    def download_check(self):
        return self.check_dirs()

    def download_from_url(self, url):
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
        uniq_name = content.find("div", class_="under_video_additional the_hildi").text.split(".")[-1:][0][23:-24].replace(" ", "-")
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

        #Офомляем красивые имена видеов
        video_name = []
        for i in range(len(links_to_page)):
            video_name.append(links_to_page[i][len(self.site_url+url)+1:-5].replace("/", " "))

        quick_parsing = False
        file_name = f"{Parser.download_path_playlists_videos}{sep}{uniq_name}-1080p.txt"

        # quick_parsing = True
        # file_name = f"catalog/{uniq_name}-480p.txt"
        print("")

        #Получаем ссылки на все видео
        links_to_vidio = []
        for i in range(len(links_to_page)):
            print(f"Parse {i + 1} video link...")
            #Подгоняем адресс под серию
            site_url = links_to_page[i]
            html = requests.get(site_url, headers=self.HEADERS)
            content = BeautifulSoup(html.content, "lxml")

            #Определяем конкретный блок видео
            block = content.find("div", class_="border_around_video no-top-right-border")
            if block is None:
                block = content.find("div", class_="border_around_video")

            #Останавливаемся если запрещенно в России или его нет на сайте
            if i == 0:
                if block.find("source") is None:
                    input(f"\nSorry, {uniq_name} is not available in Russia :(\nEnter anything to exit > ")
                    raise GeneratorExit ("WE DIDN'T FIND THIS ANIME")
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
        with open(file_name, "w") as file:
            for i in range(len(links_to_vidio)):
                file.write(f"{links_to_vidio[i]}\n")

        print("\nfinished!")
