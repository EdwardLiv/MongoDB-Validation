from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from Mongo import Mongo


class StartWindow(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        mongo = Mongo()

        def selectedDatabase(event):
            Mongo.setDatabase(mongo, comboboxDatabase.get())
            collections = Mongo.getCollections(mongo)
            comboboxCollection.config(values=collections)
            comboboxCollection.current(0)

        def nextFrame():
            Mongo.setCollection(mongo, comboboxCollection.get())
            controller.showFrame("FieldWindow")

        labelDatabase = Label(self, text="Select database:")
        labelDatabase.grid(row=0, column=0, padx=5, pady=5, sticky="W")

        databases = Mongo.getDatabases(mongo)
        comboboxDatabase = Combobox(self, state="readonly", values=databases)
        if databases: comboboxDatabase.current(0)
        else: messagebox.showerror("Error", "Localhost has no databases")
        Mongo.setDatabase(mongo, comboboxDatabase.get())
        comboboxDatabase.bind("<<ComboboxSelected>>", selectedDatabase)
        comboboxDatabase.grid(row=0, column=1, padx=5, pady=5)

        labelCollection = Label(self, text="Select collection:")
        labelCollection.grid(row=1, column=0, padx=5, pady=5, sticky="W")

        collections = Mongo.getCollections(mongo)
        comboboxCollection = Combobox(self, state="readonly", values=collections)
        comboboxCollection.current(0)
        comboboxCollection.grid(row=1, column=1, padx=5, pady=5)

        buttonConfirm = Button(self, text="Confirm", command=lambda: nextFrame())
        buttonConfirm.grid(row=2, column=1, padx=5, pady=5, sticky="E")
