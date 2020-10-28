class LoginInterface:
    # This method should create an interface allows the user to choose whether
    # they are new user, or returning user. If new user, go to createNewUser().
    # If old user, go to login
    @staticmethod
    def welcomeScreen():
        pass

    # This method should me static, when call create a new user, with username
    # and password object, with a unique ID (call the hash function here). If
    # UID already exist, throw exception
    @staticmethod
    def createNewUser():
        pass

    # This method should takes in 2 string argument and give a unique integer ID,
    # this should not result in any hash collision for at least 1 million input.
    # Try using Apache library for this one
    @staticmethod
    def newUserHash(username, password, city, date_of_create):
        pass

    # This method should ask the user for username and pass word. Password should be
    # hidden.
    @staticmethod
    def loginScreen():
        # Return a user object, where it has all the attributes bellow
        pass

    # Should return userID
    def getUID(self):
        pass

    # Should return username
    def getUsername(self):
        pass

    # Should return user password
    def getPassword(self):
        pass

    # Should return Date of Create
    def getCreateDate(self):
        pass

