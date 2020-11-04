from InputControl import RegInput
from Login.LoginInterface import *
from Object.User import *
from Backend.Database import *
from InputControl.RegInput import *


class Display(LoginInterface):
    # This method should create an interface allows the user to choose whether
    # they are new user, or returning user. If new user, go to createNewUser().
    # If old user, go to login
    @staticmethod
    def welcomeScreen(svr):
        state = 0 # Good state
        print("\n\n________________________Welcome to SQLite Mini!________________________")
        # Danh: What if user enter something wrong (ex: 'a')? Throw some kind of exception
        # or ask user input again.
        acceptable = ['y', 'n', 'quit']
        key = InputControl.Input("Are you an existing user? y / n ")
        while True:
            if key in acceptable:
                if key == 'y':
                    state = Display.loginScreen(svr)
                    break
                if key == 'n':
                    state = Display.createNewUser(svr)
                    break
                if key == 'quit':
                    exit()
            else:
                key = InputControl.Input("Wrong input, please try again. Are you an existing user? y / n ")

        return state

    # This method should be static, when call create a new user, with username
    # and password object, with a unique ID (call the hash function here). If
    # UID already exist, throw exception
    @staticmethod
    def createNewUser(svr):
        uid = InputControl.Input("Please enter a unique ID: ")
        while svr.requestUIDCheck(uid):
            uid = InputControl.Input("UID already taken, please input another UID: ")
        usrname = InputControl.Input("Please enter your name: ")
        pwd = InputControl.Input("Please enter your password: ", is_pwd=True)
        city = InputControl.Input("Please enter your city: ")

        # Call for a new ID to be generated
        cr_date = svr.getCurrentTime()
        usr = User(uid, usrname, pwd, city, cr_date)
        inp = InputControl.Input("Are you sure with this these information? If not, type 'back' to go to the Welcome Screen")
        if inp == 'back':
            return None
        insert_user = ("INSERT INTO users (uid, name, pwd, city, crdate)" +
                       f" VALUES ('{uid}', '{usrname}', '{pwd}', '{city}', DATE('{cr_date}'));")
        svr.requestQuery(insert_user)

        print("Account successfully created, you will be login right now!")
        return usr

    # This method should ask the user for username and pass word. Password should be
    # hidden.
    @staticmethod
    def loginScreen(svr):
        # Return a user object, where it has all the attributes bellow
        uid = InputControl.Input("Please enter your UID: ")
        while not svr.requestUIDCheck(uid):
            uid = InputControl.Input("UID have not registered, check your UID or enter 'back' to WelcomeScreen: ")
            if uid == 'back':
                return None

        query_string = f"SELECT * FROM USERS U WHERE U.UID = '{uid}';"
        login_authentication = svr.requestQuery(query_string, retriever=True, col_name=[],
                                                internal_call=True, debug_mode=False)

        pwd = InputControl.Input("Please enter your password: ", is_pwd=True)
        while pwd != login_authentication[0][2]:
            pwd = InputControl.Input("Wrong password. Please enter your password again: ", is_pwd=True)
            if pwd == 'back':
                return None
        current_user = User(login_authentication[0][0], login_authentication[0][1], login_authentication[0][2],
                            login_authentication[0][3], login_authentication[0][4])

        return current_user


if __name__ == '__main__':
    Display.createNewUser()

    #key != 'y' or key != 'n'