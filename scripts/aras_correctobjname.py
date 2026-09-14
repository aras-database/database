import os
from astropy.io import fits
from specutils import Spectrum1D
import glob as glob

os.chdir(r'C:\Users\franc\Documents\GitHub\database\new_spectra')
files=glob.glob("*.fit*")  
print(files)
#objname = input("Objname")

f = fits.open(files[0])
print(f)
hdr = f[0].header

fits.setval(f, 'OBJNAME', value="Z And")
f.close()
       
    
    
















