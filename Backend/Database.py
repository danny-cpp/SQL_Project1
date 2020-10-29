import sqlite3

from Backend.DatabaseInterface import *
from prettytable import PrettyTable
from datetime import datetime


# Database object control and establish, as well as terminate connection to the server.
# It has methods allows outsiders to interact with the database
class Database(DatabaseInterface):

    # Constructor establish connection to database. If database not exist, it will
    # create new instance.
    def __init__(self, path):
        self.__path = path
        self.__conn = sqlite3.connect(self.__path)
        print("Connecting to database successfully")

    # The lifetime of the connection is defined to be when the connection object is created
    # until we define to terminate it
    def __del__(self):
        self.__conn.close()
        print("Connection successfully terminated")

    # This method accept a UID input and a user create SQL query. If the user
    # already existed, it will throw a Boolean false, else, true
    def requestUIDCheck(self, uid):
        find_user_SQL = "SELECT * FROM USERS U WHERE U.UID = '" + str(uid) + "';"
        print(find_user_SQL)
        uid = self.requestQuery(find_user_SQL, internal_call=True, debug_mode=False)
        if len(uid) == 0:
            return True

        return False

    def requestQuery(self, query_string, retriever=True, col_name=[],
                     internal_call=False, debug_mode=False):

        # for debugging purpose, turn this off for official version
        if debug_mode:
            print(query_string)

        # If the query is a retriever i.e. SELECT...
        if retriever:
            cursor = self.__conn.execute(query_string)
            self.__conn.commit()
            table = PrettyTable()
            table.field_names = col_name

            # If it is not an internal call, display
            if not internal_call:
                for row in cursor:
                    table.add_row(row)
                print(table)

            records = cursor.fetchall()
            return records

        else:
            self.__conn.execute(query_string)
            self.__conn.commit()

    # Use this function to generate a new and unique post ID. Execute this method
    # will provide a unique PID
    def requestNewPID(self):
        get_new_pid_SQL = "SELECT MAX(P.PID) FROM POSTS P;"
        print(get_new_pid_SQL)
        pid = self.requestQuery(get_new_pid_SQL, True, internal_call=True)
        pid = pid[0][0]
        pid = int(pid[1:]) + 100
        pid = 'p' + str(pid)
        return pid

    def getCurrentTime(self):
        today_date = datetime.today().strftime('%Y-%m-%d')
        return today_date


if __name__ == '__main__':
    server = Database()
    server.requestQuery("SELECT * FROM users;", True)
    server.requestNewPID()
    print(server.requestUIDCheck("u600"))
