class FunctionalityInterface:
    # This is the entry point of the FSM, it call correspond functions with required information
    def menuNavigate(self):
        pass

    # After login successfully, user will be in the navigation panel. Display all
    # options the user has.
    def MainMenu(self):
        pass

    # Accept string as input, return SQL string statement update. Assume that UID
    # will be provided. It must implement a hash function to create a pid
    def postQuestion(self):
        # Return string in sql "select * from user"
        pass

    # Accepting keyword, order SQL query
    def searchPost(self):
        pass

    # Post-Action-Group

    # Accepting string answer, order a SQL query update
    def answerQuestion(self):
        pass

    # Order an sql string to update vote according to pid
    def vote(self):
        pass


