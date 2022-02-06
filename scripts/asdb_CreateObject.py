from astropy.coordinates import SkyCoord
from astroquery.simbad import Simbad
#from astropy.io import ascii
import os

#data
ObjName = 'V648 Car'
Program = "ARAS Symbiotics Program"
File0 = 'symbiotic_stars.csv'
hr = "2" # Priority HR
lr = "2" # Priority LR
cadency = 90

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

ObjectCoordinates = SkyCoord.from_name(ObjName)


simbad = Simbad()
simbad.add_votable_fields('sptype')
simbad.add_votable_fields('rv_value')
simbad.add_votable_fields('flux(V)')
result_table = simbad.query_object(ObjName)
result_table.pprint(show_unit=True)

Coord1 = result_table['RA'][0]
Coord1 = Coord1[0:11]
Coord2 = result_table['DEC'][0]
Coord2 = Coord2[0:12]
MagV = result_table['FLUX_V'][0]

file_in = "maquette.txt"
file_out = FileName
    
f = open(file_in,'r')
filedata = f.read()
f.close()

filedata = filedata.replace('ProgramTitle',Program)
filedata = filedata.replace('Name', ObjName)
filedata = filedata.replace('C1', Coord1)
filedata = filedata.replace('C2', Coord2)
filedata = filedata.replace('Nom1', NameCatalog)
filedata = filedata.replace('Nom2', NameSimbad)
filedata = filedata.replace('MagnitudeV', str(MagV))

f = open(file_out,'w')
f.write(filedata)
f.close()
           
os.chdir(r'C:\Users\franc\OneDrive\Documents\GitHub\database\data')  

sep = ";"
# f = open("symbiotic_stars.csv","a")
f = open(File0,"a")

NewLine = "0"   +sep + objname + sep + ObjName + sep + Coord1 +sep +Coord2+sep+ str(cadency) + sep + str(hr) + sep+ str(lr) +'\n'
print()
print(NewLine)

f.write(NewLine)
f.close() 


    
 
