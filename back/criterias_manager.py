from .criteria import Criteria


class CriteriasManager:
    def __init__(self, criterias=None):
        self.criterias = criterias or []

    def add_criteria(self, criteria):
        if hasattr(criteria, '__iter__'):
            self.criterias.extend(criteria)
        else:
            self.criterias.append(criteria)

    @classmethod
    def parse_criteria(cls, data):
        return Criteria(
            data['id'],
            data['name'],
            data['ratings']
        )
