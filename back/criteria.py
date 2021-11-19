from .__void import Void


class Criteria:
    def __init__(self, id=0, name='', ratings=None):
        self.id = id
        self.name = name
        self.rate = {}

        self.rate['industry'] = Void(**ratings['industry'])
        self.rate['usability'] = Void(**ratings['usability'])
        self.rate['programming'] = Void(**ratings['programming'])

        usrs = Void(**ratings['users'])
        avrg = sum(usrs.mark) / len(usrs.mark)
        self.rate['users'] = Void(weight=usrs.weight, mark=avrg)

        lst = [i.weight for i in self.rate.values()]
        self.rate['avrg_w'] = sum(lst) / 4

    def __str__(self):
        return f'{self.id:2}: {self.name}'
