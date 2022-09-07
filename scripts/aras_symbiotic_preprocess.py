# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 17:22:50 2020
@author: franc
"""

import os
from astropy.io import fits
from specutils import Spectrum1D
from shutil import copyfile


os.chdir(r'C:\Users\franc\OneDrive\Documents\GitHub\database\temporary\symbiotics') 
cwd = os.getcwd() 
path= cwd

files = []
n = 0





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
    
  
    ObjectName = fitfile[0].header['OBJNAME']
    print(ObjectName)
    t2 = ObjectName.replace(" ")
    print(t2)


    #t2 = t2.lower()
    #t2=t2.replace(' ','')
    #t2=t2.replace('_','')
    #t2=t2.replace('-','')
    
    

    

    
    
    fits.setval(f, 'OBJNAME', value = ObjectName,comment = 'corrected by asdb, if necessary')
    ArasFileName = 'asdb_' + t2 +'_' + datesp + '_' + str(timesp) +'.fit'#nom fichier ARAS
   
    #Copy Files
    
    fitfile.close()
    os.rename(f,ArasFileName)
    copyfile(ArasFileName,'C:/Users/franc/OneDrive/Documents/GitHub\database/new_spectra/' + ArasFileName)
    
    os.remove(ArasFileName)
    print(ArasFileName) 
    print('************************************************************************************')
    
    

















