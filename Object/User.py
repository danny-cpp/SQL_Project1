import datetime
from Backend.Database import *


class User:
    def __init__(self, uid, name, pwd, city, crdate):
        self.__uid = uid
        self.__usrname = name
        self.__pwd = pwd
        self.__city = city
        self.__crdate = crdate

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
        # We should check the existence of the user first

        return

    def __str__(self):
        return 'Person ' + self.__uid + ' '+ self.__usrname + ', ' + self.__city + ', ' + self.__crdate


if __name__ == '__main__':
    User('sdffs', 'fewf', 'fewswfg', 'fewfew')

