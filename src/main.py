import argparse

from src.base.menus import Menu
from src.base.no_menu import ParserWorker
from src.base.enums import ParserTypeEnum


def main(*args):
    if len(args) == 3:
        parser_type, action, url = args

        if parser_type and action and url:
            worker = ParserWorker(parser_type, action, url)

            if parser_type == ParserTypeEnum.youtube.value:
                worker.start_youtube()
            elif parser_type == ParserTypeEnum.songlyrics.value:
                worker.start_songlyrics()
            elif parser_type == ParserTypeEnum.js_enums.value:
                worker.start_jsenums()
            elif parser_type == ParserTypeEnum.with_headers.value:
                worker.start_with_headers()
            return

    Menu().main_menu()


if __name__ == '__main__':

    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument("-p", "--parser_type", type=int, required=False, help="youtube = 1\n"
                                                                                  "songlyrics = 2\n"
                                                                                  "js_enums = 3\n"
                                                                                  "with_headers = 4")
    arg_parser.add_argument("-a", "--action", type=int, required=False, help="youtube:\n"
                                                                             "one_video = 1\n"
                                                                             "one_audio = 2\n"
                                                                             "playlist_video = 3\n"
                                                                             "playlist_audio = 4")
    arg_parser.add_argument("-u", "--url", type=str, required=False)

    pargs = arg_parser.parse_args()

    main(pargs.parser_type, pargs.action, pargs.url)
