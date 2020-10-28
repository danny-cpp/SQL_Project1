import sqlite3

from Backend.DatabaseInterface import *
from prettytable import PrettyTable


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
        print("Connection successfully terminated")

    # This method accept a UID input and a user create SQL query. If the user
    # already existed, it will throw a Boolean false, else, true
    @staticmethod
    def requestUIDCheck(uid):
        return True

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


if __name__ == '__main__':
    server = Database()
    server.requestQuery("SELECT * FROM users;", True)
