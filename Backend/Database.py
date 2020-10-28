import sqlite3

from Backend.DatabaseInterface import *


# Database object control and establish, as well as terminate connection to the server.
# It has methods allows outsiders to interact with the database
class Database(DatabaseInterface):
    # Constructor establish connection to database. If database not exist, it will
    # create new instance.
    def __init__(self):
        self.__conn = sqlite3.connect('myDB.db')
        print("Open database successfully")

    # The lifetime of the connection is defined to be when the connection object is created
    # until we define to terminate it
    def __del__(self):
        self.__conn.close()

    # This method accept a UID input and a user create SQL query. If the user
    # already existed, it will throw a Boolean false, else, true
    @staticmethod
    def requestUIDCheck(uid):
        return True

    # Call backend with a SQL string
    def requestQuery(self, query_string):
        print(query_string)
        pass

    # Use this function to generate a new and unique post ID
    @staticmethod
    def requestNewPID():
        return "p200"