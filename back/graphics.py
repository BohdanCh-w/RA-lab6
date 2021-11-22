from enum import IntEnum
from math import sin, cos
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from back import DataRetriever as dr
from back.__void import Void


class GraphType(IntEnum):
    industry = 0
    usability = 1
    programming = 2
    users = 3
    avrg = 4
    combined = 5


def weight_space(start, end, weights):
    '''Return number spaced in interval with each interval weight'''
    length = sum(weights)
    cumulated_sum = 0
    step = (end-start) / length
    ret = [start]
    for i in weights[:-1]:
        cumulated_sum += i
        ret.append(start + cumulated_sum * step)
    return ret


class CriteriaGraphic:
    def __init__(self, manager):
        self.cm = manager
        self.data = None
        self.radar_factory(10)

    @staticmethod
    def radar_factory(num_vars, frame='circle'):
        theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)

        class RadarAxes(PolarAxes):
            name = 'radar'
            RESOLUTION = 1

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.set_theta_zero_location('N')

            def plot(self, *args, **kwargs):
                lines = super().plot(*args, **kwargs)
                for line in lines:
                    self._close_line(line)

            def _close_line(self, line):
                x, y = line.get_data()
                # FIXME: markers at x[0], y[0] get doubled-up
                if x[0] != x[-1]:
                    x = np.append(x, x[0])
                    y = np.append(y, y[0])
                    line.set_data(x, y)

            def set_varlabels(self, labels):
                self.set_thetagrids(np.degrees(theta), labels)

            def _gen_axes_patch(self):
                if frame == 'circle':
                    return Circle((0.5, 0.5), 0.5)
                elif frame == 'polygon':
                    return RegularPolygon((0.5, 0.5), num_vars,
                                          radius=.5, edgecolor="k")
                else:
                    raise ValueError("Unknown value for 'frame': %s" % frame)

        register_projection(RadarAxes)
        return theta

    def calc(self):
        self.data = {
            GraphType.industry: [],
            GraphType.usability: [],
            GraphType.programming: [],
            GraphType.users: [],
            GraphType.avrg: [],
            GraphType.combined: [],
        }
        key_gtype = {
            'industry': GraphType.industry,
            'usability': GraphType.usability,
            'programming': GraphType.programming,
            'users': GraphType.users,
            'avrg': GraphType.avrg
        }

        self.weights = dr.exp()['weights']
        self.initial_coef = {}
        for key in {'industry', 'usability', 'programming', 'users'}:
            self.initial_coef[key] = [i.rate[key].weight for i in self.cm.crts]
        self.initial_coef['avrg'] = [i.rate['avrg'] for i in self.cm.crts]

        self.circle_part = {}
        for key, values in self.initial_coef.items():
            val_sum = sum(values)
            self.circle_part[key] = [val / val_sum * 2*np.pi for val in values]

        self.cirle_part_temp = {}
        for key, values in self.circle_part.items():
            self.cirle_part_temp[key] = [-values[0] / 2]
            for i, val in enumerate(self.circle_part[key]):
                self.cirle_part_temp[key].append(
                    val + self.cirle_part_temp[key][i])

        self.radian = {}
        for key, val in self.cirle_part_temp.items():
            self.radian[key] = [(val[i]+val[i+1])/2 for i in range(len(val)-1)]

        self.xwq = {}
        for key in {'industry', 'usability', 'programming', 'users'}:
            self.xwq[key] = []
            for i in range(len(self.initial_coef[key])):
                self.xwq[key].append(
                    self.weights[key] * self.initial_coef[key][i]
                    * self.cm.crts[i].rate[key].mark
                )
        sum_koef = sum([self.weights[key] for key in self.xwq.keys()])
        arr = []
        for i in range(len(self.initial_coef['avrg'])):
            value = []
            for key in self.xwq.keys():
                value.append(
                    self.initial_coef[key][i] * self.cm.crts[i].rate[key].mark
                    * self.weights[key]
                )
            arr.append(sum(value)/sum_koef)
        self.xwq['avrg'] = arr

        self.abc = {}
        for key in self.xwq.keys():
            self.abc[key] = []
            for i in range(len(self.xwq[key])):
                x = self.xwq[key][i] * sin(self.radian[key][i])
                y = self.xwq[key][i] * cos(self.radian[key][i])
                self.abc[key].append(Void(a=x, b=y, c=(x**2+y**2)**0.5))
            self.abc[key].append(
                Void(a=self.abc[key][0].a,
                     b=self.abc[key][0].b,
                     c=self.abc[key][0].c)
            )

        for key, gtype in key_gtype.items():
            arr = []
            for i in range(len(self.abc[key])-1):
                arr.append(abs(
                    self.abc[key][i].a * self.abc[key][i+1].b -
                    self.abc[key][i].b * self.abc[key][i+1].a
                ))
            self.data[gtype].append(arr)

        self.data[GraphType.combined] = [
            self.data[GraphType.industry][0],
            self.data[GraphType.usability][0],
            self.data[GraphType.programming][0],
            self.data[GraphType.users][0]
        ]

        return self.data

    def get_figure(self, xlen, ylen, type):
        graph = self.data[type] if self.data is not None else self.calc()[type]

        fig, axs = plt.subplots(figsize=(xlen, ylen), dpi=100, nrows=1, ncols=1,
                                subplot_kw=dict(projection='radar'))
        colors = ['b', 'g', 'y', 'r']
        for data, color in zip(graph, colors):
            theta = weight_space(0, 2*np.pi, data)
            axs.plot(theta, data, color=color)
            axs.fill(theta, data, facecolor=color, alpha=0.25)

        fig.text(0.5, 0.965, dr.ui('graph')['categories'][int(type)],
                 horizontalalignment='center', color='black', weight='bold',
                 size='large')
        return fig
