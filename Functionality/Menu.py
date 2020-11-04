from Functionality.FunctionalityInterace import *
from Functionality.PrivilegedInterface import *
from Functionality.Pages import Pages
from Object.User import *
from InputControl.RegInput import *


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
            return self.postActionMenu()
        elif self.__state == 4:
            return self.answerQuestion()
        elif self.__state == 5:
            return self.vote()
        elif self.__state == 6:
            return self.giveBadge()
        elif self.__state == 7:
            return self.addTags()
        elif self.__state == 8:
            return self.editPostContent()
        elif self.__state == 9:
            return self.MMA()

    # After login successfully, user will be in the navigation panel. Display all
    # options the user has.
    def MainMenu(self):
        acceptable_value = ['1', '2']
        print("\n\n________________________Main menu________________________")
        print("Input the corresponding number to navigate to that option")
        print("Type 'back' anytime you want to return to Main Menu")
        print("1. Post Question")
        print("2. Search Post  ")
        inp = InputControl.Input("Please type in the number correspond to the option you choose: ")
        while inp not in acceptable_value:
            inp = InputControl.Input("Unrecognized input. Please type in the number correspond to the option you choose: ")

        if inp == '1':
            return 1, None
        if inp == '2':
            return 2, None

    # Accept string as input, return SQL string statement update. Assume that UID
    # will be provided. It must implement a hash function to create a pid
    def postQuestion(self):
        uid = self.__user.getUid()
        acceptable_value = ['y', 'n']
        print("\n\n________________________Make Post________________________")
        print("What is your title? (Hit enter when you finish)")
        title = InputControl.Input()
        print("What do you want in your post? (Hit enter when you finish)")
        body = InputControl.Input()
        confirm = InputControl.Input("Do you confirm your new post? y/n")
        while confirm not in acceptable_value:
            confirm = InputControl.Input("Unrecognized input. Do you confirm your new post? y/n ")
        if confirm == 'n':
            return 0, None
        date = self.__sever.getCurrentTime()
        pid = self.__sever.requestNewPID()
        sql = ("INSERT INTO POSTS (pid, pdate, title, body, poster) " +
               f"VALUES ('{pid}',DATE('{date}'),'{title}','{body}','{uid}');")

        update_question_sql = ("INSERT INTO QUESTIONS (pid) " +
                               f"VALUES ('{pid}');")

        self.__sever.requestQuery(sql, retriever=False, debug_mode=True)
        self.__sever.requestQuery(update_question_sql, retriever=False, debug_mode=True)
        print("Post Success!")
        return 0, None

    # Accepting keyword, order SQL query
    def searchPost(self):
        print("\n\n_______________________Search Post________________________")
        keyword = input("Search Keyword, use ',' to search multiple: ").split(",")

        # prepare keyword clause
        keyword_sql_title = self.where_clause_preparation("P.title", keyword)
        keyword_sql_body = self.where_clause_preparation("P.body", keyword)
        keyword_sql_tag = self.where_clause_preparation("T.tag", keyword)

        sql = ("SELECT P.*, COUNT(V.vno) FROM posts P LEFT JOIN votes V ON P.pid = V.pid " +
               keyword_sql_title +
               "GROUP BY P.pid, P.pdate, P.title, P.body, P.poster " +
               "UNION " +
               "SELECT P.*, COUNT(V.vno) FROM posts P LEFT JOIN votes V ON P.pid = V.pid " +
               keyword_sql_body +
               "GROUP BY P.pid, P.pdate, P.title, P.body, P.poster " +
               "UNION " +
               "SELECT Z.*, COUNT(V.vno) FROM ( " +
               "    SELECT DISTINCT P.* " +
	           "    FROM posts P " +
               "    JOIN tags T ON P.pid = T.pid " +
                    keyword_sql_tag +
               ") Z LEFT JOIN votes V ON Z.pid = V.pid " +
               "GROUP BY Z.pid, Z.pdate, Z.title, Z.body, Z.poster;")

        column_array = ['pid', 'type', 'post date', 'title', 'content', 'poster', 'votes']
        records = self.__sever.requestQuery(sql, retriever=True, col_name=column_array, internal_call=True,
                                            fetch_many=True, debug_mode=True)

        available_pid = []
        for page in records:
            for line in page:
                available_pid.append(line[0])

        new_record = []
        for page in records:
            tmp = []
            for line in page:
                tmp_line = list(line)

                # If it's an answer attach "A
                if self.__sever.checkIfAnswer(tmp_line[0]):
                    tmp_line.insert(1, "A")
                else:
                    tmp_line.insert(1, "Q")

                tmp.append(list(tmp_line))
            new_record.append(tmp)

        records = new_record
        print(records)

        # This section display them page by page
        bookkeeper = Pages(records, 0, col_name=column_array)
        bookkeeper.printPages()
        tmp_bool = False
        search_pid = list()
        while len(search_pid) == 0:
            if tmp_bool: print("Invalid PID, ", end="")
            tmp_bool = False
            pid = InputControl.Input("Please choose the post by type in the PID to interact with it, or 'back' " +
                        "to return to main menu: ")

            if pid == 'back':
                return 0, None
            elif pid == 'prev':
                bookkeeper.prevPage()
                continue
            elif pid == 'next':
                bookkeeper.nextPage()
                continue
            elif pid not in available_pid:
                tmp_bool = True
            else:
                sql1 = f"SELECT * FROM POSTS P WHERE P.PID = '{pid}';"
                search_pid = self.__sever.requestQuery(sql1, retriever=True, internal_call=True,
                                                       debug_mode=True)
                tmp_bool = True
        return 3, pid

    # Post-Action-Group

    # This window will be called if a user chose a post
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

        inp = InputControl.Input("Please type in the number correspond to the option you choose: ")
        while inp not in acceptable_value:
            inp = InputControl.Input("Unrecognized input. Please type in the number correspond to the option you choose: ")

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
        title = InputControl.Input("What is your title? ")
        body = InputControl.Input("What do you want to answer? ")
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
        vote = InputControl.Input("Do you want to vote the post? y/n ")
        while vote in acceptable:
            if vote == 'y':
                break
            if vote == 'n':
                return 3, pid
            if vote == 'quit':
                exit()
            else:
                key = InputControl.Input("Wrong input, Do you want to vote the post? y/n ")

        if self.__sever.requestVoteCheck(uid, pid):
            print("You already vote this post!")
            return 3, pid
        vno = self.__sever.requestNewVno()
        sql = ("INSERT INTO votes (pid, vno, vdate, uid) " +
               f"VALUES ('{pid}','{vno}', DATE('{date}'), '{uid}');")
        self.__sever.requestQuery(sql, retriever=False, debug_mode=True)
        print("Vote Successfully" + str(pid))
        return 3, pid

    # Mark as accepted. A privileged user can mark an answer post as accepted
    # Order a SQL query here
    def MMA(self):
        print("\n____________________Mark as Accepted_____________________")
        print("You have chosen post " + self.__chosenPID)

        get_question_sql = f"SELECT A.QID FROM ANSWERS A WHERE A.PID = '{self.__chosenPID}';"
        correspond_question = self.__sever.requestQuery(get_question_sql, internal_call=True, debug_mode=True)
        qid = str(correspond_question[0][0])

        check_AA = self.__sever.checkAA(qid)

        if check_AA:
            inp = InputControl.Input("THIS POST ALREADY HAVE AN ACCEPTED ANSWER. ARE YOU SURE YOU WANT TO CHANGE" +
                        "IT TO THIS ONE? y/n ")

        acceptable_answer = ['n', 'y']
        while inp not in acceptable_answer:
            inp = InputControl.Input("Unrecognized input. ARE YOU SURE YOU WANT TO CHANGE" +
                        "THE ACCEPTED ANSWER TO THIS ONE? y/n ")

        if inp == 'n':
            return 3, self.__chosenPID

        sql = f"UPDATE QUESTIONS SET THEAID = '{self.__chosenPID}' WHERE PID = '{qid}';"

        # Update the accepted answer
        self.__sever.requestQuery(sql, internal_call=True, debug_mode=True)

        print("\nTHE CHOSEN ANSWER IS MARKED AS ACCEPTED SUCCESSFULLY!")
        return 3, self.__chosenPID

    # Assign badge to the poster
    def giveBadge(self):
        # Get the poster
        get_poster_SQL = f"SELECT P.POSTER FROM POSTS P WHERE P.PID = '{self.__chosenPID}';"
        poster = self.__sever.requestQuery(get_poster_SQL, internal_call=True, debug_mode=True)
        poster = str(poster[0][0])

        post_date = self.__sever.getCurrentTime()
        received_post = self.__sever.checkBadgeGranted(poster, post_date)

        if received_post:
            inp = InputControl.Input("\nSORRY, THIS POSTER HAS ALREADY RECEIVED A BADGE TODAY. TRY AGAIN TOMORROW."
                        "\nHit Enter to return to the previous menu.")

            return 3, self.__chosenPID
        column_array = ['BADGES NAME', 'TYPE']
        badge_record = self.__sever.requestQuery("SELECT * FROM BADGES B;",col_name=column_array, internal_call=False, debug_mode=True)
        badge_list = []

        for row in badge_record:
            badge_list.append(row[0])

        inp = InputControl.Input("\nPlease select a badge name in this list to grant user the badge " +
                    "or 'back' to return to previous menu': ")

        bool_flag = True
        while inp not in badge_list:
            if inp == 'back':
                return 3, self.__chosenPID
            inp = InputControl.Input("Invalid badge name, please enter again")

        sql = f"INSERT INTO UBADGES(UID, BDATE, BNAME) VALUES ('{poster}', '{post_date}', '{inp}');"

        print(f"{poster} {post_date} {inp}")
        self.__sever.requestQuery(sql, internal_call=True, retriever=False, debug_mode=True)
        print("Successfully Give A Badge!")
        return 3, self.__chosenPID

    def addTags(self):
        print("\n______________________Add tag_______________________")
        inp = InputControl.Input("Choose a keyword as a tag to add to this post: ")

        sql = f"INSERT INTO TAGS(PID, TAG) VALUES ('{self.__chosenPID}', '{inp}')"
        self.__sever.requestQuery(sql, retriever=False, internal_call=True, debug_mode=True)

        return 3, self.__chosenPID

    # update the chosen post by changing the body and/or title of the post
    def editPostContent(self):
        uid = self.__user.getUid()
        pid = self.__chosenPID
        acceptable_value = ['1', '2', 'back']
        print("\n\n________________________Edit Post________________________")
        post = self.__sever.getPost(pid)
        print("Title: " + post[0][0])
        print("Body: " + post[0][1])
        print("Type 'back' anytime you want to return to Main Menu")
        print("1. Edit Title")
        print("2. Edit Body")
        inp = InputControl.Input("Please type in the number correspond to the option you choose: ")
        while inp not in acceptable_value:
            inp = InputControl.Input("Unrecognized input. Please type in the number correspond to the option you choose: ")
        if inp == 'back':
            return 3, pid
        elif inp == '1':  # edit title
            print("What is your new title of the post?")
            title = InputControl.Input("")
            update_title_sql = f"UPDATE POSTS SET TITLE = '{title}' WHERE PID = '{pid}';"
            self.__sever.requestQuery(update_title_sql, retriever=False, debug_mode=True)
        elif inp == '2':  # edit body
            print("What is your new body of the post?")
            body = InputControl.Input("")
            update_body_sql = f"UPDATE POSTS SET BODY = '{body}' WHERE PID = '{pid}';"
            self.__sever.requestQuery(update_body_sql, retriever=False, debug_mode=True)
        return 3, pid

    # This function is for internal calls only, it prepare where clause condition for queries
    def where_clause_preparation(self, subject, keyword_list):
        keyword_sql = []
        for kw in keyword_list:
            keyword_sql.append(f" lower({subject}) LIKE lower('%{kw}%') ")

        keyword_sql = " OR ".join(keyword_sql)
        keyword_sql = "WHERE" + keyword_sql
        return keyword_sql


if __name__ == '__main__':
    server = Database('../Backend/myDB.db')
    dummy = User('u500', 'D', 'abc', 'Edmonton', '2020-08-08')
    window = Menu(server, dummy, 7, 'p700')
    # window.menuNavigate()
    print(window.where_clause_preparation("P.title", ['data', 'base']))


    # f"lower(P.title) LIKE lower('%{kw}%') "
