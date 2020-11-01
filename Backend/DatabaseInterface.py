class DatabaseInterface:
    # This method accept a UID input and a user create SQL query. If the user
    # already existed, it will throw a Boolean false, else, true
    def requestUIDCheck(self, uid):
        return False

    # Call backend with a SQL string.
    def requestQuery(self, query_string, retriever=True, col_name=[],
                     internal_call=False, debug_mode=False):
        """
        Input argument is an SQL string that will be executed onto the server

        :param query_string: The input SQL string

        :param retriever: If the input is a SELECT statement. i.e. "SELECT
        * FROM ...", turning this argument to True. For setter (UPDATE, DELETE,...),
        turn this arguemnt to False

        :param col_name: The array of column_name

        :param internal_call: Turn to True for internal methods call, turn off and the
        it will not print result. Only turn on if retriever is True

        :param debug_mode: Turn to True to check what the SQL is.

        :return: SQLite3.Cursor object
        """
        pass

    # Use this function to generate a new and unique post ID. Execute this method
    # will provide a unique PID
    def requestNewPID(self):
        # Return a new and unique pid
        pass

    # Return the time at moment of issue in format YYYY-MM-DD
    def getCurrentTime(self):
        pass

    # Use this function to generate a new and unique vote ID. Execute this method
    # will provide a unique vno
    def requestNewVno(self):
        pass

    # This method check the statue of user for special post. If the user
    # already voted, it will throw a Boolean Tru, else, False
    def requestVoteCheck(self, uid, pid):
        pass

    # Check if a user is a privilege user
    def checkIfPrivilege(self, uid):
        pass

    # Check if a post is an answer
    def checkIfAnswer(self):
        pass

    # Check if a post already has an accepted answer. Return False if it have none
    def checkAA(self):
        pass

    # Get the title and body of the post
    def getPost(self, pid):
        pass

if __name__ == '__main__':
    print(DatabaseInterface.requestQuery.__doc__)
