from .criteria import Criteria


class CriteriasManager:
    def __init__(self, criterias=None):
        self.criterias = criterias or []

    def add_criteria(self, criteria):
        if hasattr(criteria, '__iter__'):
            self.criterias.extend(criteria)
        else:
            self.criterias.append(criteria)

    def analise_and_count(self):
        def avrg(x): return sum(x) / len(x)
        for crt in self.criterias:
            for key, value in crt.ratings.items():
                lst = [i * j / 10 for i, j in zip(value, self.experts[key])]
                crt.aprox[key] = avrg(lst)
            crt.avrg = avrg(crt.aprox.values())

    @classmethod
    def parse_criteria(cls, data):
        return Criteria(
            data['id'],
            data['name'],
            data['ratings']
        )
