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

automatic = 1

dir = '../temporary/updated/'

files = glob(dir + '*.fit')

if automatic == 0:
    print('Number of spectra:        ', len(files))

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
jd=0
dat=0
obs=0
obj=0
CRVAL1=0
res1=0
res2=0
res3=0
site = 0
nocor=0
RES=[]
resOK=0
new_observer=[]
new_site=[]
new_object=[]
for fi in (files):
    resOK=0
    crit=0
    err=0
    try:
        with fits.open(fi) as hdu:
                hdr = hdu[0].header
                if ('CRVAL1' in hdr) & ('CDELT1' in hdr) & ('NAXIS1' in hdr) & (hdr['CRVAL1'] > 2000):
                    CRVAL1=CRVAL1+1
                else:
                    print("Wavelenght missing:       ", fi[len(dir):])
                    crit = 1
                if 'JD-MID' in hdr:
                    if hdr['JD-MID'] == 0:
                        if 'DATE-OBS'in hdr:
                            dat=dat+1
                            fits.setval(fi, 'JD-MID', value=Time(hdr['DATE-OBS'], format="isot").jd+hdr['EXPTIME']/172800)
                            err=4
                    else:
                        jd=jd+1
                elif 'DATE-OBS'in hdr:
                    dat=dat+1
                    fits.setval(fi, 'JD-MID', value=Time(hdr['DATE-OBS'], format="isot").jd)
                    err=4
                else:
                    print("Observing time missing:      ", fi[len(dir):])
                    crit=1
                if crit == 0:
                    if 'OBSERVER' in hdr:
                        if hdr['OBSERVER'] == "":
                            print("Observer missing:         ", fi[len(dir):])
                            err=1
                        else:
                            obs=obs+1
                            if len(set([hdr['OBSERVER'].lstrip()]).intersection(set(list_of_observers["Keyword"]))) == 0:
                                new_observer.append(hdr['OBSERVER'].lstrip())
                    else:
                        print("Observer missing:         ", fi[len(dir):])
                        err=1
                    if 'OBJNAME' in hdr:
                        if hdr['OBJNAME'] == "":
                            print("Object missing:      ", fi[len(dir):])
                            err=3
                        else:
                            obj=obj+1
                            if len(set([hdr['OBJNAME'].lstrip()]).intersection(set(list_of_objects["Keyword"]))) == 0:
                                new_object.append(hdr['OBJNAME'].lstrip())
                    else:
                        print("Object missing:      ", fi[len(dir):])
                        err=3
                    if 'BSS_SITE' in hdr:
                        if hdr['BSS_SITE'] == "":
                            print("Site missing:             ", fi[len(dir):])
                            err=2
                        else:
                            site = site+1
                            if len(set([hdr['BSS_SITE'].lstrip()]).intersection(set(list_of_sites["Keyword"]))) == 0:
                                new_site.append(hdr['BSS_SITE'].lstrip())
                    else:
                        print("Site missing:             ", fi[len(dir):])
                        err=2
                    if 'SPE_RPOW' in hdr:
                        if  hdr['SPE_RPOW'] > 0:
                            resOK=1
                            res1=res1+1
                    if ('BSS_ITRP' in hdr) & (resOK == 0):
                        if hdr['BSS_ITRP'] > 0:
                            resOK=1
                            res2=res2+1
                    if resOK == 0:
                        if 'CDELT1' in hdr:
                            res3=res3+1

    except:
        print("Corrupted file (unknown error):           ", fi[len(dir):])
        nocor=nocor+1
        move(fi, '../temporary/corrupted/'+fi[len(dir):])
    if crit == 1:
        print("Corrupted file (known_error):           ", fi[len(dir):])
        nocor=nocor+1
        move(fi, '../temporary/corrupted/'+fi[len(dir):])
    try:
        if err==1:
            move(fi, '../temporary/missing/observer/'+fi[len(dir):])
        elif err==2:
            move(fi, '../temporary/missing/site/'+fi[len(dir):])
        elif err==3:
            move(fi, '../temporary/missing/object/'+fi[len(dir):])
        elif err==4:
            move(fi, '../new_spectra/'+fi[len(dir):])
    except:
        pass
if automatic == 0:
    print("---------------------------------------------")
    print('Non-corrupted spectra:    ', len(files)-nocor)
    print("WAVELENGTH included:      ",CRVAL1)
    print("JD-MID/DATE included:     ",jd+dat,"(",jd,"/",dat,")")
    print("OBSERVER included:        ",obs)
    print("SITE included:            ",site)
    print("OBJECT included:          ",obj)
    print("RESOLUTION included:      ",res1+res2+res3,"(",res1,"/",res2,"/",res3,")")
    print("---------------------------------------------")
if len(new_observer) > 0:
    if automatic == 0:
        print("New keywords for observers detected.")
    with open("../temporary/new_observers.csv","w", newline="") as f:
        f.write("New observers\n")
        f.write("\n".join(str(item) for item in new_observer))

if len(new_object) > 0:
    if automatic == 0:
        print("New keywords for objects detected.")
    with open("../temporary/new_objects.csv","w", newline="") as f:
        f.write("New objects\n")
        f.write("\n".join(str(item) for item in new_object))

if len(new_site) > 0:
    if automatic == 0:
        print("New keywords for observing sites detected.")
    with open("../temporary/new_sites.csv","w", newline="") as f:
        f.write("New sites\n")
        f.write("\n".join(str(item) for item in new_site))
