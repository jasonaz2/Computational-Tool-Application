import numpy as np
import matplotlib.pyplot as plt
from math import log

K_1 = 10 ** -6.3
K_2 = 10 ** -10.3
K_h = 10 ** -1.46
K_w = 10 ** -14


def abcd():
    run = True
    while run:
        choice = ((input("To use default A, B, C, D values, enter 'Default', otherwise enter 'Choose'")).strip()).lower()
        print(choice)
        if choice != 'default' and choice != 'choose':
            print("Invalid Input, try again")
            continue
        elif choice == 'default':
            A = 0.011825
            B = 1.356975
            C = 339
            D = 1980.5
            return A, B, C, D
        elif choice == 'choose':
            run = False
    a = True
    while a:
        try:
            A_val = float(input("Enter a positive numerical value for A"))
            if sign(A_val) == "negative" or sign(A_val) == "zero":
                print("Ensure chosen value is a positive numerical value")
                continue
            else:
                a = False
        except ValueError:
            print("Invalid Input")
    b = True
    while b:
        try:
            B_val = float(input("Enter a positive numerical value for B"))
            if sign(B_val) == "negative" or sign(B_val) == "zero":
                print("Ensure chosen value is a positive numerical value")
                continue
            else:
                b = False
        except ValueError:
            print("Invalid Input")
    c = True
    while c:
        try:
            C_val = float(input("Enter a positive numerical value for C"))
            if sign(C_val) == "negative" or sign(C_val) == "zero":
                print("Ensure chosen value is a positive numerical value")
                continue
            else:
                c = False
        except ValueError:
            print("Invalid Input")
    d = True
    while d:
        try:
            D_val = float(input("Enter a positive numerical value for D"))
            if sign(D_val) == "negative" or sign(D_val) == "zero":
                print("Ensure chosen value is a positive numerical value")
                continue
            else:
                d = False
        except ValueError:
            print("Invalid Input")

    A = A_val
    B = B_val
    C = C_val
    D = D_val
    return A, B, C, D


def index(collection, item):
    if item not in collection:
        return print("Item is not in stack")
    index_value = 0
    indicies = []
    for i in collection:
        if i == item:
            indicies.append(index_value)
        else:
            index_value += 1
    output = tuple(indicies)
    return output


def is_integer(num):
    try:
        num = float(num)
    except ValueError:
        return print("Invalid")
    if num % 1 != 0:
        return None
    else:
        return int(num)


def year_range():
    years = np.arange(1958, 2004, 1)
    year_prompt = True
    startyear_prompt = True
    endyear_prompt = True
    while year_prompt:
        while startyear_prompt:
            start_year = input("Enter opening year for range of data points")
            try:
                start_year = float(start_year)
                break
            except ValueError:
                print("Ensure year entry is a valid INTEGER")
                continue
        while endyear_prompt:
            end_year = input("Enter closing year for range of data points")
            try:
                end_year = float(end_year)
                break
            except ValueError:
                print("Ensure year entry is a valid INTEGER")
                continue
        if start_year < 1958 or start_year > 2002:
            print("Out of data range")
            continue
        elif end_year < 1959 or end_year > 2003:
            print("Out of data range")
            continue
        elif is_integer(start_year) is None:
            print("Invalid start year entry, needs to be integer")
            continue
        elif is_integer(end_year) is None:
            print("Invalid end year entry, needs to be integer")
            continue
        else:
            start = index(years, is_integer(start_year))[0]
            end = index(years, is_integer(end_year))[0] + 1
            yearrange = years[start:end]
            break

    return yearrange


def pco2(t):
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


def interval():
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


def root(list):
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


def check_num_datasaves(file):
    with open(file, "r") as f:
        f_contents = f.readlines()
        pass
    return len(f_contents)


def writ_func(file, str):
    with open(file, "a") as f:
        f.write(str + '\n')
        pass
    return None


def save_prompt(file, file_contents):
    prompting = True
    while prompting:
        prompt = input('Enter "Save" to save these plots for future viewing, and otherwise "Skip".')
        try:
            string_test = prompt.lower()
            answer = string_test.strip()
        except ValueError:
            print("Invalid input try again")
            continue
        if answer != 'save' and answer != 'skip':
            print("Invalid input try again")
            continue
        elif answer == 'save':
            while True:
                file_name = (input("Enter desired name for file:")).strip()
                if file_name + "\n" in file_contents:
                    print("File name already in use choose another.")
                    continue
                else:
                    break
            writ_func(file, file_name)
            return file_name
        else:
            prompting = False
    return None


def load_prompt(file_contents):
    inquiring = True
    while inquiring:
        question = input("Enter the name of a saved file to load and view previously saved data?, or enter nothing to skip")
        if question == "":
            return None
        elif question + "\n" not in file_contents:
            print("File not found, try different input")
            continue
        else:
            break
    return question


if __name__ == '__main__':

    # Creates a plain text file that will hold data if this is the first time program is being ran,
    # and does nothing otherwise
    data_file = "storreddatafiles.txt"
    with open(data_file, "a") as create:
        pass

    # Opens the file in read mode and creates a list of all the saved file's names
    with open(data_file, "r") as file:
        saved_files = file.readlines()
        pass

    # Checks to see if there are 4 or less saved files (This project will hold a max of 5 saved files)

    if check_num_datasaves(data_file) <= 4 and check_num_datasaves(data_file) >= 1:
        capacity = "allow save"
    elif check_num_datasaves(data_file) == 0:
        capacity = "empty"
    else:
        capacity = "full"

# If no files are saved, will only prompt for graph generation and a save
    if capacity == "empty":

        Values = abcd()

        A = Values[0]
        B = Values[1]
        C = Values[2]
        D = Values[3]

        years = year_range()

        empty_pco2_list = []

        for i in years:
            data = pco2(i)
            empty_pco2_list.append(data)

        co2_partial_pressures = np.array(empty_pco2_list)
        Hconc_list = []

        for i in co2_partial_pressures:

            def f(x):
                try:
                    x = float(x)
                except ValueError:
                    return None
                output = x ** 3 - x * (((K_1 * K_h * i) / 10 ** 6) + K_w) - (2 * K_1 * K_2 * K_h * i) / 10 ** 6
                return output


            Hconc = root(interval())
            Hconc_list.append(Hconc)

        empty_pH = []

        for i in Hconc_list:
            pH_data = -log(i)
            empty_pH.append(pH_data)

        pH = np.array(empty_pH)

        start_year = years[0]
        end_year = years[-1]
        data_points = len(years)

        x = np.linspace(start_year, end_year, data_points)

        plt.figure(1)
        pco2 = plt.plot(x, co2_partial_pressures, label="CO2")
        plt.xlabel("Year")
        plt.ylabel("ppm")
        plt.title("Carbon Dioxide Partial Pressure")
        plt.legend()
        plt.show()

        plt.figure(2)
        pH_plot = plt.plot(x, pH, label="pH")
        plt.xlabel("Year")
        plt.ylabel("pH")
        plt.title("Level of pH")
        plt.legend()
        plt.show()

        saved_data = np.column_stack([years, co2_partial_pressures, pH])

        user_save_choice = save_prompt(data_file, saved_files)
        if user_save_choice == None:
            pass
        else:
            np.savetxt(user_save_choice, saved_data)

# If there are any number (between 1 and 5) of files saved, will prompt a load, graph generation, and save
# if the number of files is 4 or less
    elif capacity == "allow save" or capacity == "full":

        load = load_prompt(saved_files)

        if load == None:

            Values = abcd()

            A = Values[0]
            B = Values[1]
            C = Values[2]
            D = Values[3]

            years = year_range()

            empty_pco2_list = []

            for i in years:
                data = pco2(i)
                empty_pco2_list.append(data)

            co2_partial_pressures = np.array(empty_pco2_list)
            Hconc_list = []

            for i in co2_partial_pressures:

                def f(x):
                    try:
                        x = float(x)
                    except ValueError:
                        return None
                    output = x ** 3 - x * (((K_1 * K_h * i) / 10 ** 6) + K_w) - (2 * K_1 * K_2 * K_h * i) / 10 ** 6
                    return output


                Hconc = root(interval())
                Hconc_list.append(Hconc)

            empty_pH = []

            for i in Hconc_list:
                pH_data = -log(i)
                empty_pH.append(pH_data)

            pH = np.array(empty_pH)

            start_year = years[0]
            end_year = years[-1]
            data_points = len(years)

            x = np.linspace(start_year, end_year, data_points)

            plt.figure(1)
            pco2 = plt.plot(x, co2_partial_pressures, label="CO2")
            plt.xlabel("Year")
            plt.ylabel("ppm")
            plt.title("Carbon Dioxide Partial Pressure")
            plt.legend()
            plt.show()

            plt.figure(2)
            pH_plot = plt.plot(x, pH, label="pH")
            plt.xlabel("Year")
            plt.ylabel("pH")
            plt.title("Level of pH")
            plt.legend()
            plt.show()

            saved_data = np.column_stack([years, co2_partial_pressures, pH])

            if capacity == "full":
                pass
            else:
                user_save_choice = save_prompt(data_file, saved_files)
                if user_save_choice == None:
                    pass
                else:
                    np.savetxt(user_save_choice, saved_data)
        else:

            loaded_years = np.loadtxt(load)[:, 0]
            loaded_co2_pp = np.loadtxt(load)[:, 1]
            loaded_pH = np.loadtxt(load)[:, 2]

            start_year = loaded_years[0]
            end_year = loaded_years[-1]
            data_points = len(loaded_years)

            x = np.linspace(start_year, end_year, data_points)

            plt.figure(1)
            pco2 = plt.plot(x, loaded_co2_pp, label="CO2")
            plt.xlabel("Year")
            plt.ylabel("ppm")
            plt.title("Carbon Dioxide Partial Pressure")
            plt.legend()
            plt.show()

            plt.figure(2)
            pH_plot = plt.plot(x, loaded_pH, label="pH")
            plt.xlabel("Year")
            plt.ylabel("pH")
            plt.title("Level of pH")
            plt.legend()
            plt.show()
