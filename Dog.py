class Dog:
    def __init__(self, name):
        self.__name = name

    def bark(self):
        print("woof")

    def getName(self):
        return self.__name


if __name__ == '__main__':
    Dog("rock")
    a = [1, 2, 3]
    print(a)
    a = a.append(4)
    test = "         hi      "
    print(test)
    test.strip()
    print(test)