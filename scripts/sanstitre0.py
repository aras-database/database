# -*- coding: utf-8 -*-
"""
Created on Sat Dec 20 19:21:09 2025

@author: franc
"""

# RSF – New Reference Stars Finder
# Version PyQt5 AUTONOME (option 2)
# Exécution : python rsf_pyqt5.py  (hors Jupyter)

import sys
import numpy as np
import pandas as pd
from datetime import date

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QGridLayout, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView
)
from PyQt5.QtCore import Qt

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from astropy.coordinates import AltAz, EarthLocation, SkyCoord
from astropy.time import Time
from astropy import units as u

# ------------------------------------------------------------
# Données
# ------------------------------------------------------------

today = str(date.today())
distance = 30  # deg

CSV_PATH = r"C:\\Users\\franc\\Documents\\rsf_data.csv"

df = pd.read_csv(CSV_PATH, sep=";")
stars = SkyCoord(
    ra=df["RA"].values * u.deg,
    dec=df["DEC"].values * u.deg,
    frame="icrs"
)

# ------------------------------------------------------------
# Application
# ------------------------------------------------------------

class RSFApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("New Reference Stars Finder – PyQt5")
        self.resize(1400, 900)
        self._build_ui()

    # --------------------------------------------------------
    # UI
    # --------------------------------------------------------
    def _build_ui(self):
        main = QGridLayout(self)

        # ---------------- TARGET ----------------
        target = QGridLayout()
        target.addWidget(QLabel("Target"), 0, 0, 1, 2)

        self.e_target = QLineEdit()
        self.e_ra = QLineEdit()
        self.e_dec = QLineEdit()
        self.e_tstart = QLineEdit("00:00")
        self.e_dur = QLineEdit("3600")
        self.e_tend = QLineEdit()

        self.e_alt0 = QLineEdit()
        self.e_az0 = QLineEdit()
        self.e_am0 = QLineEdit()
        self.e_alt1 = QLineEdit()
        self.e_az1 = QLineEdit()
        self.e_am1 = QLineEdit()

        labels = ["Name", "RA", "Dec", "Time Start", "Duration [sec]", "Time End"]
        entries = [self.e_target, self.e_ra, self.e_dec, self.e_tstart, self.e_dur, self.e_tend]

        for i, (l, e) in enumerate(zip(labels, entries), start=1):
            target.addWidget(QLabel(l), i, 0)
            target.addWidget(e, i, 1)

        self.btn_calc = QPushButton("Get Coordinates")
        self.btn_calc.clicked.connect(self.calculer)
        target.addWidget(self.btn_calc, 7, 0, 1, 2)

        main.addLayout(target, 0, 0)

        # ---------------- OBSERVATORY ----------------
        obs = QGridLayout()
        obs.addWidget(QLabel("Observatory"), 0, 0, 1, 2)

        self.e_date = QLineEdit(today)
        self.e_utc = QLineEdit("0")
        self.e_lon = QLineEdit("0")
        self.e_lat = QLineEdit("0")
        self.e_alt = QLineEdit("0")

        obs_labels = ["Date", "UTC offset", "Longitude", "Latitude", "Altitude"]
        obs_entries = [self.e_date, self.e_utc, self.e_lon, self.e_lat, self.e_alt]

        for i, (l, e) in enumerate(zip(obs_labels, obs_entries), start=1):
            obs.addWidget(QLabel(l), i, 0)
            obs.addWidget(e, i, 1)

        main.addLayout(obs, 1, 0)

        # ---------------- TABLE ----------------
        self.table = QTableWidget(0, 9)
        self.columns = ["Name", "RA", "DEC", "B", "V", "EB-V", "Sp", "sep", "dalt"]
        self.table.setHorizontalHeaderLabels(self.columns)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSortingEnabled(True)
        self.table.itemSelectionChanged.connect(self.on_reference_selected)
        main.addWidget(self.table, 0, 1, 2, 1)

        # ---------------- GRAPHS ----------------
        graphs = QVBoxLayout()

        self.fig1 = Figure(figsize=(5, 4))
        self.ax1 = self.fig1.add_subplot(111)
        self.canvas1 = FigureCanvas(self.fig1)

        self.fig2 = Figure(figsize=(5, 4))
        self.ax2 = self.fig2.add_subplot(111)
        self.canvas2 = FigureCanvas(self.fig2)

        graphs.addWidget(self.canvas1)
        graphs.addWidget(self.canvas2)
        main.addLayout(graphs, 0, 2, 2, 1)

    # --------------------------------------------------------
    # CALCUL TARGET
    # --------------------------------------------------------
    def calculer(self):
        name = self.e_target.text().strip()
        if not name:
            return

        target = SkyCoord.from_name(name)
        self.e_ra.setText(target.ra.to_string(unit=u.hour, sep='hms', precision=0))
        self.e_dec.setText(target.dec.to_string(unit=u.deg, sep='dms', precision=0))

        utc = float(self.e_utc.text())
        lon = float(self.e_lon.text())
        lat = float(self.e_lat.text())
        alt = float(self.e_alt.text())

        dur_h = float(self.e_dur.text()) / 3600.0
        t0 = Time(f"{self.e_date.text()} {self.e_tstart.text()}", format="iso") - utc * u.hour
        t1 = t0 + dur_h * u.hour

        obs = EarthLocation(lat=lat * u.deg, lon=lon * u.deg, height=alt * u.m)

        a0 = target.transform_to(AltAz(obstime=t0, location=obs))
        a1 = target.transform_to(AltAz(obstime=t1, location=obs))

        self.e_tend.setText(t1.datetime.strftime("%H:%M"))

        # Trajectoire target
        dt = np.arange(0, dur_h, 0.01) * u.hour
        track = target.transform_to(AltAz(obstime=t0 + dt, location=obs))

        self.ax1.clear()
        self.ax1.plot(track.az.deg, track.alt.deg, label="Target")
        self.ax1.set_xlabel("Azimut [°]")
        self.ax1.set_ylabel("Altitude [°]")
        self.ax1.legend()
        self.canvas1.draw_idle()

        # Etoiles proches
        df["sep"] = stars.separation(target).deg
        df0 = df[df["sep"] < distance].copy()

        stars0 = SkyCoord(df0["RA"].values * u.deg, df0["DEC"].values * u.deg)
        altaz = stars0.transform_to(AltAz(obstime=t0, location=obs))

        df0["alt"] = altaz.alt.deg
        df0["dalt"] = abs(df0["alt"] - a0.alt.deg)
        df0 = df0[(df0["alt"] > 0) & (df0["dalt"] < 10)]

        self.fill_table(df0)

    # --------------------------------------------------------
    # TABLE
    # --------------------------------------------------------
        def fill_table(self, df0):
            # IMPORTANT : désactiver le tri pendant le remplissage
            self.table.setSortingEnabled(False)
            self.table.setRowCount(0)
        
            for _, row in df0.iterrows():
                r = self.table.rowCount()
                self.table.insertRow(r)
                for c, col in enumerate(self.columns):
                    item = QTableWidgetItem(str(row[col]))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table.setItem(r, c, item)
        
            # réactiver le tri après remplissage
            self.table.setSortingEnabled(True)

    # --------------------------------------------------------
    # CALCUL REFERENCE (sélection table)
    # --------------------------------------------------------
    def on_reference_selected(self):
        items = self.table.selectedItems()
        if not items:
            return

        name = items[0].text()
        ref = df[df["Name"] == name].iloc[0]

        star = SkyCoord(ref.RA * u.deg, ref.DEC * u.deg)

        utc = float(self.e_utc.text())
        lon = float(self.e_lon.text())
        lat = float(self.e_lat.text())
        alt = float(self.e_alt.text())
        dur_h = float(self.e_dur.text()) / 3600.0

        t0 = Time(f"{self.e_date.text()} {self.e_tstart.text()}", format="iso") - utc * u.hour
        obs = EarthLocation(lat=lat * u.deg, lon=lon * u.deg, height=alt * u.m)

        dt = np.arange(0, dur_h, 0.01) * u.hour
        track = star.transform_to(AltAz(obstime=t0 + dt, location=obs))

        self.ax2.clear()
        self.ax2.plot(track.az.deg, track.alt.deg, label=name)
        self.ax2.set_xlabel("Azimut [°]")
        self.ax2.set_ylabel("Altitude [°]")
        self.ax2.legend()
        self.canvas2.draw_idle()


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = RSFApp()
    win.show()
    sys.exit(app.exec_())
