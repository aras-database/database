# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 17:22:50 2020
@author: franc
"""

import os
from astropy.io import fits
from specutils import Spectrum1D
from shutil import copyfile
from astropy.io import ascii

os.chdir(r'C:\Users\franc\OneDrive\Documents\GitHub\database\new_spectra\novae') 
cwd = os.getcwd() 
path= cwd

files = []
n = 0

data = ascii.read("names.csv", header_start=0, data_start=1, delimiter=';',format='csv')


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
    
    t1 = fitfile[0].header['DATE-OBS']
    d = t1[0:10]
    h = t1[11:19]
    t2 = fitfile[0].header['OBJNAME']
    print("objname.header",t2)

    t2 = t2.lower()
    t2=t2.replace(' ','')
    t2=t2.replace('_','')
    
    print(t2)
    
    datesp = d[0:4] + d[5:7] + d[8:10]
    timesp = int((int(h[0:2])+int(h[3:5])/60+int(h[6:8])/3600)/24*1000)+1
    
    timesp = '{:03d}'.format(timesp)
    ArasFileName = 'asdb_' + t2 +'_' + datesp + '_' + str(timesp) +'.fit'#nom fichier ARAS
    
 
    for column in data:
        if column[1] == t2:
            indx = column[0]
            ObjectName1 = data[indx-1][2]
            ObjectName2 = data[indx-1][3]
            ObjectName3 = data[indx-1][4]   
            
    
    ObjectName1 = "Nova Lup 2025"
    ObjectName2 = "V0462 Lup"
    ObjectName3 = "ASASSN-25cm"

    ObjectName1 = "PNV Vel 2025"
    ObjectName2 = "V0XXX Vel"
    ObjectName3 = "'PNV J10251200-5331109'"



                 
    print(ObjectName1)         
    print(ObjectName2)
    print(ObjectName3)
    
    
    rep = input("Correct OBJNAME y/n : ")
    
    if rep == 'y':
        fits.setval(f, 'OBJNAME', value = ObjectName1,comment = 'corrected by asdb, if necessary')
        fits.setval(f, 'OBJNAME1', value = t2,comment = 'Original OBJNAME in the header')
        fits.setval(f, 'OBJNAME2', value=ObjectName2,comment = 'GCVS name added by asdb' )
        fits.setval(f, 'OBJNAME3', value=ObjectName3,comment = 'Discovery name added by asdb' )
        ArasFileName = 'asdb_' + t2 +'_' + datesp + '_' + str(timesp) +'.fit'#nom fichier ARAS
   
        #Copy Files
    
        fitfile.close()
        os.rename(f,ArasFileName)
        copyfile(ArasFileName,'C:/Users/franc/OneDrive/Documents/GitHub\database/new_spectra/' + ArasFileName)
        
        os.remove(ArasFileName)
        print(ArasFileName) 
        print('************************************************************************************')
    
    
    else:
        print('OBJNAME not found')
















