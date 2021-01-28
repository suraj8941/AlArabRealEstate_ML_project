import pandas as pd
from sklearn.impute import SimpleImputer
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from joblib import dump, load
from tkinter import *
import tkinter.messagebox as tmsg

# Data Incoming .................................................
housing = pd.read_csv("data.csv")

# Training AND Testing data SPLIT.................................

train_set, test_set = train_test_split(housing, test_size=0.2, random_state=42)
split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
for train_index, test_index in split.split(housing, housing["CHAS"]):
    strat_train_set = housing.loc[train_index]
    strat_test_set = housing.loc[test_index]
housing = strat_train_set.copy()

# Imputer..........................................................

imputer = SimpleImputer(strategy="median")
imputer.fit(housing)

X = imputer.transform(housing)
housing_tr = pd.DataFrame(X, columns=housing.columns)

# Pipelining.......................................................
my_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy="median")),
    ('std_scaler', StandardScaler()),
])
housing_num_tr = my_pipeline.fit_transform(housing)

# Training data....................................................
housing = strat_train_set.drop("MEDV", axis=1)
housing_labels = strat_train_set["MEDV"].copy()

# Filling missing attributes.......................................
median = housing["RM"].median()
housing["RM"].fillna(median)

# Model Implementing...............................................
model = RandomForestRegressor()
model.fit(housing_num_tr, housing_labels)

# Dumping model....................................................
dump(model, "AL_Arab.joblib")
model = load("AL_Arab.joblib")


# OVER >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>




# GUI_INTERFACE_BEGIN......................................................................................................


root = Tk()
root.geometry("644x355")
root.title("AL_ARAB_PRICE_ESTIMATOR")

############################################################################################


def done():
    with open("Forms.txt", "a") as f:
        f.write(f"{name_d.get(),phone_d.get(), date_d.get(),fdser.get()}")
    x = data_input_d.get().split()
    x = [x]
    show_result_pop(x)

def show_result_pop(x):
    #arrr = [[-5.43942006 0.12628155 -1.12165014 -0.27288841 -1.42262747 -0.23979304 -1.31238772 1.61111401 -1.0016859 -0.5778192 -0.97491834 0.41164221 -0.86091034 0.7]]
    res = price_pred(x)
    res = round(float(res), 2)
    tmsg.showinfo("RESULT", f"Price of house should be : { res } Crores.")

Label(root, text="            PRICE ESTIMATOR FOR AL ARAB REAL ESTATE",font="Arial 13 bold").grid(row=0,column=3)

name = Label(root, text="Name")
phone = Label(root, text="Phone")
data_input = Label(root, text="Data_input")
date = Label(root, text="Date")


name.grid(row=1, column=1)
phone.grid(row=2, column=1)
data_input.grid(row=3, column=1)
date.grid(row=4, column=1)

name_d = StringVar()
phone_d = StringVar()
data_input_d = StringVar()
date_d = StringVar()
fdser = IntVar()

def price_pred(x):
    features = np.array(x)
    result = model.predict(features)
    print(result)
    return result

nameentry = Entry(root, textvariable=name_d)
phoneentry = Entry(root, textvariable=phone_d)
datarentry = Entry(root, textvariable=data_input_d)
dateentry = Entry(root, textvariable=date_d)

nameentry.grid(row=1, column=3)
phoneentry.grid(row=2, column=3)
datarentry.grid(row=3, column=3)
dateentry.grid(row=4, column=3)

data_confirm = Checkbutton(text="Have you cross-checked the data ?", variable=fdser).grid(row=6, column=3)
Button(text="SUBMIT", command=done).grid(row=7, column=3)

###################################################################################################################


def desc():
    rooot = Tk()
    rooot.geometry("900x600")
    rooot.title("DESCRIPTION")
    des_txt = open("DESCRIPTION.txt", "r")
    descrip = Label(rooot,text=des_txt.read(), font="arial 12", justify=LEFT)
    descrip.pack(anchor='nw')
    des_txt.close()
    rooot.mainloop()

def data_info_display():
    rooot = Tk()
    rooot.geometry("900x600")
    rooot.title("DATA-INFORMATION")
    des2_txt = open("DATA_INFO", "r")
    d2 = Label(rooot, text=des2_txt.read(), font="arial 12", justify=LEFT)
    d2.pack(anchor='nw')
    des2_txt.close()
    rooot.mainloop()

def data_display():
    rooot = Tk()
    rooot.geometry("900x600")
    rooot.title("DATA-COLLECTION")
    des3_txt = open("data.csv", "r")
    d3 = Label(rooot, text=des3_txt.read(), font="arial 12", justify=LEFT)
    d3.pack(anchor='nw')
    des3_txt.close()
    rooot.mainloop()
    #############################################################################################

def help():
    tmsg.showinfo("Help", " Mail for any Help : sc445524@gmail.com")

def rate():
    print("Rate us..")
    value = tmsg.askquestion("Rate", "Was your experience good ?")
    if value == "yes":
        tmsg.showinfo("Reply", "Thank you so much for your valuable feedback.")
    else:
        tmsg.showinfo("Reply", "Sorry for that , we are trying our best to make this a better application. ")


# this is main menu file,edit , wagera......
filemenu = Menu(root)

# file ka submenu or file
m1 = Menu(filemenu, tearoff=0)
m1.add_command(label="Description", command=desc)
m1.add_command(label="Data_info", command=data_info_display)
m1.add_command(label="Data", command=data_display)
m1.add_command(label="Exit", command=quit)
root.config(menu=filemenu)
filemenu.add_cascade(label="Explore", menu=m1)


# edit ka
filemenu.add_cascade(label="Help", command=help)
filemenu.add_cascade(label="Rate", command=rate)
#help



root.mainloop()


# GUI OVER ......................................................................................

