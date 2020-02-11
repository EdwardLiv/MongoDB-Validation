from tkinter import *
from StartWindow import StartWindow
from FieldWindow import FieldWindow
from StringLengthWindow import StringLengthWindow
from NumberIntervalWindow import NumberIntervalWindow


class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)
        container.pack(fill="both", expand=True)
        self.frames = {}
        for f in (StartWindow, FieldWindow, StringLengthWindow, NumberIntervalWindow):
            pageName = f.__name__
            frame = f(parent=container, controller=self)
            self.frames[pageName] = frame
            frame.grid(row=0, column=0, sticky="NSEW")
        self.showFrame("StartWindow")

    def showFrame(self, pageName):
        frame = self.frames[pageName]
        frame.event_generate("<<ShowFrame>>")
        frame.tkraise()


if __name__ == "__main__":
    app = App()
    app.title("MongoDB")
    app.mainloop()
