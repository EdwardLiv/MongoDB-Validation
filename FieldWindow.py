from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from Mongo import Mongo


class FieldWindow(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.bind("<<ShowFrame>>", self.onShowFrame)
        mongo = Mongo()

        def selectedDocument(event):
            Mongo.setDocument(mongo, self.comboboxDocument.current())
            fields = Mongo.getFields(mongo)
            self.comboboxField.config(values=fields)
            self.comboboxField.current(0)

        def nextFrame(field):
            Mongo.setField(mongo, field)
            dataType = Mongo.getFieldDataType(mongo)
            if dataType == 'string':
                self.controller.showFrame("StringLengthWindow")
            elif dataType == 'int' or dataType == 'double' or dataType == 'long' or dataType == 'decimal':
                self.controller.showFrame("NumberIntervalWindow")
            else:
                messagebox.showerror("Error", "Selected field must be a number or string data type")

        labelDocument = Label(self, text="Select document:")
        labelDocument.grid(row=0, column=0, padx=5, pady=5, sticky="W")

        self.comboboxDocument = Combobox(self, state="readonly")
        self.comboboxDocument.bind("<<ComboboxSelected>>", selectedDocument)
        self.comboboxDocument.grid(row=0, column=1, padx=5, pady=5)

        labelField = Label(self, text="Select field:")
        labelField.grid(row=1, column=0, padx=5, pady=5, sticky="W")

        self.comboboxField = Combobox(self, state="readonly")
        self.comboboxField.grid(row=1, column=1, padx=5, pady=5)

        buttonBack = Button(self, text="Back", command=lambda: controller.showFrame("StartWindow"))
        buttonBack.grid(row=2, column=0, padx=5, pady=5, sticky="W")

        buttonConfirm = Button(self, text="Confirm", command=lambda: nextFrame(self.comboboxField.get()))
        buttonConfirm.grid(row=2, column=1, padx=5, pady=5, sticky="E")

    def onShowFrame(self, event):
        try:
            mongo = Mongo()

            documentsID = Mongo.getDocumentsID(mongo)
            self.comboboxDocument.config(values=documentsID)
            self.comboboxDocument.current(0)
            Mongo.setDocument(mongo, self.comboboxDocument.current())

            fields = Mongo.getFields(mongo)
            self.comboboxField.config(values=fields)
            self.comboboxField.current(0)
            Mongo.setField(mongo, self.comboboxField.get())

        except IndexError:
            messagebox.showerror("Error", "Collection has no data")
            self.controller.showFrame("StartWindow")

        except:
            messagebox.showerror("Error", "Unexpected error")
