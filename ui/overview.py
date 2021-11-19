import tkinter as tk
from tkinter import ttk
from tkinter.font import Font

from back import DataRetriever as dr
from back import CriteriasManager
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
        self.table = ttk.Treeview(self, height=13, style="big.Treeview")
        self.create_table()

    def draw_components(self):
        self.header.grid(row=0)
        self.table.grid(row=1, sticky=tk.W, pady=20, padx=5)

    def create_table(self):
        tb = self.table
        cols = ('id', 'name', 'ind', 'usab', 'prog', 'user', 'avrg', 'avrg_x')
        tb['columns'] = cols
        for col in cols:
            tb.column(col, anchor=tk.CENTER, width=150)
        tb.column('#0', width=0)
        tb.column('id', width=30)
        tb.column('name', anchor=tk.W, width=450)

        for col in cols:
            tb.heading(col, text=dr.ui()['overview']['table'][col])

        style = ttk.Style()
        style.configure('big.Treeview',
                        font=Font(size=16),
                        rowheight=40,
                        )

    def write_table(self, cm):
        self.table.insert(parent='', index=tk.END, iid=0, text='',
                          values=('', dr.ui('overview')['qk'], *cm.exp_weight.values(),
                                  sum(cm.exp_weight.values())/len(cm.exp_weight)))
        for crt in cm.crts:
            self.add_criteria(crt)

        avrg = [round(i, 3) for i in cm.ratings.avrg.values()]
        avrg_w = [round(i, 3) for i in cm.ratings.avrg_w.values()]
        self.table.insert(parent='', index=tk.END, iid=98, text='',
                          values=('', dr.ui('overview')['avrg'],
                                  *avrg))
        self.table.insert(parent='', index=tk.END, iid=99, text='',
                          values=('', dr.ui('overview')['avrg_w'],
                                  *avrg_w))

    def clear_table(self):
        self.rc = Counter()
        self.table.delete(*self.table.get_children())

    def add_criteria(self, crt):
        vals = []
        for key in CriteriasManager.exp_weight.keys():
            val = crt.rate[key]
            vals.append(
                f'{val.weight} / {round(val.mark, 1)} / {round(val.val, 1)}')

        self.table.insert(parent='', index=tk.END, iid=crt.id, text='',
                          values=(crt.id, crt.name, *vals,
                                  f'{crt.rate["avrg"]:4.3f}',
                                  f'{crt.rate["avrg_x"]:4.3f}'))
