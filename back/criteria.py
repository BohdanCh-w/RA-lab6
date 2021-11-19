class Criteria:
    def __init__(self, id=0, name='', ratings=None, avrg=None):
        self.id = id
        self.name = name
        self.ratings = ratings
        self.avrg = avrg

    def __str__(self):
        return f'{self.id:2}: {self.name}'
