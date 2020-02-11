from tkinter import *
from tkinter import messagebox
from Mongo import Mongo


class NumberIntervalWindow(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.bind("<<ShowFrame>>", self.onShowFrame)
        mongo = Mongo()

        labelMin = Label(self, text="Minimum value:")
        labelMin.grid(row=0, column=0, padx=5, pady=5, sticky="W")

        self.entryMin = Entry(self)
        self.entryMin.grid(row=0, column=1, padx=5, pady=5)

        labelMax = Label(self, text="Maximum value:")
        labelMax.grid(row=1, column=0, padx=5, pady=5, sticky="W")

        self.entryMax = Entry(self)
        self.entryMax.grid(row=1, column=1, padx=5, pady=5)

        buttonBack = Button(self, text="Back", command=lambda: controller.showFrame("FieldWindow"))
        buttonBack.grid(row=2, column=0, padx=5, pady=5, sticky="W")

        buttonConfirm = Button(self, text="Confirm", command=lambda: setNumberInterval())
        buttonConfirm.grid(row=2, column=1, padx=5, pady=5, sticky="E")

        def setNumberInterval():
            try:
                minBound = float(self.entryMin.get())
                maxBound = float(self.entryMax.get())

                minValue = Mongo.findMinValue(mongo)
                maxValue = Mongo.findMaxValue(mongo)

                if minBound > maxBound:
                    messagebox.showerror("Error", "Min must be less than or equal to max")
                elif minBound > minValue:
                    messagebox.showerror("Error", "Min must be less than or equal to {} (lowest value found)".format(minValue))
                elif maxBound < maxValue:
                    messagebox.showerror("Error", "Max must be greater than or equal to {} (biggest value found)".format(maxValue))
                else:
                    Mongo.setNumberInterval(mongo, minBound, maxBound)
                    messagebox.showinfo("Information", "Number interval constraint successfully added")

            except ValueError:
                messagebox.showerror("Error", "Min and max must be numbers")

            except:
                messagebox.showerror("Error", "Unexpected error")

    def onShowFrame(self, event):
        mongo = Mongo()

        minLength = Mongo.findMinValue(mongo)
        self.entryMin.delete(0, END)
        self.entryMin.insert(0, minLength)

        maxLength = Mongo.findMaxValue(mongo)
        self.entryMax.delete(0, END)
        self.entryMax.insert(0, maxLength)
