class Counter:
    def __init__(self, start=0):
        self.__curr = start
        self.__gen = self.__generator()

    def next(self):
        return self.__gen.__next__()

    def curr(self):
        return self.__curr

    def __generator(self):
        while True:
            yield self.__curr
            self.__curr += 1
