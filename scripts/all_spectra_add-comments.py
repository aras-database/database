from astropy.io import ascii
import os
import pandas as pd


pd.options.mode.chained_assignment = None
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

all_spectra = ascii.read("../data/all_spectra.csv", header_start=0, data_start=1, delimiter=';',format='csv')
for l in range(len(all_spectra)):
    #comment
    comment = 'Ha overexposed'
    #criteria for comments
    if all_spectra[l][1] == 'rsoph' and all_spectra[l][5] == 'KSH' and all_spectra[l][4] >  59434:
        print(all_spectra[l][1],all_spectra[l][5],all_spectra[l][2])
        all_spectra[l][13]= comment
        print(all_spectra[l])
os.chdir(r'C:\Users\franc\OneDrive\Documents\GitHub\database\data') 
ascii.write(all_spectra, 'all_spectra.csv',delimiter=';',overwrite = True)