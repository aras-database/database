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

for col in all_spectra.itercols():
    if col.dtype.kind in 'SU':
        all_spectra.replace_column(col.name, col.astype('object'))

dir = '../new_spectra/'

files = glob(dir + '*.fit')

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

for fi in (files):
        resOK=0
    
        with fits.open(fi) as hdu:
            hdr = hdu[0].header
            star_name_string = list_of_objects["Object"][list(list_of_objects["Keyword"]).index(list(set([hdr['OBJNAME'].lstrip()]).intersection(set(list_of_objects["Keyword"])))[0])].replace(" ", "").lower()
            date = Time(hdr['JD-MID'], format="jd").isot[0:10]
            time = Time(hdr['JD-MID'], format="jd").isot[11:16]
            jd = round(Time(hdr['JD-MID'], format="jd").mjd+0.5, 3)
            observer = list_of_observers["Observer"][np.array(list_of_observers["Keyword"][:]).tolist().index(hdr['OBSERVER'])]
            site = list_of_sites["Site"][np.array(list_of_sites["Keyword"][:]).tolist().index(hdr['BSS_SITE'])]
            
            
            # if 'SPE_RPOW' in hdr:
            #     if  hdr['SPE_RPOW'] > 0:
            #         resolution = np.int(hdr['SPE_RPOW'])
            #         resOK=1
            #         print("ok2")
            # if ('BSS_ITRP' in hdr) & (resOK == 0):
            #     if hdr['BSS_ITRP'] > 0:
            #         resolution = np.int(hdr['BSS_ITRP'])
            #         resOK=1
            # if resOK == 0:
            #     if 'CDELT1' in hdr:
            #         resolution = np.int(550/hdr['CDELT1'])
            #     else:
            #         resolution = np.int(-10)
            # lambda_min = np.int(np.round(hdr['CRVAL1']))
            # lambda_max = np.int(np.round(hdr['CRVAL1']+hdr['NAXIS1']*hdr['CDELT1']))
            
            
            if 'SPE_RPOW' in hdr:
                if  hdr['SPE_RPOW'] > 0:
                    resolution = np.round(hdr['SPE_RPOW'],0)
                    resOK=1
            if ('BSS_ITRP' in hdr) & (resOK == 0):
                if hdr['BSS_ITRP'] > 0:
                    resolution = np.round(hdr['BSS_ITRP'],0)
                    resOK=1
            if resOK == 0:
                print("checks resolution keyword ")
                    
            
            
            
            
            lambda_min = np.round(hdr['CRVAL1'],0)
            lambda_max = np.round(hdr['CRVAL1']+hdr['NAXIS1']*hdr['CDELT1'],0)
            
            
            
            
            
            #resolution = 9000
 
            
            
            
            file = fi[len(dir):]
            preview = fi[len(dir):-4]+'.png'
            comment = " "
            last_update = Time.now().unix
            all_spectra.add_row([0,star_name_string, date, time, jd, observer, site, resolution, lambda_min, lambda_max, file, preview, last_update, comment])
        move(fi, '../spectra/'+fi[len(dir):])
    
ascii.write(all_spectra, '../data/all_spectra.csv', format="csv", delimiter = ";",overwrite=True)
