class Criteria:
    def __init__(self, id=0, name='', ratings=None, aprox=None):
        self.id = id
        self.name = name
        self.ratings = ratings
        self.aprox = aprox or {
            key: 0 for key in self.ratings.keys()
        }
        self.avrg = sum(self.aprox.values()) / 4

    def __str__(self):
        return f'{self.id:2}: {self.name}'
