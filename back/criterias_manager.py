from .criteria import Criteria
from .__void import Void
from .data_ import DataRetriever as dr


class CriteriasManager:
    __exp_weight = {
        'industry': 0.7,
        'usability': 0.8,
        'programming': 0.9,
        'users': 0.5
    }

    def __init__(self, criterias=None):
        self.crts = criterias or []

    def add_criteria(self, criteria):
        if hasattr(criteria, '__iter__'):
            self.crts.extend(criteria)
        else:
            self.crts.append(criteria)

    def analise_and_count(self):
        def avrg(x): return sum(x) / len(x)
        for crt in self.crts:
            lst = []
            for key in self.__exp_weight.keys():
                crt.rate[key].val = crt.rate[key].mark * crt.rate[key].weight
                lst.append(crt.rate[key].val * self.__exp_weight[key])
            crt.rate['avrg'] = sum(lst) / sum(self.__exp_weight.values())
            crt.rate['avrg_x'] = crt.rate['avrg'] / crt.rate['avrg_w']

        self.weights_sum = {}
        for key in self.__exp_weight.keys():
            self.weights_sum[key] = sum(
                i.rate[key].weight for i in self.crts
            )

        self.ratings = Void()
        rt = self.ratings

        rt.avrg = {}
        for key in self.__exp_weight.keys():
            rt.avrg[key] = sum(
                [i.rate[key].val for i in self.crts]
            ) / self.weights_sum[key]
        rt.avrg['avrg'] = sum(
            [i.rate['avrg'] for i in self.crts]
        ) / sum(
            [i.rate['avrg_w'] for i in self.crts]
        )
        rt.avrg['avrg_x'] = sum(
            [i.rate['avrg_x'] for i in self.crts]
        ) / len(self.crts)

        rt.avrg_w = {}
        for key in ('industry', 'usability', 'programming', 'users'):
            rt.avrg_w[key] = self.__exp_weight[key] * rt.avrg[key]

        values = 0
        values_w = 0
        for key in self.__exp_weight.keys():
            values += rt.avrg[key]
            values_w += rt.avrg_w[key]
        rt.avrg_w['avrg'] = values / len(self.__exp_weight.keys())
        rt.avrg_w['avrg_x'] = values_w / sum(self.__exp_weight.values())

    def get_mock_data(self):
        crts = dr.crt()
        for crt in crts:
            self.add_criteria(Criteria(
                crt['id'],
                crt['name'],
                crt['ratings']
            ))
