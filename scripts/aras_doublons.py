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





all_spectra = ascii.read("../data/all_spectra.csv", header_start=0, data_start=1, delimiter=';',format='csv')
try:
    all_spectra.rename_column('ď»żstar_name_string', 'star_name_string')
except:
    pass

symbiotic_stars = ascii.read("../data/symbiotic_stars.csv", header_start=0, data_start=1, delimiter=';',format='csv')
try:
    symbiotic_stars.rename_column('ď»żstar_name_string', 'star_name_string')
except:
    pass



df = pd.read_csv('../data/all_spectra.csv', delimiter=";")
df1 =df.sort_values("star_name_string")
df1 =df.sort_values(by=["star_name_string","jd"])
print(df1)


nLines = len(df1)
print(nLines)
for n in range(1,nLines):
    if df1.file[n]==df1.file[n-1]:
        print(n)
        print(df1.file[n-1])
        print(df1.file[n])
        
     
df1.to_csv('../data/all_spectra_sort.csv',index=True)