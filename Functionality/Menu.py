import Functionality.FunctionalityInterace
class Menu():
    # Accept string as input, return SQL string statement update. Assume that UID
    # will be provided. It must implement a hash function to create a pid
    @staticmethod
    def postQuestion(uid):
        title = input("What is your title?")
        body = input("What do you want to post?")
        sql = "insert into posts(pid, pdate, title, body, poster) values ('100','2020-10-22','" + title +"' ,'"+body+ "' ,'" + str(uid) + "');"
        return sql


if __name__ == '__main__':
    print(Menu.postQuestion(200))
