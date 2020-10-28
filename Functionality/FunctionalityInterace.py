class FunctionalityInterface:
    # After login successfully, user will be in the navigation panel. Display all
    # options the user has.
    @staticmethod
    def menuNavigate():
        pass

    # Accept string as input, return SQL string statement update. Assume that UID
    # will be provided. It must implement a hash function to create a pid
    @staticmethod
    def postQuestion(uid):
        # Return string in sql "select * from user"
        pass

    # Use all the value in the argument to create a a pid. Must be unique. Do
    # research on this
    @staticmethod
    def postHash(uid, postdate, post_content):
        pass

    # Accepting keyword, order SQL query
    @staticmethod
    def searchPost(keyword):
        pass

    # Allows the user to choose the post by asking the pid
    @staticmethod
    def choosePost():
        pass

    # Post-Action-Group

    # Accepting string answer, order a SQL query update
    @staticmethod
    def answerQuestion(pid):
        pass

    # Order an sql string to update vote according to pid
    @staticmethod
    def vote(pid,uid):
        pass

if __name__ == '__main__':
    print("helloWorld")
