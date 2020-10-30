from Login.LoginInterface import *
from Object.User import *
from Backend.Database import *


class Display(LoginInterface):
    # This method should create an interface allows the user to choose whether
    # they are new user, or returning user. If new user, go to createNewUser().
    # If old user, go to login
    @staticmethod
    def welcomeScreen(svr):
        state = 0 # Good state
        print("\n\n________________________Welcome to SQLite Mini!________________________")

        acceptable = ['y', 'n', 'quit']
        key = Display.prompt_user("Are you an existing user? y / n ", True)
        prompt = False
        while not prompt:
            if key in acceptable and key == 'y':
                state = Display.loginScreen(svr)
                prompt = True
            elif key in acceptable and key == 'n':
                state = Display.createNewUser(svr)
                prompt = True

            else:
                key = Display.prompt_user("Wrong input, please try again. Are you an existing user? y / n ",True)

        return state

    # This method should be static, when call create a new user, with username
    # and password object, with a unique ID (call the hash function here). If
    # UID already exist, throw exception
    @staticmethod
    def createNewUser(svr):
        uid = Display.prompt_user("Please enter  unique ID of your choice: ", True)
        while svr.requestUIDCheck(uid):
            uid = Display.prompt_user("UID already taken, please input another UID: ",True)
        usrname = Display.prompt_user("Please enter your name: ", True)
        pwd = input("Please enter your password: ")
        city = Display.prompt_user("Please enter your city: ", True)
        # Call for a new ID to be generated
        cr_date = svr.getCurrentTime()
        usr = User(uid, usrname, pwd, city, cr_date)
        inp = Display.prompt_user("Are you sure with this these information? If not, type 'n' to go to the Welcome Screen else Hit Enter", True)
        if inp == 'n':
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
        uid = Display.prompt_user("Please enter your UID: ", True)
        while not svr.requestUIDCheck(uid):
            uid = Display.prompt_user("UID have not registered, check your UID or enter 'back' to WelcomeScreen: ", True)
            if uid == 'back':
                return None

        query_string = f"SELECT * FROM USERS U WHERE U.UID = '{uid}';"
        login_authentication = svr.requestQuery(query_string, retriever=True, col_name=[],
                                                internal_call=True, debug_mode=False)

        pwd = input("Please enter your password: ")
        while pwd != login_authentication[0][2]:
            pwd = input("Wrong password. Please enter your password again: ")
        current_user = User(login_authentication[0][0], login_authentication[0][1], login_authentication[0][2],
                            login_authentication[0][3], login_authentication[0][4])

        return current_user
    #It will take prompt as an argument string , force_lower is true when you want to compare with lower string
    @staticmethod
    def prompt_user(prompt, force_lower=False):
        user_inp = input(prompt)
        if force_lower:
            user_inp = user_inp.lower()
        if user_inp == 'quit':
            exit()
        return user_inp


if __name__ == '__main__':
    Display.createNewUser()

    #key != 'y' or key != 'n'