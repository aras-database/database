# -*- coding: utf-8 -*-
"""
Created on Fri Nov 14 14:59:46 2025

@author: franc
"""

from astropy.coordinates import SkyCoord
from astroquery.simbad import Simbad

import os

# -----------------------------------------
# CONFIGURATION
# -----------------------------------------

ObjName = "AE Aur"
Program = "ARAS Dwarf Novae"
File0 = 'dwarf_novae.csv'
hr = "-"  # Priority HR
lr = "-"  # Priority LR
cadency = 0

# Mise en forme des noms
FileName = ObjName.replace(" ", "").lower() + '.txt'
NameSimbad = ObjName.replace(" ", "+")
objname = ObjName.replace(" ", "").lower()
NameCatalog = ObjName.replace(" ", "-").lower()

# -----------------------------------------
# CHANGEMENT DE REPERTOIRE
# -----------------------------------------

os.chdir(r'C:\Users\franc\Documents\GitHub\database\website_source')

print()
print("New Object:", ObjName)
print()

# -----------------------------------------
# RECUPERATION DES DONNEES SIMBAD
# -----------------------------------------

try:
    ObjectCoordinates = SkyCoord.from_name(ObjName)
except Exception as e:
    print("Erreur : impossible de résoudre l’objet dans Simbad.")
    print("Message :", e)
    exit(1)

simbad = Simbad()
simbad.add_votable_fields('sp_type')
simbad.add_votable_fields('V')

result_table = simbad.query_object(ObjName)

if result_table is None:
    print("Erreur : Simbad n’a retourné aucun résultat pour", ObjName)
    exit(1)

result_table.pprint(show_unit=True)

# Récupération RA/DEC/Mag
Coord1 = f"{result_table['ra'][0]:.3f}"
Coord2 = f"{result_table['dec'][0]:.3f}"

MagV = result_table['V'][0]
MagV = "?" if MagV is None else str(MagV)

# -----------------------------------------
# CREATION DE LA PAGE A PARTIR DE LA MAQUETTE
# -----------------------------------------

file_in = "maquette.txt"
file_out = FileName

with open(file_in, 'r', encoding='utf-8') as f:
    filedata = f.read()

# Remplacements
filedata = filedata.replace('ProgramTitle', Program)
filedata = filedata.replace('Name', ObjName)
filedata = filedata.replace('C1', Coord1)
filedata = filedata.replace('C2', Coord2)
filedata = filedata.replace('Nom1', NameCatalog)
filedata = filedata.replace('Nom2', NameSimbad)
filedata = filedata.replace('MagnitudeV', MagV)

with open(file_out, 'w', encoding='utf-8') as f:
    f.write(filedata)

print("✔ Fichier généré :", file_out)


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
    





