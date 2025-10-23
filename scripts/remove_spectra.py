# -*- coding: utf-8 -*-
"""
Created on Thu Oct 23 18:57:12 2025

@author: franc
"""

import os
import pandas as pd
x='asdb_tcrb_20250729_133.fit'
x1=x[0:len(x)-4] + 'png'
path=os.path.join(r'C:\Users\franc\Documents\GitHub\database\data',x)
df=pd.read_csv(r'C:\Users\franc\Documents\GitHub\database\data\all_spectra.csv',sep=";")
df = df[df["file"] != path]
df.to_csv(r'C:\Users\franc\Documents\GitHub\database\data\all_spectra1.csv',sep=";")

path=os.path.join(r'C:\Users\franc\Documents\GitHub\database\spectra',x)
if os.path.exists(path):
  os.remove(path)
  print(path,"removed")
else:
  print("The file does not exist")

path=os.path.join(r'C:\Users\franc\Documents\GitHub\database\figures',x1)
if os.path.exists(path):
  os.remove(path)
  print(path,"removed")
else:
  print("The file does not exist")
  
import aras_update_websites
 
 