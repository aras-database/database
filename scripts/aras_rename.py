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

try:
    list_of_observers.rename_column('ď»żKeyword', 'Keyword')
except:
    pass
try:
    list_of_objects.rename_column('ď»żKeyword', 'Keyword')
except:
    pass
try:
    list_of_sites.rename_column('ď»żKeyword', 'Keyword')
except:
    pass

dir = '../new_spectra/'

files = glob(dir + '*.fit')+glob(dir + '*.fits')

for fi in (files):
    with fits.open(fi) as hdu:
        hdr = hdu[0].header
        obj_name = list_of_objects["Object"][list(list_of_objects["Keyword"]).index(list(set([hdr['OBJNAME'].lstrip()]).intersection(set(list_of_objects["Keyword"])))[0])].replace(" ", "").lower()
        time_string = str(int((float(Time(hdr['JD-MID'], format="jd").isot[11:13])+float(Time(hdr['JD-MID'], format="jd").isot[14:16])/60+float(Time(hdr['JD-MID'], format="jd").isot[17:])/3600)/24*1000))
        if int(time_string) <10:
            time_string = "00"+time_string
        elif int(time_string) <100:
            time_string = "0"+time_string
        date_name = (Time(hdr['JD-MID'], format="jd").isot[0:10].replace("-","")+"_"+time_string)
        dst = "asdb_"+obj_name+"_"+date_name+".fit"
        print(dst)
    while os.path.exists('../new_spectra/' + dst) == True:
        if int(dst[-7:-4]) < 100:
            dst = dst[:-7]+"0"+str(int(dst[-7:-4])+1)+dst[-4:]
        else:
            dst = dst[:-7]+str(int(dst[-7:-4])+1)+dst[-4:]
    os.rename(fi, '../new_spectra/' + dst)
