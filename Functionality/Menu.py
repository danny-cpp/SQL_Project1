<<<<<<< master
if __name__ == '__main__':
    print("hi")
=======
from Functionality.FunctionalityInterace import *
import Object.User
import datetime


class Menu(FunctionalityInterface):
    # After login successfully, user will be in the navigation panel. Display all
    # options the user has.
    @staticmethod
    def menuNavigate():
        print("________________________Main menu________________________")
        print("Input the corresponding number to navigate to that option")
        print("Type 'back' anytime you want to return to Main Menu______")
        print("1. Post Question")
        print("2. Search Post  ")
        print("3. Post Answer  ")
        print("4. Vote Post    ")

    # Accept string as input, return SQL string statement update. Assume that UID
    # will be provided. It must implement a hash function to create a pid
    @staticmethod
    def postQuestion(uid):
        title = input("What is your title?")
        body = input("What do you want to post?")
        sql = "insert into posts(pid, pdate, title, body, poster) values ('100','2020-10-22','" + title +"' ,'"+body+ "' ,'" + str(uid) + "');"
        return sql

    # Use all the value in the argument to create a a pid. Must be unique. Do
    # research on this
    @staticmethod
    def postHash(uid, postdate, post_content):
        pass

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
    Menu.menuNavigate()
>>>>>>> Revert "cm to be cherry-picked"
