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
    # already existed, it will throw a Boolean Tru, else, False
    def requestUIDCheck(self, uid):
        find_user_SQL = f"SELECT * FROM USERS U WHERE U.UID = '{uid}';"
        user_record = self.requestQuery(find_user_SQL, internal_call=True, debug_mode=True)
        if len(user_record) == 0:
            return False

        return True

    def requestQuery(self, query_string, retriever=True, col_name=[],
                     internal_call=False, debug_mode=False, fetch_many=False):

        # for debugging purpose, turn this off for official version
        if debug_mode:
            print(query_string)

        # If the query is a retriever i.e. SELECT...
        if not fetch_many:  # Retriever should always on, deprecated default argument 'retriever'
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

        elif fetch_many:
            cursor = self.__conn.execute(query_string)
            self.__conn.commit()

            # in this section we fetch data in page. Maximum 2 objects per, then store
            # them in a list
            records = []
            page = cursor.fetchmany(2)
            records.append(page)
            while True:
                page = cursor.fetchmany(2)
                if len(page) == 0:
                    break
                records.append(page)

            return records

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

    # Use this function to generate a new and unique vote ID. Execute this method
    # will provide a unique vno
    def requestNewVno(self):
        get_new_vno_SQL = "SELECT MAX(V.VNO) FROM VOTES V;"
        print(get_new_vno_SQL)
        vno = self.requestQuery(get_new_vno_SQL, True, internal_call=True)
        vno = vno[0][0]
        vno = int(vno[1:]) + 100
        vno = 'v' + str(vno)
        return vno

    # This method check the statue of user for special post. If the user
    # already voted, it will throw a Boolean Tru, else, False
    def requestVoteCheck(self, uid, pid):
        find_vote_SQL = f"SELECT * FROM VOTES V WHERE V.UID = '{uid}' AND V.PID = '{pid}';"
        vote_record = self.requestQuery(find_vote_SQL, internal_call=True, debug_mode=True)
        if len(vote_record) == 0:
            return False
        return True

    # Check if a user is a privilege user
    def checkIfPrivilege(self, uid):
        uid = self.__user.getUid()
        sql = f"SELECT * FROM PRIVILEGED P WHERE P.UID = '{uid}';"
        record = self.__sever.requestQuery(sql, internal_call=True, debug_mode=True)
        if len(record == 0):
            return False
        return True

    # Check if a post is an answer
    def checkIfAnswer(self, pid):
        check_answer_SQL = f"SELECT * FROM ANSWERS A WHERE A.PID = '{pid}';"
        answer_record = self.requestQuery(check_answer_SQL, internal_call=True, debug_mode=True)
        if len(answer_record) == 0:
            return False
        return True



if __name__ == '__main__':
    server = Database("myDB.db")

    print(server.requestQuery("SELECT * FROM TAGS;", fetch_many=True))

    # server.requestNewPID()
    # print(server.requestUIDCheck("u600"))
