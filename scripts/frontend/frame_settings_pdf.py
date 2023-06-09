from scripts.backend import main_back
from tkinter import ttk, filedialog
from tkinter import *
from threading import Thread


# Settings Frame
class Settings(Frame):
    def __init__(self, container, controller):
        super().__init__(container)

        # Heading Label
        self.heading = Label(self, text="Settings", anchor=N, font=container.fonts["HEADING_FONT"])
        self.heading.grid(row=0, column=0, padx=50, pady=5, ipady=0, ipadx=0, sticky="nw")

        # Vars for execution options
        self.del_tmp = BooleanVar()
        self.blank_filling = BooleanVar()
        self.div_page_flag = BooleanVar()
        self.grouping_flag = BooleanVar()

        # del_tmp label + checkbutton
        self.del_tmp_label = Label(self,
                                   text="Delete temporary files",
                                   font=container.fonts["LARGE_FONT"]
                                   )
        self.del_tmp_label.grid(row=1, column=1, sticky="w")
        self.del_tmp_checkbutton = ttk.Checkbutton(
            self,
            variable=self.del_tmp,
            onvalue=True,
            offvalue=False
        )
        self.del_tmp.set(True)
        self.del_tmp_checkbutton.grid(column=2, row=1, padx=10, sticky="w")

        # blank_filling label + checkbutton
        self.blank_filling_label = Label(self,
                                         text="Add blank pages as divider",
                                         font=container.fonts["LARGE_FONT"]
                                         )
        self.blank_filling_label.grid(column=1, row=2, sticky="w")
        ttk.Checkbutton(
            self,
            variable=self.blank_filling,
            onvalue=True,
            offvalue=False,
            command=self.set_blank_filling
        ).grid(column=2, row=2, padx=10, sticky="w")

        # blank filling additional input of pdf pages per printed page to calculate filling
        self.blank_filling_quotient_label_placehodler = Label(self, width=40, height=2)
        self.blank_filling_quotient_label_placehodler.grid(column=3, row=3)
        self.blank_filling_quotient_label = Label(self,
                                                  text="How many files per page",
                                                  fg="black",
                                                  font=container.fonts["NORM_FONT"]
                                                  )
        self.blank_filling_quotient_label.grid(row=3, column=1, padx=10, sticky="w")
        self.blank_filling_quotient_label.grid_remove()
        self.blank_filling_quotient_entry = Entry(self, width=4)
        self.blank_filling_quotient_entry.grid(row=3, column=2, padx=10, sticky="w")
        self.blank_filling_quotient_entry.insert(0, f"{1}")
        self.blank_filling_quotient_entry.grid_remove()

        # sort_by  label + entry
        self.sort_by_label = Label(self,
                                   text="Which columns to sort?",
                                   fg="black",
                                   font=container.fonts["LARGE_FONT"]
                                   )
        self.sort_by_label.grid(row=4, column=1, sticky="w")
        self.sort_by_entry = Entry(self, textvariable=StringVar())
        self.default_sort_by_entry = "Name, Age, ..."
        self.sort_by_entry.insert(0, self.default_sort_by_entry)
        self.sort_by_entry.grid(row=4, column=2, padx=10, sticky="w")

        # grouping_flag label + checkbutton
        self.grouping_label = Label(self,
                                    text="Group entries?",
                                    font=container.fonts["LARGE_FONT"]
                                    )
        self.grouping_label.grid(row=5, column=1, sticky="w")
        self.grouping_checkbutton = ttk.Checkbutton(
            self,
            variable=self.grouping_flag,
            onvalue=True,
            offvalue=False
        )
        self.grouping_checkbutton.grid(column=2, row=5, padx=10, sticky="w")

        # divider_page_flag label + checkbutton
        self.divider_page_label = Label(self,
                                        text="Insert titled divider pages?",
                                        font=container.fonts["LARGE_FONT"]
                                        )
        self.divider_page_label.grid(row=6, column=1, sticky="w")
        self.divider_page_checkbutton = ttk.Checkbutton(
            self,
            variable=self.div_page_flag,
            onvalue=True,
            offvalue=False
        )
        self.divider_page_checkbutton.grid(column=2, row=6, padx=10, sticky="w")

        self.properties = {}

    # show / hide blank_filling quotient label and entry
    def set_blank_filling(self):
        blank_filling = self.blank_filling.get()
        if blank_filling:
            self.blank_filling_quotient_label.grid()
            self.blank_filling_quotient_entry.grid()
        else:
            self.blank_filling_quotient_label.grid_remove()
            self.blank_filling_quotient_entry.grid_remove()

    # get all properties relevant to backend script execution
    def get_properties(self):
        if self.sort_by_entry.get() != self.default_sort_by_entry:
            sort_by = self.sort_by_entry.get()
        else:
            sort_by = ""

        self.properties = {
            "del_tmp": self.del_tmp.get(),
            "sort_by": sort_by,
            "blank_filling": self.blank_filling.get(),
            "filling_quotient": self.blank_filling_quotient_entry.get(),
            "div_page_flag": self.div_page_flag.get(),
            "grouping_flag": self.grouping_flag.get()
        }
        return self.properties

    # set all properties relevant to backend script execution
    def set_properties(self, del_tmp_, sort_by_, bf_, fq_, div_f_, gp_f_):
        self.del_tmp.set(del_tmp_)
        self.sort_by_entry = sort_by_
        self.blank_filling = bf_
        self.blank_filling_quotient_entry = fq_
        self.div_page_flag = div_f_
        self.grouping_flag = gp_f_


# PdfAutoFill Frame
class PdfAutoFill(Frame):
    def __init__(self, container, controller, settings_container):
        super().__init__(container)

        self.month_only = BooleanVar()
        self.settings_container = settings_container
        self.input_path = StringVar()
        self.output_path = StringVar()

        # Heading
        self.heading = Label(self,
                             text="FillForms PDF",
                             anchor=N,
                             font=container.fonts["HEADING_FONT"]
                             )
        self.heading.grid(row=0, column=0, padx=50, pady=5, ipady=0, ipadx=0, sticky="nw")

        # month label + entry
        self.month_input_label = Label(self,
                                       text="Month",
                                       font=container.fonts["LARGE_FONT"]
                                       )
        self.month_input_label.grid(row=1, column=0, sticky='e')
        self.month_input_entry = Entry(self)
        self.month_input_entry.grid(row=1, column=1, sticky='w')

        # month_only checkbutton
        self.month_only_checkbtn = Checkbutton(self,
                                               text="Total month (j/n)",
                                               font=container.fonts["NORM_FONT"],
                                               onvalue=True,
                                               offvalue=False,
                                               command=self.set_day_entries,
                                               variable=self.month_only
                                               )
        self.month_only_checkbtn.grid(row=2, column=1, pady=5, sticky='e')

        # startday label + entry
        self.startday_input_label = Label(self,
                                          text="Starting day",
                                          font=container.fonts["LARGE_FONT"]
                                          )
        self.startday_input_label.grid(row=3, column=0, sticky='e')

        self.startday_input_entry = Entry(self)
        self.startday_input_entry.grid(row=3, column=1, pady=10, sticky='w')

        # endday label + entry
        self.endday_input_label = Label(self,
                                        text="End day",
                                        font=container.fonts["LARGE_FONT"]
                                        )
        self.endday_input_label.grid(row=4, column=0, sticky='e')

        self.endday_input_entry = Entry(self)
        self.endday_input_entry.grid(row=4, column=1, padx=0, pady=10, sticky='w')

        # Input File label + button
        self.input_file_label = Label(self,
                                      text="",
                                      font=container.fonts["NORM_FONT"],
                                      width=35
                                      )
        self.input_file_label.grid(row=3, column=3, sticky="sew")
        self.input_file_button = Button(self,
                                        text="Input File",
                                        command=lambda: self.select_file('in'),
                                        width=14,
                                        height=2,
                                        font=container.fonts["LARGE_FONT"]
                                        )
        self.input_file_button.grid(row=1, column=3, padx=5, pady=0, sticky="nsew")

        # Output File label + button
        self.output_path_label = Label(self,
                                       text="",
                                       font=container.fonts["NORM_FONT"],
                                       width=35,
                                       height=2
                                       )
        self.output_path_label.grid(row=4, column=3, sticky="new")
        self.output_path_button = Button(self,
                                         text="Output directory",
                                         font=container.fonts["LARGE_FONT"],
                                         width=14,
                                         height=2,
                                         command=lambda: self.select_file('out')
                                         )
        self.output_path_button.grid(row=2, column=3, padx=0, pady=0, sticky="nsew")

        # start button
        self.start_button = Button(self,
                                   text="Start",
                                   font=container.fonts["LARGE_FONT"],
                                   command=self.start,
                                   width=15,
                                   height=2
                                   )
        self.start_button.grid(row=5, column=3, padx=60, pady=0, sticky='nsew')

        # initializing screen
        self.month_only.set(True)
        self.set_day_entries()

    # show / hide day entries
    def set_day_entries(self):
        entry_box = self.month_only.get()
        if entry_box:
            self.startday_input_entry.config(state="disabled")
            self.endday_input_entry.config(state="disabled")
        else:
            self.startday_input_entry.config(state="normal")
            self.endday_input_entry.config(state="normal")

    # filedialogs for input and ouptut paths
    def select_file(self, deco):
        if deco == 'in':
            self.input_path = filedialog.askopenfilename(title="Input files",
                                                         initialdir="/")
            self.input_file_label.config(text=f"Input: {self.input_path.split('/')[-1]}")
        elif deco == 'out':
            self.output_path = filedialog.askdirectory(title="Output directory",
                                                       initialdir="/")
            self.output_path_label.config(text=f"Output: {self.output_path.split('/')[-1]}")

    # start background thread of main_back.py run()
    def start(self):

        if self.month_only.get():
            params = self.settings_container.get_properties()
            runner = Thread(target=main_back.run,
                            args=[self.input_path,
                                  self.output_path,
                                  self.month_input_entry.get(),
                                  params["del_tmp"],
                                  params["blank_filling"],
                                  params["sort_by"],
                                  params["div_page_flag"],
                                  params["grouping_flag"],
                                  params["filling_quotient"]
                                  ]
                            )
            runner.start()

        elif self.month_input_entry.get() and self.startday_input_entry.get() and self.endday_input_entry.get():
            params = self.settings_container.get_properties()
            runner = Thread(target=main_back.run,
                            args=[self.input_path,
                                  self.output_path,
                                  self.month_input_entry.get(),
                                  params["del_tmp"],
                                  params["blank_filling"],
                                  params["sort_by"],
                                  params["div_page_flag"],
                                  params["grouping_flag"],
                                  params["filling_quotient"],
                                  self.startday_input_entry.get(),
                                  self.endday_input_entry.get()
                                  ]
                            )
            runner.start()

        else:
            pass


if __name__ == '__main__':
    root = Tk()
    root.geometry("1280x720")
    root.title("PDF Robot")
    settings = Settings(root)
    root.mainloop()
