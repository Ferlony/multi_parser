from web_enum_parser.parser_web_enum import ParserWebEnum
import asyncio


async def main():
    try:
        print("Enter link without enum:")
        link = input()
        if link:
            enum_parser = ParserWebEnum(link)
            asyncio.create_task(enum_parser.parse_from_web())
    except Exception as e:
        print(e)
    return
