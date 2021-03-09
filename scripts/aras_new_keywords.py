from shutil import copy2, move
from glob import glob
from astropy.io import fits
import matplotlib.pylab as plt
import numpy as np
import csv
from astropy.io import ascii
import os
from specutils.spectra import Spectrum1D
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
from astropy.time import Time
from astropy import units as u
import pandas as pd
from zipfile import ZipFile
from os.path import basename
from difflib import SequenceMatcher

list_of_observers = ascii.read("../data/observers.csv", header_start=0, data_start=1, delimiter=';',format='csv')
list_of_objects = ascii.read("../data/objects.csv", header_start=0, data_start=1, delimiter=';',format='csv')
list_of_sites = ascii.read("../data/sites.csv", header_start=0, data_start=1, delimiter=';',format='csv')

list_of_new_observers_temp = []
list_of_new_objects_temp = []
list_of_new_sites_temp = []
try:
    list_of_new_objects = ascii.read("../temporary/new_objects.csv", header_start=0, data_start=1, delimiter=';',format='csv')
    list_of_new_objects_temp = []
    for i in list_of_new_objects[0][:]:
        if i not in list_of_new_objects_temp:
            list_of_new_objects_temp.append(i)
    os.remove("../temporary/new_objects.csv")
except:
    pass
try:
    list_of_new_observers = ascii.read("../temporary/new_observers.csv", header_start=0, data_start=1, delimiter=';',format='csv')
    list_of_new_observers_temp = []
    for i in list_of_new_observers[0][:]:
        if i not in list_of_new_observers_temp:
            list_of_new_observers_temp.append(i)
    os.remove("../temporary/new_observers.csv")
except:
    pass
try:
    list_of_new_sites = ascii.read("../temporary/new_sites.csv", header_start=0, data_start=1, delimiter=';',format='csv')
    list_of_new_sites_temp = []
    for i in list_of_new_sites[0][:]:
        if i not in list_of_new_sites_temp:
            list_of_new_sites_temp.append(i)
    os.remove("../temporary/new_sites.csv")
except:
    pass

try:
    for i in list_of_new_objects_temp:
        old_ratio = 0
        current_guess = []
        print(i)
        for j in range(len(list_of_objects)):
            new_ratio = SequenceMatcher(None, i, list_of_objects["Keyword"][j]).ratio()
            if new_ratio > old_ratio:
                current_guess = list_of_objects["Object"][j]
                old_ratio = new_ratio
        if old_ratio > 0.8:
            err_anw = 1
            while err_anw == 1:
                confirmation = input(str('Could '+i +" possibly be "+current_guess+"?  (Y/N)"))
                if confirmation == "Y" or confirmation == "y":
                    list_of_objects.add_row([0, i, current_guess])
                    err_anw=0
                elif confirmation == "N" or confirmation == "n":
                    new_object_name = input(str("What is the name of "+i+"?"))
                    list_of_objects.add_row([0, i, new_object_name])
                    err_anw=0
                else:
                    print("Answer with Y or N.")
        else:
            new_object_name = input(str("What is the name of "+i+"?"))
            list_of_objects.add_row([0, i, new_object_name])
except:
    pass

try:
    for i in list_of_new_observers_temp:
        old_ratio = 0
        current_guess = []
        for j in range(len(list_of_observers)):
            new_ratio = SequenceMatcher(None, i, list_of_observers["Keyword"][j]).ratio()
            if new_ratio > old_ratio:
                current_guess = list_of_observers["Observer"][j]
                old_ratio = new_ratio
        if old_ratio > 0.8:
            err_anw = 1
            while err_anw == 1:
                confirmation = input(str('Could '+i +" possibly be "+current_guess+"?  (Y/N)"))
                if confirmation == "Y" or confirmation == "y":
                    list_of_observers.add_row([0, i, current_guess])
                    err_anw=0
                elif confirmation == "N" or confirmation == "n":
                    new_observer_name = input(str("What is the name of "+i+"?"))
                    list_of_observers.add_row([0, i, new_observer_name])
                    err_anw=0
                else:
                    print("Answer with Y or N.")
        else:
            new_observer_name = input(str("What is the name of "+i+"?"))
            list_of_observers.add_row([0, i, new_observer_name])
except:
    pass

try:
    for i in list_of_new_sites_temp:
        old_ratio = 0
        current_guess = []
        for j in range(len(list_of_sites)):
            new_ratio = SequenceMatcher(None, i, list_of_sites["Keyword"][j]).ratio()
            if new_ratio > old_ratio:
                current_guess = list_of_sites["Site"][j]
                old_ratio = new_ratio
        if old_ratio > 0.8:
            err_anw = 1
            while err_anw == 1:
                confirmation = input(str('Could '+i +" possibly be "+current_guess+"?  (Y/N)"))
                if confirmation == "Y" or confirmation == "y":
                    list_of_sites.add_row([0, i, current_guess,"un", "un", "un", 0, 0])
                    err_anw=0
                elif confirmation == "N" or confirmation == "n":
                    new_site_name = input(str("What place is "+i+"?"))
                    list_of_sites.add_row([0, i, new_site_name,"un", "un", "un", 0, 0])
                    err_anw=0
                else:
                    print("Answer with Y or N.")
        else:
            new_site_name = input(str("What place is "+i+"?"))
            list_of_sites.add_row([0, i, new_site_name,"un", "un", "un", 0, 0])

except:
    pass
if len(list_of_new_observers_temp)>0:
    ascii.write(list_of_observers, '../data/observers.csv', format="csv", delimiter = ";",overwrite=True)
if len(list_of_new_sites_temp)>0:
    ascii.write(list_of_sites, '../data/sites.csv', format="csv", delimiter = ";",overwrite=True)
if len(list_of_new_objects_temp)>0:
    ascii.write(list_of_objects, '../data/objects.csv', format="csv", delimiter = ";",overwrite=True)
