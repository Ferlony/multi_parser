import argparse

from src.base.menus import Menu
from src.base.no_menu import ParserWorker
from src.base.enums import ParserTypeEnum


def main(*args):
    if len(args) > 0:
        parser_type, action, url = args
        worker = ParserWorker(parser_type, action, url)

        if parser_type == ParserTypeEnum.youtube.value:
            worker.start_youtube()
        elif parser_type == ParserTypeEnum.songlyrics.value:
            worker.start_songlyrics()
        elif parser_type == ParserTypeEnum.js_enums.value:
            worker.start_jsenums()
        elif parser_type == ParserTypeEnum.with_headers.value:
            worker.start_with_headers()
        else:
            return

    else:
        Menu().main_menu()


if __name__ == '__main__':

    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument("parser_type", type=int)
    arg_parser.add_argument("action", type=int)
    arg_parser.add_argument("url", type=str)

    pargs = arg_parser.parse_args()
    print(pargs)

    main(pargs)
