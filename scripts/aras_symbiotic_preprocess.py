# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 17:22:50 2020
@author: franc
"""

import os
from astropy.io import fits
from specutils import Spectrum1D
from shutil import copyfile
import pandas as pd

os.chdir(r'C:\Users\franc\OneDrive\Documents\GitHub\database\new_spectra') 
cwd = os.getcwd() 
path= cwd

files = []
n = 0


df = pd.read_csv(r'C:\Users\franc\OneDrive\Documents\GitHub\database\data\objects.csv')
print(df)


for r, d, f in os.walk(path):
    for file in f:
        if '.fit' in file:
            files.append(os.path.join(r, file))    
            
for f in files:
    n = n+1
    print('************************************************************************************')
    print(n)
    print(f)

    fitfile = fits.open(f)
    hdr = fitfile[0].header
    spec = Spectrum1D.read(f, format='wcs1d-fits')

    
    # #########read header
    
  
    t2 = fitfile[0].header['OBJNAME']

    a  = df.loc[df.Keyword == t2]


    #t2 = t2.lower()
    #t2=t2.replace(' ','')
    #t2=t2.replace('_','')
    #t2=t2.replace('-','')
    
    

    

    
    
    fits.setval(f, 'OBJNAME', value = ObjectName1,comment = 'corrected by asdb, if necessary')
    ArasFileName = 'asdb_' + t2 +'_' + datesp + '_' + str(timesp) +'.fit'#nom fichier ARAS
   
    #Copy Files
    
    fitfile.close()
    os.rename(f,ArasFileName)
    copyfile(ArasFileName,'C:/Users/franc/OneDrive/Documents/GitHub\database/new_spectra/' + ArasFileName)
    
    os.remove(ArasFileName)
    print(ArasFileName) 
    print('************************************************************************************')
    
    

















