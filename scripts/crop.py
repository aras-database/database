# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 09:35:51 2026

@author: franc, chat
"""


import os
import numpy as np
import matplotlib.pyplot as plt
import easygui

from astropy import units as u
from astropy.io import fits
from specutils import Spectrum1D


# ============================================================
# 1. Sélection du fichier
# ============================================================

filename = easygui.fileopenbox(
    msg="Sélectionnez un spectre FITS",
    title="Ouverture du spectre",
    filetypes=["*.fit", "*.fits"]
)

if filename is None:
    raise SystemExit


# ============================================================
# 2. Lecture avec Spectrum1D
# ============================================================

try:
    spectrum = Spectrum1D.read(filename)

except Exception as e:
    easygui.msgbox(
        f"Impossible de lire le spectre :\n\n{e}",
        "Erreur"
    )
    raise SystemExit


wavelength = spectrum.spectral_axis.to(u.AA)
flux = spectrum.flux


# ============================================================
# 3. Affichage du spectre
# ============================================================

plt.figure(figsize=(12, 5))

plt.plot(
    wavelength.value,
    flux.value,
    linewidth=0.8
)

plt.xlabel(r"Wavelength ($\AA$)")
plt.ylabel("Flux")
plt.title(os.path.basename(filename))
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()


# ============================================================
# 4. Lambda 0 et Lambda 1
# ============================================================

lambda0 = easygui.enterbox(
    "Lambda 0 (Å) :",
    "Crop"
)

if lambda0 is None:
    raise SystemExit

lambda1 = easygui.enterbox(
    "Lambda 1 (Å) :",
    "Crop"
)

if lambda1 is None:
    raise SystemExit

try:
    lambda0 = float(lambda0)
    lambda1 = float(lambda1)

except ValueError:
    easygui.msgbox(
        "Les longueurs d'onde doivent être numériques.",
        "Erreur"
    )
    raise SystemExit


if lambda0 >= lambda1:
    easygui.msgbox(
        "Lambda 0 doit être inférieur à Lambda 1.",
        "Erreur"
    )
    raise SystemExit


# ============================================================
# 5. Crop
# ============================================================

mask = (
    (wavelength.value >= lambda0) &
    (wavelength.value <= lambda1)
)

if not np.any(mask):
    easygui.msgbox(
        "Aucun point dans cet intervalle.",
        "Erreur"
    )
    raise SystemExit


wave_crop = wavelength[mask]
flux_crop = flux[mask]


# ============================================================
# 6. Affichage du spectre croppé
# ============================================================

plt.figure(figsize=(12, 5))

plt.plot(
    wave_crop.value,
    flux_crop.value,
    linewidth=0.8
)

plt.xlabel(r"Wavelength ($\AA$)")
plt.ylabel("Flux")
plt.title(
    f"Crop : {lambda0:.2f} – {lambda1:.2f} Å"
)

plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()


# ============================================================
# 7. OUVERTURE DU FITS ORIGINAL
# ============================================================

hdul = fits.open(filename)

# On travaille sur le HDU principal
hdu = hdul[0]

header = hdu.header.copy()


# ============================================================
# 8. Remplacement des données
# ============================================================

new_flux = flux_crop.value

hdu.data = new_flux.astype(
    hdu.data.dtype
)


# ============================================================
# 9. Mise à jour du header
# ============================================================

header["NAXIS1"] = len(new_flux)


# ------------------------------------------------------------
# Si le spectre possède une calibration linéaire :
#
# lambda = CRVAL1 + (pixel + 1 - CRPIX1) * CDELT1
#
# on recalcule CRVAL1 / CRPIX1 pour le nouveau spectre.
# ------------------------------------------------------------

if "CRVAL1" in header and "CDELT1" in header:

    # Nouvelle première longueur d'onde
    header["CRVAL1"] = float(wave_crop[0].value)

    # Le premier pixel devient le pixel 1
    header["CRPIX1"] = 1.0


# ============================================================
# 10. Mise à jour du header du HDU
# ============================================================

hdu.header = header


# ============================================================
# 11. Nom du fichier de sortie
# ============================================================

directory = os.path.dirname(filename)

basename = os.path.basename(filename)

name, extension = os.path.splitext(basename)

output_filename = os.path.join(
    directory,
    name + "_crop1" + extension
)


# ============================================================
# 12. Sauvegarde
# ============================================================

hdul.writeto(
    output_filename,
    overwrite=True
)

hdul.close()


# ============================================================
# 13. Confirmation
# ============================================================

easygui.msgbox(
    f"Spectre sauvegardé :\n\n"
    f"{output_filename}\n\n"
    f"Domaine : {lambda0:.2f} – {lambda1:.2f} Å\n"
    f"Points : {len(new_flux)}",
    "Crop terminé"
)

print()
print("Fichier original :", filename)
print("Fichier créé     :", output_filename)
print("Lambda 0         :", lambda0)
print("Lambda 1         :", lambda1)
print("Nombre de points :", len(new_flux))