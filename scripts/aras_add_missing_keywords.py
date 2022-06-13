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


missing_files = len(glob('../temporary/missing/observer/' + '*.fit'))+len(glob('../temporary/missing/site/' + '*.fit'))+len(glob('../temporary/missing/object/' + '*.fit'))+len(glob('../temporary/missing/observer/' + '*.fits'))+len(glob('../temporary/missing/site/' + '*.fits'))+len(glob('../temporary/missing/object/' + '*.fits'))
while missing_files > 0:
    dir = '../temporary/missing/observer/'
    files = glob(dir + '*.fit')+glob(dir + '*.fits')
    for fi in (files):
        print("File:", fi[len(dir):])
        obs_input = input('Observer:   ')
       
        fits.setval(fi, 'OBSERVER', value=obs_input)
        move(fi, '../temporary/updated/'+fi[len(dir):])

    dir = '../temporary/missing/object/'
    files = glob(dir + '*.fit')+glob(dir + '*.fits')
    for fi in (files):
        print("File:", fi[len(dir):])
        obs_input = input('Object:   ')
        fits.setval(fi, 'OBJNAME', value=obs_input)
        move(fi, '../temporary/updated/'+fi[len(dir):])

    dir = '../temporary/missing/site/'
    files = glob(dir + '*.fit')+glob(dir + '*.fits')
    for fi in (files):
        print("File:", fi[len(dir):])
        obs_input = input('Observing site:   ')
      
        fits.setval(fi, 'BSS_SITE', value=obs_input)
        move(fi, '../temporary/updated/'+fi[len(dir):])

    dir = '../temporary/updated/'
    files = glob(dir + '*.fit')+glob(dir + '*.fits')
    import aras_check_keywords_updated

    missing_files = len(glob('../temporary/missing/observer/' + '*.fit'))+len(glob('../temporary/missing/site/' + '*.fit'))+len(glob('../temporary/missing/object/' + '*.fit'))+len(glob('../temporary/missing/observer/' + '*.fits'))+len(glob('../temporary/missing/site/' + '*.fits'))+len(glob('../temporary/missing/object/' + '*.fits'))

dir = '../temporary/updated/'
files = glob(dir + '*.fit')+glob(dir + '*.fits')
for fi in (files):
    move(fi, '../new_spectra/'+fi[len(dir):])
