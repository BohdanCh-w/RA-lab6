import tkinter as tk
from tkinter import ttk
from tkinter.font import Font

from back import DataRetriever as dr
from .__counter import Counter


class ExpertRatings(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#ffffff")
        self.create_components()
        self.draw_components()

    def create_components(self):
        self.header = tk.Label(self, bg='#ffffff',
                               text=dr.ui()['experts']['header'],
                               font=Font(size=20))
        self.table = ttk.Treeview(self, height=25)
        self.create_table()

    def draw_components(self):
        self.header.grid(row=0)
        self.table.grid(row=1, sticky=tk.W, pady=20, padx=5)

    def create_table(self):
        tb = self.table
        cols = ('id', 'name', 'exp_type', *(f'exp{i+1}' for i in range(15)),
                'avrg', 'res')
        tb['columns'] = cols
        for col in cols:
            tb.column(col, anchor=tk.CENTER, width=45)
        tb.column('#0', width=0)
        tb.column('id', width=20)
        tb.column('name', anchor=tk.W, width=360)
        tb.column('exp_type', anchor=tk.W, width=90)
        tb.column('avrg', width=125)
        tb.column('res', width=115)

        tb.heading('id', text=dr.ui()['experts']['table']['id'])
        tb.heading('name', text=dr.ui()['experts']['table']['name'])
        tb.heading('exp_type', text=dr.ui()['experts']['table']['exp_type'])
        tb.heading('avrg', text=dr.ui()['experts']['table']['avrg'])
        tb.heading('res', text=dr.ui()['experts']['table']['res'])
        for i in range(15):
            tb.heading(f'exp{i+1}', text=dr.ui()
                       ['experts']['table']['exp'].format(i+1))

    def clear_table(self):
        self.rc = Counter()
        self.table.delete(*self.table.get_children())

    def add_criteria(self, criteria):
        tb = self.table
        tb.insert(parent='', index=tk.END, iid=criteria.id*100, text='',
                  values=(criteria.id, criteria.name, '',
                          *['' for i in range(15)], '----',
                          f'{criteria.avrg: 4.2f}'))

        for i, (key, val) in enumerate(criteria.ratings.items(), 1):
            tb.insert(parent='', index=tk.END, iid=criteria.id*100+i, text='',
                      values=('', '', key.title(), *val,
                              f'{criteria.aprox[key]:4.2f}'))

        tb.insert(parent='', index=tk.END, iid=criteria.id*100+10, text='',
                  values=['-'*100 for i in range(len(tb['columns']))])
