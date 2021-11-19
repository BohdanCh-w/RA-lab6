import tkinter as tk
from tkinter import ttk
from tkinter.font import Font

from back import DataRetriever as dr
from .__counter import Counter


class CriteraOverview(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#ffffff")
        self.create_components()
        self.draw_components()

    def create_components(self):
        self.header = tk.Label(self, bg='#ffffff',
                               text=dr.ui()['overview']['header'],
                               font=Font(size=20))
        self.table = ttk.Treeview(self, height=10, style="big.Treeview")
        self.create_table()

    def draw_components(self):
        self.header.grid(row=0)
        self.table.grid(row=1, sticky=tk.W, pady=20, padx=5)

    def create_table(self):
        tb = self.table
        cols = ('id', 'name', 'ind', 'usab', 'prog', 'user', 'avrg')
        tb['columns'] = cols
        for col in cols:
            tb.column(col, anchor=tk.CENTER, width=150)
        tb.column('#0', width=0)
        tb.column('id', width=30)
        tb.column('name', anchor=tk.W, width=600)

        for col in cols:
            tb.heading(col, text=dr.ui()['overview']['table'][col])

        style = ttk.Style()
        style.configure('big.Treeview',
                        font=Font(size=20),
                        rowheight=50,
                        )

    def clear_table(self):
        self.rc = Counter()
        self.table.delete(*self.table.get_children())

    def add_criteria(self, criteria):
        vals = [round(i, 3) for i in criteria.aprox.values()]
        self.table.insert(parent='', index=tk.END, iid=criteria.id, text='',
                          values=(criteria.id, criteria.name, *vals,
                                  f'{criteria.avrg:4.3f}'))
