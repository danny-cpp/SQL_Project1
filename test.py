import Login.LoginInterface

class Login(Login.LoginScreen):
    def __init__(self, username, password):
        self.__username = username
        self.__password = password

        @staticmethod
        def postQuestion(uid):
            post  = input("what's the post?")
            sql = "select * from" + post
            # Return string in sql "select * from user"
            return





if __name__ == '__main__':
    new_user = Login.getUser()

