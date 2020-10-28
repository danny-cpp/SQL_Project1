from Login.LoginInterface import *
from Object.User import *


class Display(LoginInterface):
    # This method should create an interface allows the user to choose whether
    # they are new user, or returning user. If new user, go to createNewUser().
    # If old user, go to login
    @staticmethod
    def welcomeScreen():
        # Danh: What if user enter something wrong (ex: 'a')? Throw somekind of exception
        # or ask user input again.
        acceptable = ['y', 'n']
        key = input("Are you a new user? y / n")
        while True:
            if (key in acceptable):
                if key == 'y':
                    Display.loginScreen()
                    break
                if key == 'n':
                    Display.createNewUser()
                    break
            else:
                key = input("Wrong input, please try again. Are you a new user? y / n")

    # This method should be static, when call create a new user, with username
    # and password object, with a unique ID (call the hash function here). If
    # UID already exist, throw exception
    @staticmethod
    def createNewUser():
        uid = input("Please enter a unique ID: ")
        usrname = input("Please enter your name: ")
        pwd = input("Please enter your password: ")
        city = input("Please enter your city: ")
        # Call for a new ID to be generated

        usr = User(uid, usrname, pwd, city)

    # This method should ask the user for username and pass word. Password should be
    # hidden.
    @staticmethod
    def loginScreen():
        # Return a user object, where it has all the attributes bellow
        uid = input("Please enter your UID: ")
        pwd = input("Please enter your password: ")
        current_user = User.login(uid, pwd)
        return current_user


if __name__ == '__main__':
    Display.welcomeScreen()

    #key != 'y' or key != 'n'