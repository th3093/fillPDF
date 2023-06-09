from tkinter import *
from scripts.frontend import frame_settings_pdf


class ControlFrame(Frame):
    def __init__(self, container):
        super().__init__(container)

        self.frame = Frame(container, width=1080, height=100, bg="#102E4A")
        self.frame.pack()
        self.frames = []

        #testing
        self.frames.append(frame_settings_pdf.Settings(self.frame))
        print(self.frames)
        self.settings_btn = Button(self.frame,
                                   text="Einstellungen",
                                   bg="grey",
                                   fg="black",
                                   command=self.change_frame
                                   )
        self.settings_btn.pack(side="left")

    def change_frame(self):
        frame = frame_settings_pdf.Settings(self.frame)
        print()
        #if self.frames[1]
        #frame.pack(side="left")
        frame.tkraise()
        #gui.Settings(frame)
        #self.frames.append(frame)


class TemplateFrame(Frame):
    def __init__(self, container):
        super().__init__(container)






root = Tk()
root.geometry("800x600")
ControlFrame(root)
root.mainloop()
