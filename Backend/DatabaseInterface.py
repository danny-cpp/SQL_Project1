class DatabaseInterface:
    # This method accept a UID input and a user create SQL query. If the user
    # already existed, it will throw a Boolean false, else, true
    @staticmethod
    def requestUIDCheck(uid):
        return False

    # Call backend with a SQL string
    @staticmethod
    def requestQuery(query_string):
        pass

    # Use this function to generate a new and unique post ID
    @staticmethod
    def requestNewPID():
        return "p200"

