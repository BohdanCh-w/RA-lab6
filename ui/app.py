import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from tkinter.messagebox import showerror

from back import DataRetriever as dr
from back import CriteriasManager

from .overview import CriteraOverview
from .graph import CriteraGraph


class CriteriasApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry('1400x650')

        self.lang = 'uk'
        self.languages = ['uk', 'en']

        self.cm = CriteriasManager()
        self.cm.get_mock_data()
        self.cm.analise_and_count()

        self.create_components()
        self.draw_components()

    def create_components(self):
        self.sections = ttk.Notebook(self)
        self.tab1 = CriteraOverview(self)
        self.tab2 = tk.Frame(self)
        self.tab3 = CriteraGraph(self, self.cm)
        self.sections.add(self.tab1, text=dr.ui()['main'][0])
        self.sections.add(self.tab2, text=dr.ui()['main'][1])
        self.sections.add(self.tab3, text=dr.ui()['main'][2])
        self.sections.bind('<<NotebookTabChanged>>', self.on_tab_change)

        self.b_change_lang = tk.Button(self, text=dr.ui()['ch_lang'],
                                       font=Font(size=8), command=self.change_lang)

    def draw_components(self):
        self.sections.pack(expand=True, fill=tk.BOTH)
        self.b_change_lang.place(relx=0.93, rely=0,
                                 relwidth=0.07, relheight=0.03)

    def on_tab_change(self, event):
        tab = event.widget.tab('current')['text']
        if tab == dr.ui()['main'][0]:
            self.update_overview_tab()
        elif tab == dr.ui()['main'][2]:
            self.update_graph_tab()

    def update_overview_tab(self):
        self.tab1.clear_table()
        self.tab1.write_table(self.cm)

    def change_lang(self):
        self.lang = self.languages[
            (self.languages.index(self.lang) + 1) % len(self.languages)]
        dr.set_ui_lang(f'data\\ui_{self.lang}.json')
        self.sections.pack_forget()
        self.b_change_lang.place_forget()
        self.create_components()
        self.draw_components()

    def update_graph_tab(self):
        pass

    def report_callback_exception(self, exc, val, tb):
        showerror("Error", message=str(val))
