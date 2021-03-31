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

dir = '../new_spectra/replace/'

files = glob(dir + '*.fit')+glob(dir + '*.fits')

all_spectra = ascii.read("../data/all_spectra.csv", header_start=0, data_start=1, delimiter=';',format='csv')

for col in all_spectra.itercols():
    if col.dtype.kind in 'SU':
        all_spectra.replace_column(col.name, col.astype('object'))
        
def zipFilesInDir(dirName, zipFileName, filter):
    with ZipFile(zipFileName, 'w') as zipObj:
        for folderName, subfolders, filenames in os.walk(dirName):
            for filename in filenames:
                if filter(filename):
                    filePath = os.path.join(folderName, filename)
                    zipObj.write(filePath, basename(filePath))

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
    while os.path.exists('../new_spectra/' + dst) == True:
        if int(dst[-7:-4]) < 100:
            dst = dst[:-7]+"0"+str(int(dst[-7:-4])+1)+dst[-4:]
        else:
            dst = dst[:-7]+str(int(dst[-7:-4])+1)+dst[-4:]
    os.rename(fi, '../new_spectra/replace/' + dst)
    
files = glob(dir + '*.fit')+glob(dir + '*.fits')
for fi in (files):
    if len(all_spectra[all_spectra["file"]==fi[len(dir):]])==1:
        print("The old version of the spectrum will be replaced.")
        os.remove("../spectra/" + fi[len(dir):])
        os.remove('../figures/' + fi[len(dir):-4]+'.png')       
        with fits.open(fi) as hdu:
            hdr = hdu[0].header
            obj_name = list_of_objects["Object"][list(list_of_objects["Keyword"]).index(list(set([hdr['OBJNAME'].lstrip()]).intersection(set(list_of_objects["Keyword"])))[0])]
            date_string = Time(hdr['JD-MID'], format="jd").isot[0:10]
            time_string = Time(hdr['JD-MID'], format="jd").isot[11:-4]
            obs_string = list_of_observers["Observer"][list(list_of_observers["Keyword"]).index(list(set([hdr['OBSERVER'].lstrip()]).intersection(set(list_of_observers["Keyword"])))[0])]
        if hdr['CUNIT1'] == "ANGSTROM":
            fits.setval(fi, 'CUNIT1', value="angstrom")
        spec = Spectrum1D.read(fi, format='wcs1d-fits')
        fig = plt.figure(figsize = (9,4), dpi=120)
        if np.median(spec.flux.value) > 1*10**(-5):
            plt.ylabel('Relative flux')
        else:
            plt.ylabel('Flux [erg.s⁻¹.cm⁻².Å⁻¹]')
        plt.xlabel('Wavelength [Å]')
    
        title_string = obj_name + " | " + date_string + " | " + time_string + " | " + obs_string
        plt.title(title_string)
        ax = plt.gca()
        ax.tick_params(which='both', direction='in')
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())
    
        plt.plot(spec.spectral_axis.value,spec.flux.value,'C3-')
        plt.savefig('../figures/' + fi[len(dir):-4]+'.png')
        plt.close(fig)
        move(fi, '../spectra/'+ fi[len(dir):])
        
        for symbiotic in [list_of_objects["Object"][list(list_of_objects["Keyword"]).index(list(set([hdr['OBJNAME'].lstrip()]).intersection(set(list_of_objects["Keyword"])))[0])].replace(" ", "").lower()]:
            if np.max(all_spectra[all_spectra["star_name_string"]==symbiotic]["last_update"]) > 0:
                if symbiotic != "chcyg":
                    zipFilesInDir('../spectra/', '../archives/'+symbiotic+'.zip', lambda name : symbiotic in name)
                else:
                    zipFilesInDir('../spectra/', '../archives/'+symbiotic+'2.zip', lambda name : ("chcyg_2019"  in name) or ("chcyg_202"  in name) )

        
    else:
        print("This spectrum does not seem to be in the database. You can add it as a new spectrum.")