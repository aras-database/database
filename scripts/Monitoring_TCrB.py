"""
Created on 2022-08
@author: francois teyssier
Monitoring T CrB
"""
import os
import numpy as np
import pandas as pd
import datetime as dt
from datetime import date, timedelta
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import warnings
warnings.filterwarnings("ignore")

Folder = r'C:\Users\franc\OneDrive\Documents\GitHub\database\data'
os.chdir(Folder) 
path = os.getcwd() 
df = pd.read_csv("all_spectra.csv",sep =";")
df = df.sort_values(by=["star_name_string","date"],ignore_index=False)

object = "tcrb"
df1 = df[df["star_name_string"] == object]

delta = timedelta(days = 30)
date_today = date.today()
date_debut = date_today - delta

df1["date"] = pd.to_datetime(df1["date"])
df1 = df1[df1["date"].dt.date > date_debut]


##############################################################

intervalle = 3
fig, ax = plt.subplots()

for i in range(0,3):
    print(i) 
    if i == 0:
        df2 = df1
        y0 = 1
    if i == 1:
        df2 = df1[(df1["resolution"]< 1200)]
        y0 = 1.5
    if i == 2:
        df2 = df1[(df1["lambda_min"]< 3601)]
        y0 = 2       
    # if i == 3:
    #     df2 = df1[(df1["resolution"]> 8000) & (df1["resolution"] < 12000)]
    #     y0 = 2.5  
    if i ==3:
        df2 = df1[(df1["resolution"]> 12000)]
        y0 = 3 
    
    df2 = df2[["date","jd"]]
    df2["inter"] =df2["jd"].diff( periods = 1)
    df2["ord"] = y0
    df2 = df2.fillna(0)
    last = df2["date"].iloc[len(df2.index) - 1]
    df2["inter"] = np.where(df2["inter"] < intervalle, "g", "orangered")
    df2["inter"].iloc[0] = "gray"
    if (pd.to_datetime(date_today) - last).days > intervalle*2: df2["inter"].iloc[len(df2.index) - 1] = "darkred"
    
    ax = df2.plot.scatter(x = 'date', y = 'ord',c = df2["inter"], figsize = (18,6),title="TCrB monitoring Current status: " + str(date.today()),ax=ax);

date_form = DateFormatter("%m-%d")
ax.xaxis.set_major_formatter(date_form)
ax.xaxis.set_minor_locator(plt.MultipleLocator(1))
ax.xaxis.set_major_locator(plt.MaxNLocator(7))
ax.get_yaxis().set_visible(False)

dt = timedelta(days = 1)
plt.text(date_debut+dt,1.1,"full")
plt.text(date_debut+dt,1.6,"LR")
plt.text(date_debut+dt,2.1,"Near UV")
plt.text(date_debut+dt,2.6,"Echelle")
plt.text(date_debut+dt,3.1,"HR H alpha")
plt.ylim(0.5,3.3)

filename = r"C:\Users\franc\OneDrive\Documents\GitHub\database\temporary\campaigns\tcrb.png"
plt.savefig(filename, format='png',bbox_inches='tight', dpi = 72)






plt.show()