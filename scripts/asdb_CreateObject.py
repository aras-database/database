from astropy.coordinates import SkyCoord
from astroquery.simbad import Simbad
import numpy as np
#from astropy.io import ascii
import os

#data
ObjName = "AM Her" 
Program = "ARAS Dwarf Novae"
File0 = 'Dwarf Novae.csv'
hr = "-" # Priority HR
lr = "-" # Priority LR
cadency = 0

# Mise en forme
FileName = ObjName.replace(" ", "") + '.txt'
FileName= FileName.lower()
NameSimbad =ObjName.replace(" ", "+")
objname =  ObjName.replace(" ", "")
objname = objname.lower()
NameCatalog = ObjName.replace(" ", "-")
NameCatalog = NameCatalog.lower()

# Main

os.chdir(r'C:\Users\franc\Documents\GitHub\database\website_source') 
print()
print("New Object: ", ObjName)
print()

ObjectCoordinates = SkyCoord.from_name(ObjName)


simbad = Simbad()
simbad.add_votable_fields('sp_type')
simbad.add_votable_fields('V')
result_table = simbad.query_object(ObjName)
result_table.pprint(show_unit=True)

Coord1 = np.round(result_table['ra'],3)
Coord2 = np.round(result_table['dec'],3)
MagV = result_table['V'][0]

file_in = "maquette.txt"
file_out = FileName
    
f = open(file_in,'r')
filedata = f.read()
f.close()

filedata = filedata.replace('ProgramTitle',"ARAS Dwarf Novae")
filedata = filedata.replace('Name', ObjName)
filedata = filedata.replace('C1', Coord1)
filedata = filedata.replace('C2', Coord2)
filedata = filedata.replace('Nom1', NameCatalog)
filedata = filedata.replace('Nom2', NameSimbad)
filedata = filedata.replace('MagnitudeV', str(MagV))

f = open(file_out,'w')
f.write(filedata)
f.close()
           
os.chdir(r'C:\Users\franc\Documents\GitHub\database\data')  

sep = ";"
# f = open("symbiotic_stars.csv","a")
f = open(File0,"a")

NewLine = "0"   +sep + objname + sep + ObjName + sep + Coord1 +sep +Coord2+sep+ str(cadency) + sep + str(hr) + sep+ str(lr) +'\n'
print()
print(NewLine)

f.write(NewLine)
f.close() 

f = open("objects.csv","a")

NewLine = "0"   +sep + ObjName + sep + ObjName +'\n'
print()
print(NewLine)

f.write(NewLine)
f.close() 
    
 
