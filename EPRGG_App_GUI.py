import numpy as np
import os
import tkinter as tk
from tkinter import messagebox
from math import log
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

summary_explanation = "This tool is used to model graphs that display the effects of pH on rainwater due " \
                      "to greenhouse gasses. It takes inputs\n for the years of data to model (between 1958 and 2003), " \
                      "along with coefficient values for the partial pressure of CO2\nfunction, and produces two graphs, " \
                      "partial pressure of CO2 as a function of years, and pH as a function of years.\nThis tool also allows you " \
                      "to save and load graph generations as well as override/edit your saved files."

inp_label_msg = "Fill out the following fields to generate your graph"

year_range_msg = "Enter the range of years\n" \
                 "between 1958 and 2003 \n"\
                 "as Integers"

Coefficient_inp_msg = "Enter desired coefficient\n" \
                      "values, or click the\n" \
                      "default values button."

Equation_display = "PCO\u2082(year) = A(year-D)\u00B2 + B(year-D) + C"

K_1 = 10 ** -6.3
K_2 = 10 ** -10.3
K_h = 10 ** -1.46
K_w = 10 ** -14

def index(list, item):
    index = 0
    for i in list:
        if i == item:
            return index
        else:
            index += 1


def delete_saves(file, filename):
    with open(file, "r") as read:
        contents = read.readlines()
        pass
    formatted_filename = filename + "\n"
    pop_index = index(contents, formatted_filename)
    contents.pop(pop_index)
    with open(file, "w+") as delete:
        delete.truncate()
        for i in contents:
            delete.write(i)
            pass
        return None


def edit_saves(file, original_item, editted_item):
    with open(file, "r") as contents:
        contents = contents.readlines()
        pass
    original_item_formatted = original_item + "\n"
    editted_item_formatted = editted_item + "\n"
    item_index = index(contents, original_item_formatted)
    contents[item_index] = editted_item_formatted
    with open(file, "w+") as rewrite:
        rewrite.truncate()
        for i in contents:
            rewrite.write(i)
            pass
        return None


def axis_interval_optimizer(start, finish):
    length = len(np.arange(start, finish))
    increment = int(length/5)
    if increment == 0:
        return np.arange(start, finish+1, 1)
    else:
        return np.arange(start, finish+increment, increment)

def save_filename(file, name):
    formatted_name = name + "\n"
    with open(file, "a") as append:
        append.write(formatted_name)
        pass
    return None

def data_loader(files, filename):
    with open(files, "r") as load:
        return np.loadtxt(filename)

def bare_name_converter(freadlines):
    product = []
    for i in freadlines:
        name = i[0:-1]
        product.append(name)
    return product

#PCO\u2082(Year) = A(Year – D)\u00B2 + B(Year – D) + C

def pco2(t, A, B, C, D):
    output = A * (t - D) ** 2 + B * (t - D) + C
    return output


def sign(num):
    try:
        num = float(num)
    except ValueError:
        return None

    if num > 0:
        number = "positive"
    elif num < 0:
        number = "negative"
    elif num == 0:
        number = "zero"
    return number


def interval(f):
    x_not = 0
    x_k = 1
    var1 = f(x_not)
    var2 = f(x_k)
    while sign(var1) == sign(var2):
        x_not += 1
        x_k += 1
        var1 = f(x_not)
        var2 = f(x_k)
    interval = [x_not, x_k]
    return interval


def root(list, f):
    a = list[0]
    b = list[1]
    midpoint = (a + b) / 2
    run = True
    while run:
        if sign(f(midpoint)) == "negative":
            a = midpoint
        elif sign(f(midpoint)) == "positive":
            b = midpoint
        elif sign(f(midpoint)) == "zero":
            return midpoint
        midpoint = (a + b) / 2
        y = round(f(midpoint), 30)
        if y == 0:
            run = False
        else:
            continue
    return midpoint


class GUI:

    def default(self):
        self.A_inp.delete(0, 'end')
        self.B_inp.delete(0, 'end')
        self.C_inp.delete(0, 'end')
        self.D_inp.delete(0, 'end')
        self.A_inp.insert(0, "0.011825")
        self.B_inp.insert(0, "1.356975")
        self.C_inp.insert(0, "339")
        self.D_inp.insert(0, "1980.5")


    def confirm_values(self):
        self.values_ready = "no"
        self.mbtn1.config(state="disabled")
        try:
            self.A = float(self.A_inp.get())
            self.B = float(self.B_inp.get())
            self.C = float(self.C_inp.get())
            self.D = float(self.D_inp.get())
            self.values_ready = "yes"
            try:
                if self.values_ready == "yes" and self.years_ready == "yes":
                    self.mbtn1.config(state="normal")
            except AttributeError:
                pass
        except ValueError:
            messagebox.showinfo(title="Error!", message="Ensure all values are NUMBERS!")

    def confirm_years(self):
        self.years_ready = "no"
        self.mbtn1.config(state="disabled")
        try:
            self.start_year = int(self.start_year_inp.get())
            self.end_year = int(self.end_year_inp.get())
            if self.start_year < 1958 or self.start_year > 2002:
                messagebox.showinfo(title="Error!", message="Out of data range")
            elif self.end_year < 1959 or self.end_year > 2003:
                messagebox.showinfo(title="Error!", message="Out of data range")
            else:
                if self.start_year > self.end_year:
                    messagebox.showinfo(title="Error!", message="Start year cannot\nbe greater than end year!")
                    return None
                else:
                    self.years = np.arange(1958, 2004, 1)
                    self.start = index(self.years, self.start_year)
                    self.end = index(self.years, self.end_year) + 1
                    self.yearrange = self.years[self.start:self.end]
                    self.years_ready = "yes"
                    try:
                        if self.values_ready == "yes" and self.years_ready == "yes":
                            self.mbtn1.config(state="normal")
                    except AttributeError:
                        pass
        except ValueError:
            messagebox.showinfo(title="Error!", message="Ensure years are INTEGER NUMBERS!")
            pass

    def save_graphs(self, columnstack):

        self.user_inp = self.save_prompt.get()
        if self.user_inp == "":
            messagebox.showinfo(title="Error!", message="No file name entered")
        elif len(self.user_inp) > 32:
            messagebox.showinfo(title="Error!", message="Maximum of 32 characters for file name!")
        else:
            if self.user_inp + "\n" in self.saved_files:
                messagebox.showinfo(title="Error!", message="File name already in use, try another.")
            else:
                np.savetxt(self.user_inp, columnstack)
                save_filename(self.data_file, self.user_inp)
                self.save_root.destroy()

    def save_graphs_win(self, columnstack):

        self.save_root = tk.Toplevel()
        self.save_root.geometry("300x200+300+200")
        self.save_root.title("Save Data")

        self.saveframe = tk.Frame(self.save_root)
        self.saveframe.columnconfigure(0, weight=2)
        self.saveframe.columnconfigure(1, weight=1)
        self.saveframe.columnconfigure(2, weight=1)
        self.save_exitbtn = tk.Button(self.saveframe, text="Cancel",
                                      font=("Arial", 16), command=lambda: self.save_root.destroy())
        self.save_exitbtn.grid(row=0, column=1, sticky="ew")
        self.save_btn = tk.Button(self.saveframe, text="Save",
                                  font=("Arial", 16), command=lambda: self.save_graphs(columnstack))
        self.save_btn.grid(row=0, column=2, sticky="ew")

        self.save_instr = tk.Label(self.save_root, text="Enter the name you would\nlike to save the file as\nbelow and "
                                                        "click save."
                                   , font=("Calibri", 20))
        self.save_prompt = tk.Entry(self.save_root)
        self.save_instr.pack(pady=5, padx=5)
        self.save_prompt.pack(padx=5, pady=15, expand=True, fill="x")
        self.saveframe.pack(padx=5, pady=15, side=tk.BOTTOM)

        self.save_root.transient(self.gen_root)
        self.save_root.grab_set()
        self.save_root.wait_window(self.save_root)


    def create_graphs(self, columnstack, *, new_gen=bool):

        years_float = columnstack[:, 0]
        years = [int(i) for i in years_float]
        pco2 = columnstack[:, 1]
        pH = columnstack[:, 2]


        self.gen_root = tk.Toplevel()
        self.gen_root.geometry('1400x650+25+100')
        self.gen_root.title("Generated Graphs")

        self.gen_exitbtn = tk.Button(self.gen_root, text="Exit",\
                            font=("Arial", 20), command=lambda: self.gen_root.destroy())

        self.gen_savebtn = tk.Button(self.gen_root, text="Save Graphs",font=("Arial", 20),
                                     command=lambda: self.save_graphs_win(self.array_package))

        self.f = Figure(figsize=(15,8), dpi=216)
        self.pH_plot = self.f.add_subplot(121)
        self.pH_plot.plot(years, pH)
        self.pH_plot.set_xlabel("Years")
        self.pH_plot.set_ylabel("pH")
        self.pH_plot.set_title("Rainwater pH Vs. Years")
        self.pH_plot.set_xticks(axis_interval_optimizer(min(years), max(years)))
        self.pH_plot.tick_params(axis="x", rotation=55)
        self.co2_plot = self.f.add_subplot(122)
        self.co2_plot.plot(years, pco2)
        self.co2_plot.set_xlabel("Years")
        self.co2_plot.set_ylabel("ppm")
        self.co2_plot.set_title("Carbon Dioxide Partial\nPressure Vs. Years")
        self.co2_plot.set_xticks(axis_interval_optimizer(min(years), max(years)))
        self.co2_plot.tick_params(axis="x", rotation=55)
        self.f.set_tight_layout(tight=True)
        self.plot_window = FigureCanvasTkAgg(self.f, self.gen_root)

        self.plot_window.get_tk_widget().pack(padx=20, pady=20)
        self.gen_exitbtn.place(x=1325, y=585, width=65, height=50)
        self.gen_exitbtn.tkraise()

        if new_gen == True:
            self.gen_savebtn.place(x=1200, y=585, width=125, height=50)
            self.gen_savebtn.tkraise()
        else:
            pass

        self.gen_root.transient(self.root)
        self.gen_root.grab_set()
        self.gen_root.wait_window(self.gen_root)


    def gen_graphs(self):

        if self.values_ready == "yes" and self.years_ready == "yes":

            empty_pco2_list = []
            for i in self.yearrange:
                par_pres = pco2(i, self.A, self.B, self.C, self.D)
                empty_pco2_list.append(par_pres)

            self.pco2_array = np.array(empty_pco2_list)

            Hconc_list = []
            for i in self.pco2_array:

                def f(x):
                    try:
                        x = float(x)
                    except ValueError:
                        return None
                    output = x ** 3 - x * (((K_1 * K_h * i) / 10 ** 6) + K_w) - (2 * K_1 * K_2 * K_h * i) / 10 ** 6
                    return output


                Hconc = root(interval(f), f)
                Hconc_list.append(Hconc)

            empty_pH_list = []
            for i in Hconc_list:
                pH = -log(i)
                empty_pH_list.append(pH)

            self.pH_array = np.array(empty_pH_list)

            self.array_package = np.column_stack([self.yearrange, self.pco2_array, self.pH_array])
            print(self.array_package)
            self.create_graphs(self.array_package, new_gen=True)

        else:
            messagebox.showinfo(title="Error!", message="Ensure VALID year and value selection!")


    def root_exitbtn_clicked(self):
        # print(self.root_exitbtn.winfo_rootx())
        # print(self.root_exitbtn.winfo_rooty())

        self.main_exit = tk.Toplevel()
        self.main_exit.geometry("200x200+350+200")
        self.main_exit.title("Exit?")

        self.exit_querry = tk.Label(self.main_exit, text="Are you sure you want to\nexit the program?",
                                    font=("Calibri", 16))
        self.main_exit_frame = tk.Frame(self.main_exit)
        self.main_exit_frame.columnconfigure(0, weight=2)
        self.main_exit_frame.columnconfigure(1, weight=1)
        self.main_exit_frame.columnconfigure(2, weight=1)

        self.main_exitcncl = tk.Button(self.main_exit_frame, text="Cancel", font=("Arial", 16),
                                       command=lambda: self.main_exit.destroy())
        self.main_exitcncl.grid(row=0, column=1, sticky="ew")
        self.main_exitconf = tk.Button(self.main_exit_frame, text="Exit", font=("Arial", 16),
                                       command=lambda: self.root.destroy())
        self.main_exitconf.grid(row=0, column=2, sticky="ew")

        self.exit_querry.pack(padx=4, pady=5)
        self.main_exit_frame.pack(padx=5, pady=5, side=tk.BOTTOM)

        self.main_exit.transient(self.root)
        self.main_exit.grab_set()
        self.main_exit.wait_window(self.main_exit)

        self.main_exit.transient(self.root)
        self.main_exit.grab_set()
        self.main_exit.wait_window(self.main_exit)

    def create_button_list_load(self, buttonframe, label, row_number, data_file):

        self.list_button = tk.Button(buttonframe, text=label, font=("Arial", 16),
                           command=lambda: self.create_graphs(data_loader(data_file, label), new_gen=False))
        return self.list_button.grid(row=row_number, column=0, sticky="news", ipadx=4, ipady=4)

    def load_files_clicked(self):

        self.load_root = tk.Toplevel()
        self.load_root.geometry("350x400+400+150")
        self.load_root.title("Load File")

        self.loadscroll_frame = tk.Frame(self.load_root)
        self.loadscroll_frame.pack(fill=tk.BOTH, expand=True)
        self.loadscroll_canvas = tk.Canvas(self.loadscroll_frame)
        self.loadscroll_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10, padx=10)
        self.load_win_scrollbar = tk.Scrollbar(self.loadscroll_frame, orient="vertical",
                                          command=self.loadscroll_canvas.yview)
        self.load_win_scrollbar.pack(side=tk.RIGHT, fill="y", padx=2)
        self.loadscroll_canvas.configure(yscrollcommand=self.load_win_scrollbar.set)
        self.loadscroll_canvas.bind('<Configure>', lambda e: self.loadscroll_canvas.configure(
            scrollregion = self.loadscroll_canvas.bbox("all")))
        self.load_root_frame = tk.Frame(self.loadscroll_canvas)
        self.loadscroll_canvas.create_window((0,0), window=self.load_root_frame)
        self.load_root_frame.columnconfigure(0, weight=1)

        with open(self.data_file, "r") as load:
            self.saved_load = load.readlines()
            pass

        self.file_names_load = bare_name_converter(self.saved_load)


        btn_row_num = 0
        for i in self.file_names_load:
            self.create_button_list_load(self.load_root_frame, i, btn_row_num, self.data_file)
            btn_row_num += 1

        self.load_root.transient(self.root)
        self.load_root.grab_set()
        self.load_root.wait_window(self.load_root)


    def delete_func(self, filename):
        delete_saves(self.data_file, filename)
        os.remove(filename)

        with open(self.data_file, "r") as edit:
            self.saved_delete_func_update = bare_name_converter(edit.readlines())
            pass

        for widgets in self.edit_root_frame.winfo_children():
            widgets.destroy()

        delt_list_ind = 0
        for i in self.saved_delete_func_update:
            self.create_button_list_edit(self.edit_root_frame, i, delt_list_ind)
            delt_list_ind += 1

        self.delete_root.destroy()
        messagebox.showinfo(title="Status", message="File Truncation Successful!")

    def delete_win(self, filename):

        self.delete_root = tk.Toplevel()
        self.delete_root.geometry("200x200+350+200")
        self.delete_root.title("Delete Data?")

        self.delete_querry = tk.Label(self.delete_root, text="Are you sure you want\nto delete this data file?\nAction"
                                                             "cannot be undone.", font=("Calibri", 16))
        self.delete_querry.pack(padx=4, pady=10)

        self.delete_win_frame = tk.Frame(self.delete_root)
        self.delete_win_frame.columnconfigure(0, weight=3)
        self.delete_win_frame.columnconfigure(1, weight=1)
        self.delete_win_frame.columnconfigure(2, weight=1)

        self.delete_cncl = tk.Button(self.delete_win_frame, text="No", font=("Calibri", 18),
                                     command=lambda: self.delete_root.destroy())
        self.delete_cncl.grid(row=0, column=1, sticky="ew", ipadx=4, ipady=4)
        self.delete_conf = tk.Button(self.delete_win_frame, text="Yes", font=("Calibri", 18),
                                     command=lambda: self.delete_func(filename))
        self.delete_conf.grid(row=0, column=2, sticky="ew", ipadx=4, ipady=4)

        self.delete_win_frame.pack(side=tk.BOTTOM, padx=4, pady=10, expand=True)

        self.delete_root.transient(self.edit_root)
        self.delete_root.grab_set()
        self.delete_root.wait_window(self.delete_root)


    def edit_func(self, orig_name):

        self.edit_filename = self.edit_prompt.get()

        with open(self.data_file, "r") as edit:
            self.saved_edit_func = edit.readlines()
            pass
        if self.edit_filename + "\n" in self.saved_edit_func:
            messagebox.showinfo(title="Error!", message="File name already in use, try another.")
        elif len(self.edit_filename) > 32:
            messagebox.showinfo(title="Error!", message="Maximum of 32 characters for file name!")
        else:
            edit_saves(self.data_file, orig_name, self.edit_filename)
            os.rename(orig_name, self.edit_filename)

            with open(self.data_file, "r") as edit:
                self.saved_edit_func_update = bare_name_converter(edit.readlines())
                pass

            for widgets in self.edit_root_frame.winfo_children():
                widgets.destroy()

            edit_list_ind = 0
            for i in self.saved_edit_func_update:
                self.create_button_list_edit(self.edit_root_frame, i, edit_list_ind)
                edit_list_ind += 1

            messagebox.showinfo(title="Status", message="File Name Edit Successful!")
            self.edit_win.destroy()

    def edit_win_c(self, orig_name):

        self.edit_win = tk.Toplevel()
        self.edit_win.geometry("300x200+300+200")
        self.edit_win.title("Edit File Name")

        self.edit_inst = tk.Label(self.edit_win, text="Enter desired file name and\nclick 'Edit' to save change.",
                                  font=("Arial", 16))
        self.edit_inst.pack(pady=10, padx=4, expand=True)
        self.edit_prompt = tk.Entry(self.edit_win)
        self.edit_win_frame = tk.Frame(self.edit_win)
        self.edit_win_frame.columnconfigure(0, weight=3)
        self.edit_win_frame.columnconfigure(1, weight=1)
        self.edit_win_frame.columnconfigure(2, weight=1)

        self.edit_prompt.pack(padx=10, pady=20, fill="x")

        self.edit_cncl = tk.Button(self.edit_win_frame, text="Cancel", font=("Calibri", 18),
                                   command=lambda: self.edit_win.destroy())
        self.edit_cncl.grid(row=0, column=1, sticky="ew", ipadx=4, ipady=4)
        self.edit_btn = tk.Button(self.edit_win_frame, text="Edit", font=("Calibri", 18),
                                  command=lambda: self.edit_func(orig_name))
        self.edit_btn.grid(row=0, column=2, sticky="ew", ipadx=4, ipady=4)

        self.edit_win_frame.pack(side=tk.BOTTOM, pady=7, padx=3, expand=True)

        self.edit_win.transient(self.edit_root)
        self.edit_win.grab_set()
        self.edit_win.wait_window(self.edit_win)

    def create_button_list_edit(self, buttonframe, label, row_num):

        self.edit_list_label = tk.Label(buttonframe, text=label, font=("Arial", 16), pady=5,
                                        relief=tk.SOLID)
        self.edit_list_delt = tk.Button(buttonframe, text="Delete", font=("Calibri", 16),
                                        command=lambda: self.delete_win(label))
        self.edit_list_edit = tk.Button(buttonframe, text="Edit", font=("Calibri", 16),
                                        command=lambda: self.edit_win_c(label))
        self.edit_list_label.grid(row=row_num, column=0, sticky="news")
        self.edit_list_delt.grid(row=row_num, column=1, sticky="news")
        self.edit_list_edit.grid(row=row_num, column=2, sticky="news")



    def edit_files_clicked(self):

        self.edit_root = tk.Toplevel()
        self.edit_root.geometry("400x300+250+150")
        self.edit_root.title("Edit Saved Files")

        with open(self.data_file, "r") as edit:
            self.saved_edit = edit.readlines()
            pass

        self.file_names_edit = bare_name_converter(self.saved_edit)

        self.editscroll_frame = tk.Frame(self.edit_root)
        self.editscroll_frame.pack(fill=tk.BOTH, expand=True)
        self.editscroll_canvas = tk.Canvas(self.editscroll_frame)
        self.editscroll_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10, padx=10)
        self.edit_win_scrollbar = tk.Scrollbar(self.editscroll_frame, orient="vertical",
                                               command=self.editscroll_canvas.yview)
        self.edit_win_scrollbar.pack(side=tk.RIGHT, fill="y", padx=2)
        self.editscroll_canvas.configure(yscrollcommand=self.edit_win_scrollbar.set)
        self.editscroll_canvas.bind('<Configure>', lambda e: self.editscroll_canvas.configure(
            scrollregion=self.editscroll_canvas.bbox("all")))
        self.edit_root_frame = tk.Frame(self.editscroll_canvas)
        self.editscroll_canvas.create_window((0,0), window=self.edit_root_frame)
        self.edit_root_frame.columnconfigure(0, weight=4)
        self.edit_root_frame.columnconfigure(1, weight=1)
        self.edit_root_frame.columnconfigure(2, weight=1)

        edit_list_ind = 0
        for i in self.file_names_edit:
            self.create_button_list_edit(self.edit_root_frame, i, edit_list_ind)
            edit_list_ind += 1

        self.edit_root.transient(self.root)
        self.edit_root.grab_set()
        self.edit_root.wait_window(self.edit_root)


    def __init__(self):

        self.data_file = "storreddatafiles.txt"
        with open(self.data_file, "a") as create:
            pass

        with open(self.data_file, "r") as file:
            self.saved_files = file.readlines()
            pass

        self.num_saves = len(self.saved_files)

        self.root = tk.Tk()
        self.root.geometry("1000x800+200+100")
        self.root.title("Effects of pH on Rainwater Computation Tool")

        self.summary = tk.Label(self.root, text=summary_explanation, font=("Arial", 18))
        self.summary.pack(fill="x", pady=12)

        self.menu_buttonframe = tk.Frame(self.root)
        self.menu_buttonframe.columnconfigure(0, weight=1)
        self.menu_buttonframe.columnconfigure(1, weight=1)
        self.menu_buttonframe.columnconfigure(2, weight=1)
        # self.menu_buttonframe.columnconfigure(3, weight=1)

        self.mbtn1 = tk.Button(self.menu_buttonframe, text="Generate Graph",font=("Calibri", 20),
                               command=self.gen_graphs, state="disabled")
        self.mbtn1.grid(row=0, column=0, sticky="we", ipadx=5, ipady=5)
        # self.mbtn2 = tk.Button(self.menu_buttonframe, text="Save file", font=("Calibri", 20))
        # self.mbtn2.grid(row=0, column=1, sticky="we")
        self.mbtn2 = tk.Button(self.menu_buttonframe, text="Load File", font=("Calibri", 20),
                               command=self.load_files_clicked)
        self.mbtn2.grid(row=0, column=1, sticky="we", ipadx=5, ipady=5)
        self.mbtn3 = tk.Button(self.menu_buttonframe, text="Edit Saved Files", font=("Calibri", 20),
                               command=self.edit_files_clicked)

        self.mbtn3.grid(row=0, column=2, sticky="we", ipadx=5, ipady=5)
        # self.menu_buttonframe.pack(pady=20)

        self.equation_display = tk.Label(self.root, text=Equation_display, font=("Arial", 16))
        self.user_inp_label = tk.Label(self.root, text=inp_label_msg, font=("Arial", 16))
        self.user_inp_label.pack(pady=5)
        self.equation_display.pack(pady=8)

        self.input_buttonframe = tk.Frame(self.root)
        self.input_buttonframe.columnconfigure(0, weight=4)
        self.input_buttonframe.columnconfigure(1, weight=1)
        self.input_buttonframe.columnconfigure(2, weight=1)
        self.input_buttonframe.columnconfigure(3, weight=4)
        self.input_buttonframe.columnconfigure(4, weight=1)

        self.year_range_inp = tk.Label(self.input_buttonframe, text=year_range_msg, font=("Arial", 16))
        self.year_range_inp.grid(row=0, column=0)
        self.start_year_inp = tk.Entry(self.input_buttonframe)
        self.start_year_inp.grid(row=0, column=1)
        self.end_year_inp = tk.Entry(self.input_buttonframe)
        self.end_year_inp.grid(row=0, column=2)
        self.year_confirm_btn = tk.Button(self.input_buttonframe, text="Confirm Year Selection",
                                          font=("Arial", 16), command=self.confirm_years)
        self.year_confirm_btn.grid(row=1, column=2)
        self.Coefficient_inp_title = tk.Label(self.input_buttonframe, text=Coefficient_inp_msg, font=("Arial", 16))
        self.Coefficient_inp_title.grid(row=0, column=3)
        self.Val_label = tk.Label(self.input_buttonframe, text="Value", font=("Arial", 18))
        self.Val_label.grid(row=0, column=4)
        self.A_val = tk.Label(self.input_buttonframe, text="A", font=("Arial", 20))
        self.A_val.grid(row=1, column=3)
        self.B_val = tk.Label(self.input_buttonframe, text="B", font=("Arial", 20))
        self.B_val.grid(row=2, column=3)
        self.C_val = tk.Label(self.input_buttonframe, text="C", font=("Arial", 20))
        self.C_val.grid(row=3, column=3)
        self.D_val = tk.Label(self.input_buttonframe, text="D", font=("Arial", 20))
        self.D_val.grid(row=4, column=3)
        self.Default_button = tk.Button(self.input_buttonframe, text="Select Default\nCoefficient Values",
                                        font=("Arial", 16), command=self.default)
        self.Default_button.grid(row=5, column=3, padx=3)
        self.A_inp = tk.Entry(self.input_buttonframe)
        self.A_inp.grid(row=1, column=4)
        self.B_inp = tk.Entry(self.input_buttonframe)
        self.B_inp.grid(row=2, column=4)
        self.C_inp = tk.Entry(self.input_buttonframe)
        self.C_inp.grid(row=3, column=4)
        self.D_inp = tk.Entry(self.input_buttonframe)
        self.D_inp.grid(row=4, column=4)
        self.Confirm_valbtn = tk.Button(self.input_buttonframe, text="Cofirm Values",
                                        font=("Arial", 16), command=self.confirm_values)
        self.Confirm_valbtn.grid(row=5, column=4)

        self.root_exitbtn = tk.Button(self.root, text="Exit", font=("Arial", 20),
                                      command=self.root_exitbtn_clicked)
        self.root_exitbtn.place(x=80, y=512, width=60, height=40)

        self.input_buttonframe.pack(padx=10, pady=10)
        self.menu_buttonframe.pack(pady=30, padx=5)

        self.root.mainloop()
        

if __name__ == '__main__':

    computation_tool_GUI = GUI()
