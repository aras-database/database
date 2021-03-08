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
import warnings
from astropy.utils.exceptions import AstropyWarning
warnings.simplefilter('ignore', category=AstropyWarning)

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

ang = u.def_unit('ANGSTROM', 1 * u.AA)
dir = '../new_spectra/'

files = glob(dir + '*.fit')

for fi in (files):
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
