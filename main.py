from menus import Menu
from youtube_parser import YoutubeParser
import queue


def main(*args):
    Menu(args[0], args[1]).main_menu()


if __name__ == '__main__':
    youtube_pars = YoutubeParser()
    some_queue = queue.Queue()
    main(youtube_pars, some_queue)
