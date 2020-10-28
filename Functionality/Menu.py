from Functionality.FunctionalityInterace import *
from Object.User import *
from Backend.Database import *
import datetime


class Menu(FunctionalityInterface):

    def __init__(self, uid):
        self.uid = uid

    # After login successfully, user will be in the navigation panel. Display all
    # options the user has.
    @staticmethod
    def menuNavigate(uid):
        accepted_input = ['1', '2']
        print("________________________Main menu________________________")
        print("Input the corresponding number to navigate to that option")
        print("Type 'back' anytime you want to return to Main Menu______")
        print("1. Post Question")
        print("2. Search Post  ")
        inp = input("Please type in the number correspond to the option: ")
        while inp not in accepted_input:
            inp = input("Unrecognized input. Please type in the number correspond to the option: ")

        if inp == '1':
            Menu.postQuestion(uid)
        elif inp == '2':
            Menu.searchPost(uid)

    # Accept string as input, return SQL string statement update. Assume that UID
    # will be provided. It must implement a hash function to create a pid
    def postQuestion(self):
        title = input("What is your title? ")
        body = input("What do you want to post? ")
        pid = Database.requestNewPID()
        sql = "insert into posts(pid, pdate, title, body, poster) values (" + pid + ",'2020-10-22','" + title +" ," + body + " ," + str(self) + "');"
        Database.requestQuery(sql)
        return sql


    # Accepting keyword, order SQL query
    @staticmethod
    def searchPost(keyword):
        keyword = input("Search Keyword: ")
        sql = "selet * from posts where title like '%" + keyword+"%';"
        return sql

    # Allows the user to choose the post by asking the pid
    @staticmethod
    def choosePost():
        keyword = input("Search pid: ")
        sql = "selet * from posts where pid = " + keyword + ";"
        return sql

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
    while True:
        Menu.menuNavigate('u200')