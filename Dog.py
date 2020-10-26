class Dog:
    def __init__(self, name):
        self.__name = name

    def bark(self):
        print("woof")

    def getName(self):
        return self.__name