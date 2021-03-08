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

def zipFilesInDir(dirName, zipFileName, filter):
    with ZipFile(zipFileName, 'w') as zipObj:
        for folderName, subfolders, filenames in os.walk(dirName):
            for filename in filenames:
                if filter(filename):
                    filePath = os.path.join(folderName, filename)
                    zipObj.write(filePath, basename(filePath))

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

last_update_archive = np.float(open("../data/last_update_archive.txt", "r").read())

for symbiotic in symbiotic_stars["star_name_string"]:
    if np.max(all_spectra[all_spectra["star_name_string"]==symbiotic]["last_update"]) > last_update_archive:
        zipFilesInDir('../spectra/', '../archives/'+symbiotic+'.zip', lambda name : symbiotic in name)
last_update = open("../data/last_update_archive.txt", "w")
last_update.write(str(Time.now().unix))
last_update.close()
