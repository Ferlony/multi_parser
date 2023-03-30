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
