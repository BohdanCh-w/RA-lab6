import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from back import DataRetriever as dr
from back import CriteriaGraphic, GraphType


class CriteraGraph(tk.Frame):
    def __init__(self, parent, criteria_manager):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#ffffff")
        self.graphics = CriteriaGraphic(criteria_manager)
        self.graph_frame = None

        self.create_components()
        self.draw_components()

    def create_components(self):
        self.header = tk.Label(self, bg='#ffffff',
                               text=dr.ui()['graph']['header'],
                               font=Font(size=20))
        str_var = tk.StringVar(self)
        str_var.set('Виберіть графік')
        self.dd_category = tk.OptionMenu(self, str_var, *dr.ui('graph')['categories'],
                                         command=self.type_selected)
        self.b_build = tk.Button(self, text=dr.ui('graph')['build'],
                                 command=self.build_graph)

    def draw_components(self):
        self.header.grid(row=0, column=0, sticky=tk.W)
        self.dd_category.grid(row=0, column=1, sticky=tk.W)
        self.b_build.grid(row=0, column=2, sticky=tk.W, padx=10, pady=5)

    def type_selected(self, type):
        for i, name in enumerate(dr.ui('graph')['categories']):
            if type == name:
                self.type = GraphType(i)

    def build_graph(self):
        self.graph_frame = tk.Frame(self, bg='#ffffff')
        self.graph_frame.grid(row=1, column=0, columnspan=3, sticky='ns')
        self.canvas = FigureCanvasTkAgg(self.graphics.get_figure(6, 6, self.type),
                                        master=self.graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(sticky="nsew")
