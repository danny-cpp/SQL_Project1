from Functionality.FunctionalityInterace import *
from Object.User import *


class Menu(FunctionalityInterface):

    # As we build a finite state machine here, each number will be each state of this machine.
    # For this particular case: 0 = Main Menu, 1 = Post Question, 2 = Post Question, 3 = Search Post
    # It also needs to operate on a server and a user object
    def __init__(self, svr, usr, state):
        self.__sever = svr
        self.__user = usr
        self.__state = state

        # if state == 0:
        #     Menu.menuNavigate()
        if state == 1:
            self.postQuestion()
        elif state == 2:
            self.searchPost()

    # After login successfully, user will be in the navigation panel. Display all
    # options the user has.
    @staticmethod
    def menuNavigate():
        acceptable_value = ['1', '2']
        print("\n\n________________________Main menu________________________")
        print("Input the corresponding number to navigate to that option")
        print("Type 'back' anytime you want to return to Main Menu______")
        print("1. Post Question")
        print("2. Search Post  ")
        inp = input("Please type in the number correspond to the option you choose: ")
        while inp not in acceptable_value:
            inp = input("Unrecognized input. Please type in the number correspond to the option you choose: ")

        if inp == '1':
            return 1
        if inp == '2':
            return 2

    # Accept string as input, return SQL string statement update. Assume that UID
    # will be provided. It must implement a hash function to create a pid
    def postQuestion(self):
        uid = self.__user.getUid()
        title = input("What is your title? ")
        body = input("What do you want to post? ")
        date = self.__sever.getCurrentTime()
        pid = self.__sever.requestNewPID()
        sql = ("INSERT INTO POSTS (pid, pdate, title, body, poster) " +
               f"VALUES ('{pid}','{date}','{title}','{body}','{uid}');")
        print(sql)
        return 0

    # Accepting keyword, order SQL query
    def searchPost(self):
        keyword = input("Search Keyword: ")
        sql = "selet * from posts where title like '%" + keyword+"%';"
        return 0

    # Allows the user to choose the post by asking the pid
    @staticmethod
    def choosePost():
        keyword = input("Search pid: ")
        sql = "selet * from posts where pid = " + keyword + ";"
        return 0

    # Post-Action-Group

    # Accepting string answer, order a SQL query update
    @staticmethod
    def answerQuestion(pid):
        answer = input("Please enter your answer: ")
        sql = "update posts set body = " + answer +" where pid = " + pid + ";"
        return sql

    # Order an sql string to update vote according to pid
    @staticmethod
    def vote(pid,uid):
        vote = input("Do you want to vote the post? y/n")
        if vote == 'y':
            sql = "insert into votes(pid, vdate, uid) values (" + pid + ", " + datetime.datetime.now()+ ", "+uid+");"
        return sql


if __name__ == '__main__':
    Menu.menuNavigate()
