import asyncio

from src.web_enum_parser.parser_web_enum import ParserWebEnum
from src.web_enum_parser.enums_classes import LinkType


async def main():
    try:
        print("Enter link without enum:")
        # https://test/{i}
        link = input()
        if link:
            enum_parser = ParserWebEnum(link)
            asyncio.create_task(enum_parser.parse_from_web(LinkType.en.value))
    except Exception as e:
        print(e)
    return
