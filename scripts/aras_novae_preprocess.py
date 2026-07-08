# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 17:22:50 2020
@author: franc
"""

import os
from astropy.io import fits
from shutil import copyfile
import glob as glob

os.chdir(r'C:\Users\franc\Documents\GitHub\database\new_spectra\novae') 
cwd = os.getcwd() 
path= cwd


n = 0

#data = ascii.read("names.csv", header_start=0, data_start=1, delimiter=';',format='csv')


files=glob.glob("*.fit*")  


print(files)
            
for f in files:
    n = n+1
    print('************************************************************************************')
    
    print(f)

    fitfile = fits.open(f)
    hdr = fitfile[0].header
    

    # #########read header
    
    t1 = fitfile[0].header['DATE-OBS']
    d = t1[0:10]
    h = t1[11:19]
    Obj = fitfile[0].header['OBJNAME']
    print("objname.header",Obj)

    t2 = Obj.lower()
    t2=t2.replace(' ','')
    t2=t2.replace('_','')
    
    print(t2)
    
    datesp = d[0:4] + d[5:7] + d[8:10]
    timesp = int((int(h[0:2])+int(h[3:5])/60+int(h[6:8])/3600)/24*1000)+1
    
    timesp = '{:03d}'.format(timesp)
    ArasFileName = 'asdb_' + t2 +'_' + datesp + '_' + str(timesp) +'.fit'#nom fichier ARAS
    
    n=2
    # n=input("Lup=1, Vel=2, Ser=3, Oph=4,Sgrd=5, Cen=6: ")
    # n=float(n)
    
    if n==1:
        ObjectName = "Nova SMC 2026"
        ObjectName1 = "Nova SMC 2026"
        ObjectName2 = ""
        ObjectName3 = "AT 2016oyp"
        
   
    if n == 2:
        ObjectName = "Nova Mus 2026"
        ObjectName1 = "Nova Mus 2026"
        ObjectName2 = "V419 Mus"
        ObjectName3 = "AT 2016noc"
    
    if n==3:
            ObjectName = "Nova Aql 2026"
            ObjectName1 = "Nova Aql 2026"
            ObjectName2 = "V2104 Aql"
            ObjectName3 = "AT 2016rdg"

  

    t2=ObjectName1.replace(" ","")
    t2=t2.lower()
                 
    print(ObjectName1)         
    print("")
    fitfile.close()
    
    with fits.open(f, mode="update") as fitfile:
    
        hdr = fitfile[0].header
    
        t1 = hdr["DATE-OBS"]
        Obj = hdr["OBJNAME"]
    

    
        hdr["OBJNAME"]  = (ObjectName1, "corrected by asdb")
        hdr["OBJECT"]  = (ObjectName1, "corrected by asdb")
        hdr["OBJNAME1"] = (Obj, "original name")
        hdr["OBJNAME2"] = (ObjectName2, "GCVS name")
        hdr["OBJNAME3"] = (ObjectName3, "Discovery name")
    #Copy Files

        fitfile.close()
    os.rename(f,ArasFileName)
    copyfile(ArasFileName,r'C:\Users\franc\Documents\GitHub\database\new_spectra/' + ArasFileName)
    
    os.remove(ArasFileName)
    print(ArasFileName) 
    print('************************************************************************************')
    
    
















