import tkinter as tk
from tkinter import ttk
from scripts.frontend import frame_settings_pdf

fonts = {'LARGE_FONT': "Verdana 12",
         'NORM_FONT': "Verdana 10",
         'SMALL_FONT': "Verdana 8",
         'HEADING_FONT': "Verdana 24",
         'SUBHEADING_FONT': "Verdana 16 underline"}

ERROR_404 = "Error 404 : Page not found !"
# 1080p opt
_HEIGHT = 320
_WIDTH = 1080

SIDEBAR_COLORS = ['#102E4A', 'white', '#55C1FF']


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        self.prop = {}

        # make window
        tk.Tk.__init__(self, *args, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.geometry(f"{_WIDTH}x{_HEIGHT}")
        self.wm_minsize(width=_WIDTH, height=_HEIGHT)
        self.wm_maxsize(width=_WIDTH, height=_HEIGHT)
        self.size_factors = {
            "sidebar": [0.25, 1],
            "container": [0.75, 0.9],
            "footer": [1, 0.25]
        }
        self.title("FillPDF")

        # initialize fonts
        self.fonts = fonts

        # make sidebar(controller) frame
        self.frame_sidebar = tk.Frame(self, background=SIDEBAR_COLORS[0],
                                      width=int(_WIDTH * self.size_factors["sidebar"][0]),
                                      height=int(_HEIGHT * self.size_factors["sidebar"][1]),
                                      pady=10
                                      )  # , padx=10)
        self.frame_sidebar.grid(column=0, row=0, rowspan=10, sticky="NW")

        self.frame_sidebar.buttons = {}
        self.frame_sidebar.buttons['empty'] = tk.Label(self.frame_sidebar)
        self.frame_sidebar.buttons['empty'].grid(column=0, row=0, pady=_HEIGHT/15-1, sticky="w")

        self.frame_sidebar.buttons["Settings"] = tk.Button(self.frame_sidebar,
                                                           text="Settings",
                                                           font=self.fonts["LARGE_FONT"],
                                                           anchor="w",
                                                           padx=100,
                                                           command=lambda: self.show_page("Settings"),
                                                           width=int(_WIDTH * self.size_factors["sidebar"][0]),
                                                           height=3,
                                                           bg=SIDEBAR_COLORS[0],
                                                           fg=SIDEBAR_COLORS[1],
                                                           activebackground=SIDEBAR_COLORS[2],
                                                           activeforeground=SIDEBAR_COLORS[0]
                                                           )

        self.frame_sidebar.buttons["Settings"].grid(column=0, row=3, ipady=0, sticky="w")

        self.frame_sidebar.buttons['empty2'] = tk.Label(self.frame_sidebar)
        self.frame_sidebar.buttons['empty2'].grid(column=0, row=2, pady=_HEIGHT/15, sticky="w")

        self.frame_sidebar.buttons["PdfAutoFill"] = tk.Button(self.frame_sidebar,
                                                              text="Fill PDFs",
                                                              font=self.fonts["LARGE_FONT"],
                                                              anchor="w",
                                                              padx=100,
                                                              command=lambda: self.show_page("PdfAutoFill"),
                                                              width=int(_WIDTH * self.size_factors["sidebar"][0]),
                                                              height=3,
                                                              bg=SIDEBAR_COLORS[0],
                                                              fg=SIDEBAR_COLORS[1],
                                                              activebackground=SIDEBAR_COLORS[2],
                                                              activeforeground=SIDEBAR_COLORS[0]
                                                              )
        self.frame_sidebar.buttons["PdfAutoFill"].grid(column=0, row=1, pady=0)

        self.frame_sidebar.grid_propagate(0)

        # make body frame
        container = tk.Frame(self,
                             width=int(_WIDTH * 0.75),
                             height=int(_HEIGHT * 0.9)
                             )
        for i in range(10):
            container.grid_rowconfigure(i, weight=1)
            container.grid_columnconfigure(i, weight=1)
        container.fonts = self.fonts
        container.grid(column=1, row=0, columnspan=10, sticky="w")

        # list of Pages
        self.frames = {}
        self.frames[frame_settings_pdf.Settings] = frame_settings_pdf.Settings(container, self)
        self.frames[frame_settings_pdf.PdfAutoFill] = frame_settings_pdf.PdfAutoFill(
            container,
            self,
            self.frames[frame_settings_pdf.Settings]
        )
        self.show_page("Settings")

    def show_page(self, page_name):
        """
            let us use the NAME of the class to display(the function show_frame
            use directly the class).
            when we use the class name, we can put our classes in different
            files
        """
        for b in self.frame_sidebar.buttons:
            self.frame_sidebar.buttons[b].config(bg=SIDEBAR_COLORS[0], fg=SIDEBAR_COLORS[1])

        if self.frame_sidebar.buttons[page_name.split('.')[-1]]:
            self.frame_sidebar.buttons[page_name.split('.')[-1]].config(bg=SIDEBAR_COLORS[2], fg=SIDEBAR_COLORS[0])

        for F in self.frames:
            if F.__name__ == page_name:
                self.show_frame(F)
                return
        print(ERROR_404)

    def show_frame(self, cont):
        """raise to the front the frame we want

            :param cont: the frame
        """
        frame = self.frames[cont]
        frame.grid(column=1, row=0, sticky="nsew", columnspan=10)
        frame.tkraise()
        # frame.grid_propagate(0)


class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


if __name__ == "__main__":
    App = App()
    App.mainloop()
