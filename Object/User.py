import datetime
class User:
    __uid = 0
    __usrname = ""
    __pwd = 0
    __city = ""
    __crdate = ""

    def __int__(self,name,pwd,city):
        self.__usrname = name
        self.__pwd = pwd
        self.__city = city
        self.__crdate = datetime.datetime.now()

    def getName(self, name):
        return self.__usrname

    def getUid(self):
        return self.__uid

    def getPwd(self):
        return self.__pwd

    def getCrdate(self):
        return self.__crdate

    def login(self, name, pwd):
        # call db and search the user with name and pwd
        # select * from user where name = '' and pwd = ''
        pass

    def __str__(self):
        return 'Person ' + self.__uid + ' '+ self.__usrname + ', ' + self.__city + ', ' + self.__crdate




