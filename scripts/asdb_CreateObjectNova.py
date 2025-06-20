from astropy.coordinates import SkyCoord
from astroquery.simbad import Simbad
#from astropy.io import ascii
import os

#data
ObjName = 'Nova Lup 2025'
Program = "ARAS Novae Program"
File0 = 'novae.csv'

# Mise en forme
FileName = ObjName.replace(" ", "") + '.txt'
FileName= FileName.lower()
NameSimbad =ObjName.replace(" ", "+")
objname =  ObjName.replace(" ", "")
objname = objname.lower()
NameCatalog = ObjName.replace(" ", "-")
NameCatalog = NameCatalog.lower()

# Main

os.chdir(r'C:\Users\franc\OneDrive\Documents\GitHub\database\website_source') 
print()
print("New Object: ", ObjName)
print()

Coord1 = "15 08 03.27"
Coord2 = "-40 08 29.58"

file_in = "maquette.txt"
file_out = FileName
    
f = open(file_in,'r')
filedata = f.read()
f.close()

GCSVName =  ''
DiscoveryName ='ASASSN-25cm'


filedata = filedata.replace('ProgramTitle',Program)
filedata = filedata.replace('Name', ObjName)
filedata = filedata.replace('C1', Coord1)
filedata = filedata.replace('C2', Coord2)
filedata = filedata.replace('GCSVName',GCSVName)
filedata = filedata.replace('DiscoveryName',DiscoveryName )


f = open(file_out,'w')
f.write(filedata)
f.close()
           
os.chdir(r'C:\Users\franc\OneDrive\Documents\GitHub\database\data')  

sep = ";"
f = open(File0,"a")

NewLine = "0"+sep + objname + sep + ObjName + sep + Coord1 +sep +Coord2+sep  + GCSVName + sep+ DiscoveryName + '\n'
print()
print(NewLine)




f.write(NewLine)
f.close() 


    
 
