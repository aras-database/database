# correct OBJNAME according to objects.cvs names
# fmt - 2022-01-21
import os
import pandas as pd
from astropy.io import fits


df1 = pd.read_csv('../data/objects.csv', delimiter=";")
# df = pd.read_csv('../data/all_spectra.csv', delimiter=";")
# df =df.sort_values(by=["star_name_string","jd"])
# df = df.drop_duplicates(subset=["star_name_string", "jd","observer"], keep='last')
# df.to_csv('../data/all_spectra.csv',index=False,sep = ';')


path = r'C:\Users\franc\OneDrive\Documents\GitHub\database\spectra'
files = []
n = 0
for r, d, f in os.walk(path):
    for file in f: 
        if '.fit' in file:
            files.append(os.path.join(r, file))

for f in files:
    n = n+1
    if n < 12000:
        # hdul = fits.open(f)
        with fits.open(f, mode = 'update') as hdul:
            objname = hdul[0].header['OBJNAME']
            # print(objname)
     
       
            # print(n,t1)
            t = df1.loc[df1['Keyword']==objname]
            
            t = str(t.Object.values) 
            t = t.replace("['","")
            t = t.replace("']","")
            
            print(f)
            print(t)
            if len(t) > 2:
                hdul[0].header['OBJNAME']=t
            hdul.flush()
            
        
        
        