from Functionality.FunctionalityInterace import *
from Functionality.Pages import Pages
from Object.User import *


class Menu(FunctionalityInterface):

    # As we build a finite state machine here, each number will be each state of this machine.
    # For this particular case: 0 = Main Menu, 1 = Post Question, 2 = Post Question, 3 = Search Post
    # It also needs to operate on a server and a user object
    def __init__(self, svr, usr, state, chosenPID):
        self.__sever = svr
        self.__user = usr
        self.__state = state
        self.__chosenPID = chosenPID # Store the current current chosen post ID

        # if state == 0:
        #     Menu.menuNavigate()
        if state == 1:
            self.postQuestion()
        elif state == 2:
            self.searchPost()
        elif state == 3:
            self.postActionMenu()
        elif state == 4:
            self.answerQuestion()

    # After login successfully, user will be in the navigation panel. Display all
    # options the user has.
    @staticmethod
    def menuNavigate():
        acceptable_value = ['1', '2']
        print("\n\n________________________Main menu________________________")
        print("Input the corresponding number to navigate to that option")
        print("Type 'back' anytime you want to return to Main Menu")
        print("1. Post Question")
        print("2. Search Post  ")
        inp = input("Please type in the number correspond to the option you choose: ")
        while inp not in acceptable_value:
            inp = input("Unrecognized input. Please type in the number correspond to the option you choose: ")

        if inp == '1':
            return 1, None
        if inp == '2':
            return 2, None

    # Accept string as input, return SQL string statement update. Assume that UID
    # will be provided. It must implement a hash function to create a pid
    def postQuestion(self):
        uid = self.__user.getUid()
        print("\n\n________________________Make Post________________________")
        title = input("What is your title? ")
        body = input("What do you want to post? ")
        date = self.__sever.getCurrentTime()
        pid = self.__sever.requestNewPID()
        sql = ("INSERT INTO POSTS (pid, pdate, title, body, poster) " +
               f"VALUES ('{pid}',DATE('{date}'),'{title}','{body}','{uid}');")
        self.__sever.requestQuery(sql, retriever=False, debug_mode=True)
        return 0, None


    #########################################################
    ## This section needs more work to move cursor around!
    #########################################################
    # Accepting keyword, order SQL query
    def searchPost(self):
        print("\n\n_______________________Search Post________________________")
        keyword = input("Search Keyword: ").lower()
        sql = ("SELECT * FROM posts P " +
               f"WHERE lower(P.title) LIKE lower('%{keyword}%') " +
               "UNION " +
               "SELECT * FROM posts P " +
               f"WHERE lower(P.body) LIKE lower('%{keyword}%') " +
               "UNION " +
               "SELECT P.* FROM posts P JOIN tags T ON P.pid = T.pid " +
               f"WHERE lower(T.tag) LIKE lower('%{keyword}%');")

        column_array = ['pid', 'post date', 'title', 'content', 'poster']
        records = self.__sever.requestQuery(sql, retriever=True, col_name=column_array, internal_call=True,
                                            fetch_many=True, debug_mode=True)

        # This section display them page by page
        bookkeeper = Pages(records, 0, col_name=column_array)
        bookkeeper.printPages()
        tmp_bool = True

        pid = input("Choose the post by type in the PID to interact with it, or 'back to return to main menu: ")
        if pid == 'back':
            return 0, None
        elif pid == 'prev':
            bookkeeper.prevPage()
            tmp_bool = False
        elif pid == 'next':
            bookkeeper.nextPage()
            tmp_bool = False

        # If the user input an invalid PID we request again
        sql1 = f"SELECT * FROM POSTS P WHERE P.PID = '{pid}';"
        record = self.__sever.requestQuery(sql1, retriever=True, internal_call=True,
                                           debug_mode=True)

        while len(record) == 0:
            if tmp_bool: print("Invalid PID, ", end="")
            pid = input("Please choose the post by type in the PID to interact with it, or 'back' " +
                        "to return to main menu: ")

            if pid == 'back':
                return 0, None
            elif pid == 'prev':
                bookkeeper.prevPage()
                tmp_bool = False
                continue
            elif pid == 'next':
                bookkeeper.nextPage()
                tmp_bool = False
                continue

            sql1 = f"SELECT * FROM POSTS P WHERE P.PID = '{pid}'"
            record = self.__sever.requestQuery(sql1, retriever=True, internal_call=True,
                                               debug_mode=True)

            tmp_bool = True
        return 3, pid

    # Post-Action-Group

    # This window will be called if a user chose a post
    def postActionMenu(self):
        print("\n_______________________Action Menu________________________")
        print("You have chosen post " + self.__chosenPID)
        acceptable_value = ['1', '2', 'back']

        column_array = ['pid', 'post date', 'title', 'content', 'poster']
        sql1 = f"SELECT * FROM POSTS P WHERE P.PID = '{self.__chosenPID}'"
        self.__sever.requestQuery(sql1, retriever=True, col_name=column_array, debug_mode=True)

        print("Input the corresponding number to navigate to that option")
        print("Type 'back' anytime you want to return to Main Menu")
        print("1. Answer Question")
        print("2. Vote Post")

        inp = input("Please type in the number correspond to the option you choose: ")
        while inp not in acceptable_value:
            inp = input("Unrecognized input. Please type in the number correspond to the option you choose: ")

        if inp == 'back':
            return 0, None
        if inp == '1':
            return 4, self.__chosenPID
        if inp == '2':
            return 5, self.__chosenPID

    # Accepting string answer, order a SQL query update
    def answerQuestion(self):
        answer = input("Please enter your answer: ")
        # sql = "update posts set body = " + answer +" where pid = " + pid + ";"
        return 0

    # Order an sql string to update vote according to pid
    def vote(self):
        vote = input("Do you want to vote the post? y/n")
        if vote == 'y':
            pass # sql = "insert into votes(pid, vdate, uid) values (" + pid + ", " + datetime.datetime.now()+ ", "+uid+");"
        return 0


if __name__ == '__main__':
    Menu.menuNavigate()
