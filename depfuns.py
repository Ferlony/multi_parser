# from os import sep
from os import mkdir
# from shutil import rmtree


def conformation():
    while True:
        print("Are you sure?\n'1' Yes\n'0' No")
        inp = input()
        if inp == "1":
            return True
        elif inp == "0":
            return False
        else:
            print("Wrong input")


def create_dir(current_working_dir, gen_files_folder, additional_files_folder):
    try:
        mkdir(current_working_dir + gen_files_folder + additional_files_folder)
    except:
        try:
            mkdir(current_working_dir + gen_files_folder)
            mkdir(current_working_dir + gen_files_folder + additional_files_folder)
        except:
            return
        # except:
        #     rmtree(files_location_path_abs + gen_files_folder + additional_files_folder)
        #     mkdir(files_location_path_abs + gen_files_folder + additional_files_folder)
    return


def create_new_dir(full_files_path, new_dir):
    try:
        mkdir(full_files_path + new_dir)
    except:
        return
    return
