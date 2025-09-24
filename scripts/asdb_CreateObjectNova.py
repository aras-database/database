from astropy.coordinates import SkyCoord
from astroquery.simbad import Simbad
import os

# todo
# saut de ligne
# add ligne in objects.csv


#data
ObjName = 'Nova sgr 2025d'
Program = "ARAS Novae Program"
File0 = 'novae.csv'
Coord1 = "18 03 52.75"
Coord2 = "-31 27 24.7"
GCSVName =  'V7994 Sgr'
DiscoveryName ='TCP J18035290-3127298'



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



file_in = "maquette.txt"
file_out = FileName
    
f = open(file_in,'r')
filedata = f.read()
f.close()




filedata = filedata.replace('ProgramTitle',Program)
filedata = filedata.replace('Name', ObjName)
filedata = filedata.replace('C1', Coord1)
filedata = filedata.replace('C2', Coord2)
filedata = filedata.replace('GCSVName',GCSVName)
filedata = filedata.replace('DiscoveryName',DiscoveryName )


f = open(file_out,'w')
f.write(filedata)
f.close()
           
os.chdir(r'C:\Users\franc\Documents\GitHub\database\data')  

sep = ";"
f = open(File0,"a")

NewLine = "0"+sep + objname + sep + ObjName + sep + Coord1 +sep +Coord2+sep  + GCSVName + sep+ DiscoveryName + '\n'
print()
print(NewLine)




f.write(NewLine)
f.close() 


    
 
