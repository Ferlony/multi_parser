import os
from pathlib import Path


def get_program_root():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.chdir("..")
    location = os.getcwd()
    return location


def check_dirs():
    def check_dir_internal(folder):
        if not os.path.exists(folder):
            os.mkdir(folder)

    program_root_path = get_program_root()
    program_internal_path = os.path.dirname(os.path.abspath(__file__))

    ParsedFiles = "ParsedFiles"
    ParserNameDir = "WebEnum"
    Gen = "Gen"
    Logs = "Logs"

    check_dir_internal(program_root_path + os.sep + ParsedFiles)
    check_dir_internal(program_internal_path + os.sep + Logs)
    check_dir_internal(program_root_path + os.sep + ParsedFiles + os.sep + ParserNameDir)
    check_dir_internal(program_root_path + os.sep + ParsedFiles + os.sep + ParserNameDir + os.sep + Gen)
    return True


def get_file_content(filename, write_if_not: str):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return f.read()
    else:
        with open(filename, "w") as f:
            f.write(write_if_not)
            return write_if_not


def write_content_in_file(filename, value):
    with open(filename, "w") as f:
        f.write(str(value))


def check_part_files(folder_path):
    files = Path(folder_path).iterdir()
    for each in files:
        if str(each).endswith(".part"):
            os.remove(str(each))


def create_new_dir(folder_path):
    try:
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        return 1
    except Exception as e:
        print(e)
        return -1
