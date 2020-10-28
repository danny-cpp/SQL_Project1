class LoginInterface:
    # This method should create an interface allows the user to choose whether
    # they are new user, or returning user. If new user, go to createNewUser().
    # If old user, go to login
    @staticmethod
    def welcomeScreen(svr):
        pass

    # This method should me static, when call create a new user, with username
    # and password object, with a unique ID (call the hash function here). If
    # UID already exist, throw exception
    @staticmethod
    def createNewUser(svr):
        pass

    # This method should ask the user for username and pass word. Password should be
    # hidden.
    @staticmethod
    def loginScreen(svr):
        # Return a user object, where it has all the attributes bellow
        pass


