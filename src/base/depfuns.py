from os import path


def confirmation():
    while True:
        print("Are you sure?\n'1' Yes\n'0' No")
        inp = input()
        if inp == "1":
            return True
        elif inp == "0":
            return False
        else:
            print("Wrong input")


def add_string_to_file(item: str, file_name="parser_get_with_headers.txt"):
    if not path.exists(file_name):
        with open(file_name, 'w') as f:
            pass
    
    with open(file_name, "a") as f:
        f.write(item)
        f.write("\n")
