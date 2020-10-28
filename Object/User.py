import datetime
class User:
    __uid = 0
    __usrname = ""
    __pwd = 0
    __city = ""
    __crdate = ""

    def __int__(self, uid, name, pwd, city):
        self.__uid = uid
        self.__usrname = name
        self.__pwd = pwd
        self.__city = city
        self.__crdate = datetime.datetime.now()

    @staticmethod
    def generateNewID():
        pass

    def getName(self, name):
        return self.__usrname

    def getUid(self):
        return self.__uid

    def getPwd(self):
        return self.__pwd

    def getCrdate(self):
        return self.__crdate

    @staticmethod
    def login(uid, pwd):
        return # return user object

    def __str__(self):
        return 'Person ' + self.__uid + ' '+ self.__usrname + ', ' + self.__city + ', ' + self.__crdate




