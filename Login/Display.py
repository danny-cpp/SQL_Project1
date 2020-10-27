import Login.LoginInterface
import Object.User

class Display(Login.LoginInterface):
    # This method should create an interface allows the user to choose whether
    # they are new user, or returning user. If new user, go to createNewUser().
    # If old user, go to login
    @staticmethod
    def welcomeScreen():
        key = input("Are you a new user? y / n")
        if ( key == "y"):
            Display.createNewUser()
        else:
            Display.login()

    # This method should be static, when call create a new user, with username
    # and password object, with a unique ID (call the hash function here). If
    # UID already exist, throw exception
    @staticmethod
    def createNewUser():
        usrname = input("Please enter your name: ")
        pwd = input("Please enter your password: ")
        city = input("Please enter your city: ")
        usr = Object.User(usrname, pwd, city)


    # This method should takes in 2 string argument and give a unique integer ID,
    # this should not result in any hash collision for at least 1 million input.
    # Try using Apache library for this one
    @staticmethod
    def newUserHash(username, password, city, date_of_create):
        pass

    # This method should ask the user for username and pass word. Password should be
    # hidden.
    @staticmethod
    def login():
        # Return a user object, where it has all the attributes bellow
        usrname = input("Please enter your name: ")
        pwd = input("Please enter your password: ")
        return Object.User.User.login(usrname,pwd)

    # Should return userID
    def getUID(self):
        return Object.User.User.getUid()

    # Should return username
    def getUsername(self):
        return Object.User.User.getName()

    # Should return user password
    def getPassword(self):
        return Object.User.User.getPwd()

    # Should return Date of Create
    def getCreateDate(self):
        return Object.User.User.getCrdate()