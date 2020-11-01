from Functionality.FunctionalityInterace import *
from Functionality.PrivilegedInterface import *
from Functionality.Pages import Pages
from Object.User import *


class Menu(FunctionalityInterface, PrivilegeInterface):

    # As we build a finite state machine here, each number will be each state of this machine.
    # For this particular case: 0 = Main Menu, 1 = Post Question, 2 = Post Question, 3 = Search Post
    # It also needs to operate on a server and a user object
    def __init__(self, svr, usr, state, chosenPID):
        self.__sever = svr
        self.__user = usr
        self.__state = state
        self.__chosenPID = chosenPID # Store the current current chosen post ID

    # This is the entry point of the FSM, it call correspond functions with required information
    def menuNavigate(self):
        if self.__state == 0:
            return self.MainMenu()
        if self.__state == 1:
            return self.postQuestion()
        elif self.__state == 2:
            return self.searchPost()
        elif self.__state == 3:
            return self.postActionMenu
        elif self.__state == 4:
            return self.answerQuestion()
        elif self.__state == 5:
            return self.vote()

    # After login successfully, user will be in the navigation panel. Display all
    # options the user has.
    def MainMenu(self):
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

        update_question_sql = ("INSERT INTO QUESTIONS (pid) " +
                               f"VALUES ('{pid}');")

        self.__sever.requestQuery(sql, retriever=False, debug_mode=True)
        self.__sever.requestQuery(update_question_sql, retriever=False, debug_mode=True)
        return 0, None

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

            sql1 = f"SELECT * FROM POSTS P WHERE P.PID = '{pid}';"
            record = self.__sever.requestQuery(sql1, retriever=True, internal_call=True,
                                               debug_mode=True)

            tmp_bool = True
        return 3, pid

    # Post-Action-Group

    # This window will be called if a user chose a post
    @property
    def postActionMenu(self):
        print("\n_______________________Action Menu________________________")
        print("You have chosen post " + self.__chosenPID)
        acceptable_value = ['1', 'back']

        column_array = ['pid', 'post date', 'title', 'content', 'poster']
        sql1 = f"SELECT * FROM POSTS P WHERE P.PID = '{self.__chosenPID}';"
        self.__sever.requestQuery(sql1, retriever=True, col_name=column_array, debug_mode=True)
        privilege_status = self.__sever.checkIfPrivilege(self.__user.getUid())
        post_is_answer = self.__sever.checkIfAnswer(self.__chosenPID)

        print("What do you want to do with this post? ")
        print("Type 'back' anytime you want to return to Main Menu")
        print("1. Vote Post")

        if not post_is_answer:
            acceptable_value.append('2')
            print("2. Answer Question")

        # If a user is a privilege user, they have more options than normal
        if privilege_status:
            acceptable_value.extend(['3', '4', '5'])

            print("\nYou are a privilege user, these options are unique to you: ")
            print("3. Give a badge to this poster")
            print("4. Add a tag to this post")
            print("5. Edit this post")

            if post_is_answer:
                acceptable_value.append('6')
                print("6. Mark as accepted")

        inp = input("Please type in the number correspond to the option you choose: ")
        while inp not in acceptable_value:
            inp = input("Unrecognized input. Please type in the number correspond to the option you choose: ")

        if inp == 'back':
            return 0, None
        if inp == '1':                      # Vote post
            return 5, self.__chosenPID
        if inp == '2':                      # Answer (only if it is not an answer itself)
            return 4, self.__chosenPID
        if inp == '3':                      # Give badge to poster
            return 6, self.__chosenPID
        if inp == '4':                      # Add tag to this post
            return 7, self.__chosenPID
        if inp == '5':                      # Edit this post
            return 8, self.__chosenPID
        if inp == '6':                      # Mark as accepted
            return 9, self.__chosenPID

    # Accepting string answer, order a SQL query update
    def answerQuestion(self):
        uid = self.__user.getUid()
        print("\n\n________________________Make Answer________________________")
        title = input("What is your title? ")
        body = input("What do you want to answer? ")
        date = self.__sever.getCurrentTime()
        pid = self.__sever.requestNewPID()
        qid = self.__chosenPID
        sql = ("INSERT INTO POSTS (pid, pdate, title, body, poster) " +
               f"VALUES ('{pid}',DATE('{date}'),'{title}','{body}','{uid}');")
        self.__sever.requestQuery(sql, retriever=False, internal_call=True, debug_mode=True)
        sql = ("INSERT INTO ANSWERS (pid, qid) " +
               f"VALUES ('{pid}','{qid}');")
        self.__sever.requestQuery(sql, retriever=False, internal_call=True, debug_mode=True)
        print("Successfully answered post " + str(qid))
        return 3, qid

    # Order an sql string to update vote according to pid
    def vote(self):
        uid = self.__user.getUid()
        date = self.__sever.getCurrentTime()
        pid = self.__chosenPID

        acceptable = ['y', 'n', 'quit']
        print("\n\n________________________Make Vote________________________")
        vote = input("Do you want to vote the post? y/n ")
        while vote in acceptable:
            if vote == 'y':
                break
            if vote == 'n':
                return 3, pid
            if vote == 'quit':
                exit()
            else:
                key = input("Wrong input, Do you want to vote the post? y/n ")

        if self.__sever.requestVoteCheck(uid, pid):
            print("You already vote this post!")
            return 3, pid
        vno = self.__sever.requestNewVno()
        sql = ("INSERT INTO votes (pid, vno, vdate, uid) " +
               f"VALUES ('{pid}','{vno}', DATE('{date}'), '{uid}');")
        self.__sever.requestQuery(sql, retriever=False, debug_mode=True)
        return 3, pid

    # Mark as accepted. A privileged user can mark an answer post as accepted
    # Order a SQL query here
    # def MMA(self):


if __name__ == '__main__':
    Menu.MainMenu()
    server = Database('../Backend/myDB.db')
