#-*- coding: utf-8 -*-
# Python version 3.4
# The use of the ttk module is optional, you can use regular tkinter widgets

from tkinter import *
from tkinter import ttk


class Selector():
    def __init__(self, options_list):
        # Creating root of object
        self.root = Tk()
        self.root.title("Multiple Choice Listbox")
        self.root.geometry("+50+300")

        # Creating frame to displace the options
        frame = ttk.Frame(self.root, padding=(3, 3, 12, 12))
        frame.grid(column=0, row=0, sticky=(N, S, E, W))

        # Creating option list from python list recieved
        var = StringVar(value=options_list)
        self.lstbox = Listbox(frame, listvariable = var, selectmode=MULTIPLE, width=50, height=10)
        self.lstbox.grid(column=0, row=0, columnspan=2)

        btn = ttk.Button(frame, text="OK", command = self.select)
        btn.grid(column=1, row=1)
        self.root.mainloop()
    
    def select(self):
        reslist = list()
        seleccion = self.lstbox.curselection()
        self.selected_items = []
        for i in seleccion:
            entrada = self.lstbox.get(i)
            reslist.append(entrada)
        for val in reslist:
            self.selected_items.append(val)
        
        self.root.destroy()

    def get_select(self):
        return self.selected_items


mylist = ['one', 'two', 'three']
list_box = Selector(mylist)
chosen_options = list_box.get_select()
print(chosen_options)
