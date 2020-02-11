from tkinter import *
from tkinter import messagebox
from Mongo import Mongo


class StringLengthWindow(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.bind("<<ShowFrame>>", self.onShowFrame)
        mongo = Mongo()

        labelMin = Label(self, text="Minimum length:")
        labelMin.grid(row=0, column=0, padx=5, pady=5, sticky="W")

        self.entryMin = Entry(self)
        self.entryMin.grid(row=0, column=1, padx=5, pady=5)

        labelMax = Label(self, text="Maximum length:")
        labelMax.grid(row=1, column=0, padx=5, pady=5, sticky="W")

        self.entryMax = Entry(self)
        self.entryMax.grid(row=1, column=1, padx=5, pady=5)

        buttonBack = Button(self, text="Back", command=lambda: controller.showFrame("FieldWindow"))
        buttonBack.grid(row=2, column=0, padx=5, pady=5, sticky="W")

        buttonConfirm = Button(self, text="Confirm", command=lambda: setStringLength())
        buttonConfirm.grid(row=2, column=1, padx=5, pady=5, sticky="E")

        def setStringLength():
            try:
                minBound = int(self.entryMin.get())
                maxBound = int(self.entryMax.get())

                minValue = Mongo.findStringMinLength(mongo)
                maxValue = Mongo.findStringMaxLength(mongo)

                if minBound < 0:
                    messagebox.showerror("Error", "Min must be a positive integer")
                elif maxBound < 1:
                    messagebox.showerror("Error", "Max must be a non-zero positive integer")
                elif minBound > maxBound:
                    messagebox.showerror("Error", "Min must be less than or equal to max")
                elif minBound > minValue:
                    messagebox.showerror("Error", "Min must be less than or equal to {} (shortest string found)".format(minValue))
                elif maxBound < maxValue:
                    messagebox.showerror("Error", "Max must be greater than or equal to {} (longest string found)".format(maxValue))
                else:
                    Mongo.setStringLength(mongo, minBound, maxBound)
                    messagebox.showinfo("Information", "String length constraint successfully added")

            except ValueError:
                messagebox.showerror("Error", "Min and max must be integers")

            except:
                messagebox.showerror("Error", "Unexpected error")

    def onShowFrame(self, event):
        mongo = Mongo()

        minLength = Mongo.findStringMinLength(mongo)
        self.entryMin.delete(0, END)
        self.entryMin.insert(0, minLength)

        maxLength = Mongo.findStringMaxLength(mongo)
        self.entryMax.delete(0, END)
        self.entryMax.insert(0, maxLength)
