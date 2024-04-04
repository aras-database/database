from shutil import copy2, move
from glob import glob
from astropy.io import fits
import matplotlib.pylab as plt
import numpy as np
import csv
from astropy.io import ascii
import os
from specutils.spectra import Spectrum1D
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
from astropy.time import Time
from astropy import units as u
import pandas as pd
from zipfile import ZipFile
from os.path import basename
from difflib import SequenceMatcher

pd.options.mode.chained_assignment = None
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

all_spectra = ascii.read("../data/all_spectra.csv", header_start=0, data_start=1, delimiter=';',format='csv')
try:
    all_spectra.rename_column('ď»żstar_name_string', 'star_name_string')
except:
    pass

symbiotic_stars = ascii.read("../data/symbiotic_stars.csv", header_start=0, data_start=1, delimiter=';',format='csv')
try:
    symbiotic_stars.rename_column('ď»żstar_name_string', 'star_name_string')
except:
    pass

novae = ascii.read("../data/novae.csv", header_start=0, data_start=1, delimiter=';',format='csv')
try:
    novae.rename_column('ď»żstar_name_string', 'star_name_string')
except:
    pass

dwarf_novae = ascii.read("../data/dwarf_novae.csv", header_start=0, data_start=1, delimiter=';',format='csv')
try:
    novae.rename_column('ď»żstar_name_string', 'star_name_string')
except:
    pass



symbiotic_stars_merc = ascii.read("../data/symbiotic_stars_Merc.csv", header_start=0, data_start=1, delimiter=';',format='csv')
try:
    symbiotic_stars_merc.rename_column('ď»żstar_name_string', 'star_name_string')
except:
    pass

campaigns = ascii.read("../data/campaigns.csv", header_start=0, data_start=1, delimiter=';',format='csv')

df = pd.read_csv('../data/all_spectra.csv', delimiter=";")
df = df.rename(columns={"date": "Date", "time": "Time (UT)", "jd": "JD 24..", "observer": "Observer", "site": "Site", "resolution": "Resolution", "lambda_min": "&lambda;<sub>min</sub>","lambda_max": "&lambda;<sub>max</sub>", "comment": "Comments"}).replace(np.nan, '', regex=True)


home = pd.read_csv('../data/symbiotic_stars.csv', delimiter=";")
home = home.rename(columns={"ra": "RA (2000)", "dec": "DEC (2000)", "frequency": "Frequency"}).replace(np.nan, '', regex=True)

last_update = float(open("../data/last_update.txt", "r").read())
intro = open("../website_source/navigation.txt", "r").read()
footer = open("../website_source/footer.txt", "r").read()
first_spec = []
last_spec = []
since_last_spec = []
num_spec = []
name_website = []
for symbiotic in symbiotic_stars["star_name_string"]:
    first_spec.append(str(np.min(Time(all_spectra[all_spectra["star_name_string"]==symbiotic]["date"])).value[:10]))
    last_spec.append(str(np.max(Time(all_spectra[all_spectra["star_name_string"]==symbiotic]["date"])).value[:10]))
    since_last_spec.append('<script>var date1, date2;date1 = new Date();date2 = new Date( "'+str(np.max(Time(all_spectra[all_spectra["star_name_string"]==symbiotic]["date"])).value[:10])+' 00:00:00" );var res = Math.abs(date1 - date2) / 1000;var days = Math.floor(res / 86400);document.write(days);</script>')
    num_spec.append(str(len(all_spectra[all_spectra["star_name_string"]==symbiotic])))
    name_website.append('<a href="'+symbiotic+'.html">'+symbiotic_stars["name"][symbiotic_stars["star_name_string"]==symbiotic][0]+'</a>')
    if np.max(all_spectra[all_spectra["star_name_string"]==symbiotic]["last_update"]) > 0: #last_update-10000000:
        star_intro = open("../website_source/"+symbiotic+".txt", "r").read()
        star_info = '<div class="col-sm-6">\n    <div class="card">\n      <div class="card-body">\n\n        <p class="card-text">Number of spectra:   '+str(len(all_spectra[all_spectra["star_name_string"]==symbiotic]))+'</p>\n<p class="card-text">First spectrum:   '+str(np.min(Time(all_spectra[all_spectra["star_name_string"]==symbiotic]["date"])).value[:10])+'</p>\n<p class="card-text">Last spectrum:   '+str(np.max(Time(all_spectra[all_spectra["star_name_string"]==symbiotic]["date"])).value[:10])+'</p>\n<br><br>\n<p class="card-text" style="margin-bottom:0.055cm;"><i>send spectra to francoismathieu.teyssier [at] gmail.com & arasdatabase [at] gmail.com</i></p>\n      </div>\n    </div>\n  </div>\n\n</div>\n\n<br><style>table {text-align: center;}table thead th {text-align: center;}</style>'
        current = df[df["star_name_string"]==symbiotic]

        #trial
        current = current.sort_values(by = ['JD 24..'], ascending = [False])
        #end

        campaign_string=[]
        try:
            if campaigns["campaign_type"][np.array(campaigns["star_name_string"][:]).tolist().index(symbiotic)] == "Ongoing campaign":
                campaign_type = "bg-success"
            elif campaigns["campaign_type"][np.array(campaigns["star_name_string"][:]).tolist().index(symbiotic)] == "Ongoing survey":
                campaign_type = "bg-warning"
            elif campaigns["campaign_type"][np.array(campaigns["star_name_string"][:]).tolist().index(symbiotic)] == "Current outburst":
                campaign_type = "bg-danger"
            elif campaigns["campaign_type"][np.array(campaigns["star_name_string"][:]).tolist().index(symbiotic)] == "Symbiotic nova outburst":
                campaign_type = "bg-danger"
            else:
                campaign_type = "bg-dark"
            try:
                campaign_string = '<div class="card text-white '+campaign_type+' mb-3">\n<div class="card-body">\n<h5 class="card-title">'+campaigns["campaign_type"][np.array(campaigns["star_name_string"][:]).tolist().index(symbiotic)]+'</h5>\n<p class="card-text"><p class="card-text">'+campaigns["campaign_text"][np.array(campaigns["star_name_string"][:]).tolist().index(symbiotic)]+'</p>\n</div>\n</div>\n<br>\n\n'
            except:
                campaign_string = '<div class="card text-white '+campaign_type+' mb-3">\n<div class="card-body">\n<h5 class="card-title">'+campaigns["campaign_type"][np.array(campaigns["star_name_string"][:]).tolist().index(symbiotic)]+'</h5></div>\n</div>\n<br>\n\n'

        except:
            campaign_string=''
        if symbiotic !="chcyg":
            campaign_string = campaign_string + '<a href="archives/'+symbiotic+'.zip" class="btn btn-secondary">Download all spectra as *.zip file (' + str(round(os.stat('../archives/'+symbiotic+'.zip').st_size/(1048576),1))+' MB)</a>'
        else:
            current_year_string = str(np.max(Time(all_spectra[all_spectra["star_name_string"]==symbiotic]["date"])).value[:4])
            campaign_string = campaign_string + '<a href="archives/'+symbiotic+'1.zip" class="btn btn-secondary">Download 2011-2018 spectra as *.zip file (' + str(round(os.stat('../archives/'+symbiotic+'1.zip').st_size/(1048576),1))+' MB)</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+'<a href="archives/'+symbiotic+'2.zip" class="btn btn-secondary">Download 2019-'+current_year_string +' spectra as *.zip file (' + str(round(os.stat('../archives/'+symbiotic+'2.zip').st_size/(1048576),1))+' MB)</a><br><br>'

        file_string = []
        image_string = []
        resolution_string = []
        wavelength_string = []
        for i in range(len(current)):
            file_string.append('<a href="spectra/'+current.iloc[i]["file"]+'" download target="_blank"><svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-download" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M.5 8a.5.5 0 0 1 .5.5V12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8.5a.5.5 0 0 1 1 0V12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V8.5A.5.5 0 0 1 .5 8z"/><path fill-rule="evenodd" d="M5 7.5a.5.5 0 0 1 .707 0L8 9.793 10.293 7.5a.5.5 0 1 1 .707.707l-2.646 2.647a.5.5 0 0 1-.708 0L5 8.207A.5.5 0 0 1 5 7.5z"/><path fill-rule="evenodd" d="M8 1a.5.5 0 0 1 .5.5v8a.5.5 0 0 1-1 0v-8A.5.5 0 0 1 8 1z"/></svg></a>')
            image_string.append('<a href="figures/'+current.iloc[i]["image"]+'" target="_blank"><svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-eye" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8zM1.173 8a13.134 13.134 0 0 0 1.66 2.043C4.12 11.332 5.88 12.5 8 12.5c2.12 0 3.879-1.168 5.168-2.457A13.134 13.134 0 0 0 14.828 8a13.133 13.133 0 0 0-1.66-2.043C11.879 4.668 10.119 3.5 8 3.5c-2.12 0-3.879 1.168-5.168 2.457A13.133 13.133 0 0 0 1.172 8z"/><path fill-rule="evenodd" d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0z"/></svg></a>')
            if current.iloc[i]["Resolution"] < 500:
                resolution_string.append('')
            elif current.iloc[i]["Resolution"] < 900:
                resolution_string.append('<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>')
            elif current.iloc[i]["Resolution"] < 1800:
                resolution_string.append('<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>')
            elif current.iloc[i]["Resolution"] < 4500:
                resolution_string.append('<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>')
            elif current.iloc[i]["Resolution"] < 9000:
                resolution_string.append('<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>')
            else:
                resolution_string.append('<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>')
            wavelength_string_temp = ''
            if current.iloc[i]["&lambda;<sub>min</sub>"] < 3600:
                wavelength_string_temp = wavelength_string_temp + '<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#A74AC7" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>'
            if current.iloc[i]["&lambda;<sub>min</sub>"] < 4100 and current.iloc[i]["&lambda;<sub>max</sub>"] > 4120:
                wavelength_string_temp = wavelength_string_temp + '<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#151B8D" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>'
            if current.iloc[i]["&lambda;<sub>min</sub>"] < 4670 and current.iloc[i]["&lambda;<sub>max</sub>"] >4680:
                wavelength_string_temp = wavelength_string_temp + '<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#4AA02C" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>'
            if current.iloc[i]["&lambda;<sub>min</sub>"] < 5870 and current.iloc[i]["&lambda;<sub>max</sub>"] > 5880:
                wavelength_string_temp = wavelength_string_temp + '<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#EAC117" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>'
            if current.iloc[i]["&lambda;<sub>min</sub>"] < 6550 and current.iloc[i]["&lambda;<sub>max</sub>"] > 6570:
                wavelength_string_temp = wavelength_string_temp + '<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#E42217" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>'
            if current.iloc[i]["&lambda;<sub>max</sub>"] >7500:
                wavelength_string_temp = wavelength_string_temp + '<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#8C001A" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>'
            wavelength_string.append(wavelength_string_temp)

        current["File"] = file_string
        current["Preview"] = image_string
        current['<div style="display:none;">Resolution</div>'] = resolution_string
        current['<div style="display:none;"Wavelength</div>'] = wavelength_string
        table = current.to_html(index=False, escape=False,classes="display", table_id = "table_id",border=0, columns=["Date","Time (UT)","JD 24..","Observer","Site","Resolution",'<div style="display:none;">Resolution</div>',"&lambda;<sub>min</sub>","&lambda;<sub>max</sub>",'<div style="display:none;"Wavelength</div>',"File","Preview","Comments"])
        website = open("../"+symbiotic+".html", "w")
        try:
            website.write(intro+"\n"+star_intro+star_info+campaign_string+"\n"+table+footer)
        except:
            website.write(intro+"\n"+star_intro+star_info+"\n"+table+footer)
        website.close()
home["First spectrum"] = first_spec
home["Last spectrum"] = last_spec
home["No. of spectra"] = num_spec
home["Days since last"] = since_last_spec
home["Name"] = name_website
camp_string = []
surv_string = []
outb_string = []
for stars in campaigns["star_name_string"]:
    if campaigns["campaign_type"][campaigns["star_name_string"]==stars] == "Ongoing campaign":
        try:
            camp_string = camp_string + ", " + symbiotic_stars["name"][symbiotic_stars["star_name_string"]==stars][0]
        except:
            camp_string = symbiotic_stars["name"][symbiotic_stars["star_name_string"]==stars][0]
    if campaigns["campaign_type"][campaigns["star_name_string"]==stars] == "Ongoing survey":
        try:
            surv_string = surv_string + ", " + symbiotic_stars["name"][symbiotic_stars["star_name_string"]==stars][0]
        except:
            surv_string = symbiotic_stars["name"][symbiotic_stars["star_name_string"]==stars][0]
    if campaigns["campaign_type"][campaigns["star_name_string"]==stars] == "Current outburst":
        try:
            outb_string = outb_string + ", " + symbiotic_stars["name"][symbiotic_stars["star_name_string"]==stars][0]
        except:
            outb_string = symbiotic_stars["name"][symbiotic_stars["star_name_string"]==stars][0]
    if campaigns["campaign_type"][campaigns["star_name_string"]==stars] == "Symbiotic nova outburst":
        try:
            outb_string = outb_string + ", " + symbiotic_stars["name"][symbiotic_stars["star_name_string"]==stars][0] + " (SyN)"
        except:
            outb_string = symbiotic_stars["name"][symbiotic_stars["star_name_string"]==stars][0]

if not camp_string:
    camp_string = ""
if not surv_string:
    surv_string = ""
if not outb_string:
    outb_string = ""
home_table = home.to_html(index=False, escape=False,classes="display", table_id = "table_id",border=0, columns=["Name","RA (2000)", "DEC (2000)", "No. of spectra", "First spectrum", "Last spectrum", "Days since last", "Frequency", "HR", "LR"])
sym_info = '<p class="card-text">Number of stars: '+str(len(home))+'\n</p><p class="card-text">Number of spectra: '+str(home.astype({'No. of spectra': 'int32'})["No. of spectra"].sum(axis=0))+'\n</p><p class="card-text">Last update: '+str(Time.now().isot)[0:10]+', '+str(Time.now().isot)[11:16]+'</p>\n<br><br>\n<a href="observers.html" class="btn btn-secondary">Observers</a>\n        <a href="observatories.html" class="btn btn-secondary">Observatories</a>\n\n      </div>\n    </div>\n  </div>\n\n  <div class="col-sm-6">\n    <div class="card">\n      <div class="card-body">\n        <h5 class="card-title">Stars of special interest</h5>\n<p class="card-text">Current campaigns: '+camp_string+'</p>\n<p class="card-text">Current surveys: '+surv_string+'</p>\n<p class="card-text" style="margin-bottom:0.88cm;">Outbursts: '+outb_string
home_top = open("../website_source/home_top.txt", "r").read()
home_footer = open("../website_source/home_footer.txt", "r").read()
home_info = open("../website_source/home_info.txt", "r").read()
home_website = open("../symbiotics.html", "w")
home_website.write(home_top+sym_info+home_info+home_table+home_footer)
home_website.close()

merc_syst = pd.read_csv('../data/symbiotic_stars_Merc.csv', delimiter=";")
mask = df.star_name_string.apply(lambda x: any(item for item in merc_syst.star_name_string.tolist() if item in x))
df_merc = df[mask]

file_string = []
image_string = []
resolution_string = []
wavelength_string = []
object_name_string = []
for i in range(len(df_merc)):
    object_name_string.append(merc_syst.name[merc_syst.star_name_string == df_merc.iloc[i]["star_name_string"]].values[0])
    file_string.append('<a href="spectra/'+df_merc.iloc[i]["file"]+'" download target="_blank"><svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-download" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M.5 8a.5.5 0 0 1 .5.5V12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8.5a.5.5 0 0 1 1 0V12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V8.5A.5.5 0 0 1 .5 8z"/><path fill-rule="evenodd" d="M5 7.5a.5.5 0 0 1 .707 0L8 9.793 10.293 7.5a.5.5 0 1 1 .707.707l-2.646 2.647a.5.5 0 0 1-.708 0L5 8.207A.5.5 0 0 1 5 7.5z"/><path fill-rule="evenodd" d="M8 1a.5.5 0 0 1 .5.5v8a.5.5 0 0 1-1 0v-8A.5.5 0 0 1 8 1z"/></svg></a>')
    image_string.append('<a href="figures/'+df_merc.iloc[i]["image"]+'" target="_blank"><svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-eye" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8zM1.173 8a13.134 13.134 0 0 0 1.66 2.043C4.12 11.332 5.88 12.5 8 12.5c2.12 0 3.879-1.168 5.168-2.457A13.134 13.134 0 0 0 14.828 8a13.133 13.133 0 0 0-1.66-2.043C11.879 4.668 10.119 3.5 8 3.5c-2.12 0-3.879 1.168-5.168 2.457A13.133 13.133 0 0 0 1.172 8z"/><path fill-rule="evenodd" d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0z"/></svg></a>')
    if df_merc.iloc[i]["Resolution"] < 500:
        resolution_string.append('')
    elif df_merc.iloc[i]["Resolution"] < 900:
        resolution_string.append('<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>')
    elif df_merc.iloc[i]["Resolution"] < 1800:
        resolution_string.append('<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>')
    elif df_merc.iloc[i]["Resolution"] < 4500:
        resolution_string.append('<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>')
    elif df_merc.iloc[i]["Resolution"] < 9000:
        resolution_string.append('<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>')
    else:
        resolution_string.append('<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>')
    wavelength_string_temp = ''
    if df_merc.iloc[i]["&lambda;<sub>min</sub>"] < 3600:
        wavelength_string_temp = wavelength_string_temp + '<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#A74AC7" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>'
    if df_merc.iloc[i]["&lambda;<sub>min</sub>"] < 4100 and df_merc.iloc[i]["&lambda;<sub>max</sub>"] > 4120:
        wavelength_string_temp = wavelength_string_temp + '<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#151B8D" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>'
    if df_merc.iloc[i]["&lambda;<sub>min</sub>"] < 4670 and df_merc.iloc[i]["&lambda;<sub>max</sub>"] >4680:
        wavelength_string_temp = wavelength_string_temp + '<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#4AA02C" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>'
    if df_merc.iloc[i]["&lambda;<sub>min</sub>"] < 5870 and df_merc.iloc[i]["&lambda;<sub>max</sub>"] > 5880:
        wavelength_string_temp = wavelength_string_temp + '<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#EAC117" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>'
    if df_merc.iloc[i]["&lambda;<sub>min</sub>"] < 6550 and df_merc.iloc[i]["&lambda;<sub>max</sub>"] > 6570:
        wavelength_string_temp = wavelength_string_temp + '<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#E42217" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>'
    if df_merc.iloc[i]["&lambda;<sub>max</sub>"] >7500:
        wavelength_string_temp = wavelength_string_temp + '<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#8C001A" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>'
    wavelength_string.append(wavelength_string_temp)

df_merc["File"] = file_string
df_merc["Preview"] = image_string
df_merc['<div style="display:none;">Resolution</div>'] = resolution_string
df_merc['<div style="display:none;"Wavelength</div>'] = wavelength_string
df_merc["Object"] = object_name_string

table = df_merc.to_html(index=False, escape=False,classes="display", table_id = "table_id",border=0, columns=["Object","Date","Time (UT)","JD 24..","Observer","Site","Resolution",'<div style="display:none;">Resolution</div>',"&lambda;<sub>min</sub>","&lambda;<sub>max</sub>",'<div style="display:none;"Wavelength</div>',"File","Preview","Comments"])

footer = open("../website_source/special_footer.txt", "r").read()
merc_info = open("../website_source/merc.txt", "r").read()
merc_website = open("../symbiotics-merc.html", "w")
merc_website.write(merc_info+table+footer)
merc_website.close()

lucy_syst = pd.read_csv('../data/symbiotic_stars_Lucy.csv', delimiter=";")
mask = df.star_name_string.apply(lambda x: any(item for item in lucy_syst.star_name_string.tolist() if item in x))
df_lucy = df[mask]

file_string = []
image_string = []
resolution_string = []
wavelength_string = []
object_name_string = []
for i in range(len(df_lucy)):
    object_name_string.append(lucy_syst.name[lucy_syst.star_name_string == df_lucy.iloc[i]["star_name_string"]].values[0])
    file_string.append('<a href="spectra/'+df_lucy.iloc[i]["file"]+'" download target="_blank"><svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-download" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M.5 8a.5.5 0 0 1 .5.5V12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8.5a.5.5 0 0 1 1 0V12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V8.5A.5.5 0 0 1 .5 8z"/><path fill-rule="evenodd" d="M5 7.5a.5.5 0 0 1 .707 0L8 9.793 10.293 7.5a.5.5 0 1 1 .707.707l-2.646 2.647a.5.5 0 0 1-.708 0L5 8.207A.5.5 0 0 1 5 7.5z"/><path fill-rule="evenodd" d="M8 1a.5.5 0 0 1 .5.5v8a.5.5 0 0 1-1 0v-8A.5.5 0 0 1 8 1z"/></svg></a>')
    image_string.append('<a href="figures/'+df_lucy.iloc[i]["image"]+'" target="_blank"><svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-eye" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8zM1.173 8a13.134 13.134 0 0 0 1.66 2.043C4.12 11.332 5.88 12.5 8 12.5c2.12 0 3.879-1.168 5.168-2.457A13.134 13.134 0 0 0 14.828 8a13.133 13.133 0 0 0-1.66-2.043C11.879 4.668 10.119 3.5 8 3.5c-2.12 0-3.879 1.168-5.168 2.457A13.133 13.133 0 0 0 1.172 8z"/><path fill-rule="evenodd" d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0z"/></svg></a>')
    if df_lucy.iloc[i]["Resolution"] < 500:
        resolution_string.append('')
    elif df_lucy.iloc[i]["Resolution"] < 900:
        resolution_string.append('<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>')
    elif df_lucy.iloc[i]["Resolution"] < 1800:
        resolution_string.append('<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>')
    elif df_lucy.iloc[i]["Resolution"] < 4500:
        resolution_string.append('<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>')
    elif df_lucy.iloc[i]["Resolution"] < 9000:
        resolution_string.append('<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>')
    else:
        resolution_string.append('<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>')
    wavelength_string_temp = ''
    if df_lucy.iloc[i]["&lambda;<sub>min</sub>"] < 3600:
        wavelength_string_temp = wavelength_string_temp + '<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#A74AC7" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>'
    if df_lucy.iloc[i]["&lambda;<sub>min</sub>"] < 4100 and df_lucy.iloc[i]["&lambda;<sub>max</sub>"] > 4120:
        wavelength_string_temp = wavelength_string_temp + '<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#151B8D" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>'
    if df_lucy.iloc[i]["&lambda;<sub>min</sub>"] < 4670 and df_lucy.iloc[i]["&lambda;<sub>max</sub>"] >4680:
        wavelength_string_temp = wavelength_string_temp + '<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#4AA02C" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>'
    if df_lucy.iloc[i]["&lambda;<sub>min</sub>"] < 5870 and df_lucy.iloc[i]["&lambda;<sub>max</sub>"] > 5880:
        wavelength_string_temp = wavelength_string_temp + '<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#EAC117" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>'
    if df_lucy.iloc[i]["&lambda;<sub>min</sub>"] < 6550 and df_lucy.iloc[i]["&lambda;<sub>max</sub>"] > 6570:
        wavelength_string_temp = wavelength_string_temp + '<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#E42217" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>'
    if df_lucy.iloc[i]["&lambda;<sub>max</sub>"] >7500:
        wavelength_string_temp = wavelength_string_temp + '<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#8C001A" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>'
    wavelength_string.append(wavelength_string_temp)

df_lucy["File"] = file_string
df_lucy["Preview"] = image_string
df_lucy['<div style="display:none;">Resolution</div>'] = resolution_string
df_lucy['<div style="display:none;"Wavelength</div>'] = wavelength_string
df_lucy["Object"] = object_name_string

table = df_lucy.to_html(index=False, escape=False,classes="display", table_id = "table_id",border=0, columns=["Object","Date","Time (UT)","JD 24..","Observer","Site","Resolution",'<div style="display:none;">Resolution</div>',"&lambda;<sub>min</sub>","&lambda;<sub>max</sub>",'<div style="display:none;"Wavelength</div>',"File","Preview","Comments"])

footer = open("../website_source/special_footer.txt", "r").read()
lucy_info = open("../website_source/lucy.txt", "r").read()
lucy_website = open("../symbiotics-lucy.html", "w")
lucy_website.write(lucy_info+table+footer)
lucy_website.close()


# Novae

df = pd.read_csv('../data/all_spectra.csv', delimiter=";")
df = df.rename(columns={"date": "Date", "time": "Time (UT)", "jd": "JD 24..", "observer": "Observer", "site": "Site", "resolution": "Resolution", "lambda_min": "&lambda;<sub>min</sub>","lambda_max": "&lambda;<sub>max</sub>", "comment": "Comments"}).replace(np.nan, '', regex=True)
home = pd.read_csv('../data/novae.csv', delimiter=";")
home = home.rename(columns={"ra": "RA (2000)", "dec": "DEC (2000)", "gcvs": "GCVS", "discovery_name": "Discovery Name"}).replace(np.nan, '', regex=True)


last_update = float(open("../data/last_update.txt", "r").read())
intro = open("../website_source/navigation_novae.txt", "r").read()
footer = open("../website_source/footer_novae.txt", "r").read()
first_spec = []
last_spec = []
since_last_spec = []
num_spec = []
name_website = []
for nova in novae["star_name_string"]:
    if nova in symbiotic_stars["star_name_string"]:
        first_spec.append(str(np.min(Time(all_spectra[all_spectra["star_name_string"]==nova]["date"])).value[:10]))
        last_spec.append(str(np.max(Time(all_spectra[all_spectra["star_name_string"]==nova]["date"])).value[:10]))
        since_last_spec.append('<script>var date1, date2;date1 = new Date();date2 = new Date( "'+str(np.max(Time(all_spectra[all_spectra["star_name_string"]==nova]["date"])).value[:10])+' 00:00:00" );var res = Math.abs(date1 - date2) / 1000;var days = Math.floor(res / 86400);document.write(days);</script>')
        num_spec.append(str(len(all_spectra[all_spectra["star_name_string"]==nova])))
        name_website.append('<a href="'+nova+'.html">'+novae["name"][novae["star_name_string"]==nova][0]+'</a>')
    else:
        try:
            first_spec.append(str(np.min(Time(all_spectra[all_spectra["star_name_string"]==nova]["date"])).value[:10]))
            last_spec.append(str(np.max(Time(all_spectra[all_spectra["star_name_string"]==nova]["date"])).value[:10]))
            since_last_spec.append('<script>var date1, date2;date1 = new Date();date2 = new Date( "'+str(np.max(Time(all_spectra[all_spectra["star_name_string"]==nova]["date"])).value[:10])+' 00:00:00" );var res = Math.abs(date1 - date2) / 1000;var days = Math.floor(res / 86400);document.write(days);</script>')
            num_spec.append(str(len(all_spectra[all_spectra["star_name_string"]==nova])))
            name_website.append('<a href="'+nova+'.html">'+novae["name"][novae["star_name_string"]==nova][0]+'</a>')
            if np.max(all_spectra[all_spectra["star_name_string"]==nova]["last_update"]) > 0: #last_update-10000000:
                star_intro = open("../website_source/"+nova+".txt", "r").read()
                star_info = '<div class="col-sm-6">\n    <div class="card">\n      <div class="card-body">\n\n        <p class="card-text">Number of spectra:   '+str(len(all_spectra[all_spectra["star_name_string"]==nova]))+'</p>\n<p class="card-text">First spectrum:   '+str(np.min(Time(all_spectra[all_spectra["star_name_string"]==nova]["date"])).value[:10])+'</p>\n<p class="card-text">Last spectrum:   '+str(np.max(Time(all_spectra[all_spectra["star_name_string"]==nova]["date"])).value[:10])+'</p>\n<br>\n<p class="card-text" style="margin-top:0.36cm;"><i>send spectra to francoismathieu.teyssier [at] gmail.com & arasdatabase [at] gmail.com</i></p>\n      </div>\n    </div>\n  </div>\n\n</div>\n\n<br><style>table {text-align: center;}table thead th {text-align: center;}</style>'
                current = df[df["star_name_string"]==nova]
                campaign_string=[]
                try:
                    if campaigns["campaign_type"][np.array(campaigns["star_name_string"][:]).tolist().index(nova)] == "Ongoing campaign":
                        campaign_type = "bg-success"
                    elif campaigns["campaign_type"][np.array(campaigns["star_name_string"][:]).tolist().index(nova)] == "Nova in outburst":
                        campaign_type = "bg-danger"
                    else:
                        campaign_type = "bg-dark"
                    try:
                        campaign_string = '<div class="card text-white '+campaign_type+' mb-3">\n<div class="card-body">\n<h5 class="card-title">'+campaigns["campaign_type"][np.array(campaigns["star_name_string"][:]).tolist().index(nova)]+'</h5>\n<p class="card-text"><p class="card-text">'+campaigns["campaign_text"][np.array(campaigns["star_name_string"][:]).tolist().index(nova)]+'</p>\n</div>\n</div>\n<br>\n\n'
                    except:
                        campaign_string = '<div class="card text-white '+campaign_type+' mb-3">\n<div class="card-body">\n<h5 class="card-title">'+campaigns["campaign_type"][np.array(campaigns["star_name_string"][:]).tolist().index(nova)]+'</h5></div>\n</div>\n<br>\n\n'

                except:
                    campaign_string=''
                if nova !="chcyg":
                    campaign_string = campaign_string + '<a href="archives/'+nova+'.zip" class="btn btn-secondary">Download all spectra as *.zip file (' + str(round(os.stat('../archives/'+nova+'.zip').st_size/(1048576),1))+' MB)</a>'
                else:
                    current_year_string = str(np.max(Time(all_spectra[all_spectra["star_name_string"]==nova]["date"])).value[:4])
                    campaign_string = campaign_string + '<a href="archives/'+nova+'1.zip" class="btn btn-secondary">Download 2011-2018 spectra as *.zip file (' + str(round(os.stat('../archives/'+nova+'1.zip').st_size/(1048576),1))+' MB)</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+'<a href="archives/'+nova+'2.zip" class="btn btn-secondary">Download 2019-'+current_year_string +' spectra as *.zip file (' + str(round(os.stat('../archives/'+nova+'2.zip').st_size/(1048576),1))+' MB)</a><br><br>'

                file_string = []
                image_string = []
                resolution_string = []
                wavelength_string = []
                for i in range(len(current)):
                    file_string.append('<a href="spectra/'+current.iloc[i]["file"]+'" download target="_blank"><svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-download" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M.5 8a.5.5 0 0 1 .5.5V12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8.5a.5.5 0 0 1 1 0V12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V8.5A.5.5 0 0 1 .5 8z"/><path fill-rule="evenodd" d="M5 7.5a.5.5 0 0 1 .707 0L8 9.793 10.293 7.5a.5.5 0 1 1 .707.707l-2.646 2.647a.5.5 0 0 1-.708 0L5 8.207A.5.5 0 0 1 5 7.5z"/><path fill-rule="evenodd" d="M8 1a.5.5 0 0 1 .5.5v8a.5.5 0 0 1-1 0v-8A.5.5 0 0 1 8 1z"/></svg></a>')
                    image_string.append('<a href="figures/'+current.iloc[i]["image"]+'" target="_blank"><svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-eye" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8zM1.173 8a13.134 13.134 0 0 0 1.66 2.043C4.12 11.332 5.88 12.5 8 12.5c2.12 0 3.879-1.168 5.168-2.457A13.134 13.134 0 0 0 14.828 8a13.133 13.133 0 0 0-1.66-2.043C11.879 4.668 10.119 3.5 8 3.5c-2.12 0-3.879 1.168-5.168 2.457A13.133 13.133 0 0 0 1.172 8z"/><path fill-rule="evenodd" d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0z"/></svg></a>')
                    if current.iloc[i]["Resolution"] < 500:
                        resolution_string.append('')
                    elif current.iloc[i]["Resolution"] < 900:
                        resolution_string.append('<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>')
                    elif current.iloc[i]["Resolution"] < 1800:
                        resolution_string.append('<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>')
                    elif current.iloc[i]["Resolution"] < 4500:
                        resolution_string.append('<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>')
                    elif current.iloc[i]["Resolution"] < 9000:
                        resolution_string.append('<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>')
                    else:
                        resolution_string.append('<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>')
                    wavelength_string_temp = ''
                    if current.iloc[i]["&lambda;<sub>min</sub>"] < 3600:
                        wavelength_string_temp = wavelength_string_temp + '<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#A74AC7" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>'
                    if current.iloc[i]["&lambda;<sub>min</sub>"] < 4100 and current.iloc[i]["&lambda;<sub>max</sub>"] > 4120:
                        wavelength_string_temp = wavelength_string_temp + '<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#151B8D" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>'
                    if current.iloc[i]["&lambda;<sub>min</sub>"] < 4670 and current.iloc[i]["&lambda;<sub>max</sub>"] >4680:
                        wavelength_string_temp = wavelength_string_temp + '<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#4AA02C" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>'
                    if current.iloc[i]["&lambda;<sub>min</sub>"] < 5870 and current.iloc[i]["&lambda;<sub>max</sub>"] > 5880:
                        wavelength_string_temp = wavelength_string_temp + '<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#EAC117" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>'
                    if current.iloc[i]["&lambda;<sub>min</sub>"] < 6550 and current.iloc[i]["&lambda;<sub>max</sub>"] > 6570:
                        wavelength_string_temp = wavelength_string_temp + '<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#E42217" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>'
                    if current.iloc[i]["&lambda;<sub>max</sub>"] >7500:
                        wavelength_string_temp = wavelength_string_temp + '<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#8C001A" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>'
                    wavelength_string.append(wavelength_string_temp)

                current["File"] = file_string
                current["Preview"] = image_string
                current['<div style="display:none;">Resolution</div>'] = resolution_string
                current['<div style="display:none;"Wavelength</div>'] = wavelength_string

                table = current.to_html(index=False, escape=False,classes="display", table_id = "table_id",border=0, columns=["Date","Time (UT)","JD 24..","Observer","Site","Resolution",'<div style="display:none;">Resolution</div>',"&lambda;<sub>min</sub>","&lambda;<sub>max</sub>",'<div style="display:none;"Wavelength</div>',"File","Preview","Comments"])
                website = open("../"+nova+".html", "w")
                try:
                    website.write(intro+"\n"+star_intro+star_info+campaign_string+"\n"+table+footer)
                except:
                    website.write(intro+"\n"+star_intro+star_info+"\n"+table+footer)
                website.close()
        except:
            first_spec.append(str("-"))
            last_spec.append(str("-"))
            since_last_spec.append(str("-"))
            num_spec.append(str(0))
            name_website.append(novae["name"][novae["star_name_string"]==nova][0])


print(first_spec)
print(last_spec)
home["First spectrum"] = first_spec
home["Last spectrum"] = last_spec
home["No. of spectra"] = num_spec
home["Days since last"] = since_last_spec
home["Name"] = name_website


camp_string = []
surv_string = []
outb_string = []
for stars in campaigns["star_name_string"]:
    if campaigns["campaign_type"][campaigns["star_name_string"]==stars] == "Nova in outburst":
        try:
            outb_string = outb_string + ", " + novae["name"][novae["star_name_string"]==stars][0]
        except:
            outb_string = novae["name"][novae["star_name_string"]==stars][0]

    if campaigns["campaign_type"][campaigns["star_name_string"]==stars] == "Symbiotic nova outburst":
        try:
            outb_string = outb_string + ", " + novae["name"][novae["star_name_string"]==stars][0] + " (SyN)"
        except:
            outb_string = novae["name"][novae["star_name_string"]==stars][0] + " (SyN)"

if not camp_string:
    camp_string = ""
if not surv_string:
    surv_string = ""
if not outb_string:
    outb_string = ""
home_table = home.to_html(index=False, escape=False,classes="display", table_id = "table_id",border=0, columns=["Name","RA (2000)", "DEC (2000)", "GCVS", "Discovery Name", "No. of spectra", "First spectrum", "Last spectrum", "Days since last"])
sym_info = '<p class="card-text">Number of stars: '+str(len(home))+'\n</p><p class="card-text">Number of spectra: '+str(home.astype({'No. of spectra': 'int32'})["No. of spectra"].sum(axis=0))+'\n</p><p class="card-text">Last update: '+str(Time.now().isot)[0:10]+', '+str(Time.now().isot)[11:16]+'</p>\n<br><br>\n<a href="observers.html" class="btn btn-secondary">Observers</a>\n        <a href="observatories.html" class="btn btn-secondary">Observatories</a>\n\n      </div>\n    </div>\n  </div>\n\n  <div class="col-sm-6">\n    <div class="card">\n      <div class="card-body">\n        <h5 class="card-title">Stars of special interest</h5>\n<p class="card-text" style="margin-bottom:2.358cm;">Novae in outburst: '+outb_string
home_top = open("../website_source/home_top_novae.txt", "r").read()
home_footer = open("../website_source/home_footer_novae.txt", "r").read()
home_info = open("../website_source/home_info_novae.txt", "r").read()
home_website = open("../novae.html", "w")
home_website.write(home_top+sym_info+home_info+home_table+home_footer)
home_website.close()

last_update = open("../data/last_update.txt", "w")
last_update.write(str(Time.now().unix))
last_update.close()

#dwarf_novae

# df = pd.read_csv('../data/all_spectra.csv', delimiter=";")
# df = df.rename(columns={"date": "Date", "time": "Time (UT)", "jd": "JD 24..", "observer": "Observer", "site": "Site", "resolution": "Resolution", "lambda_min": "&lambda;<sub>min</sub>","lambda_max": "&lambda;<sub>max</sub>", "comment": "Comments"}).replace(np.nan, '', regex=True)
# home = pd.read_csv('../data/dwarf_novae.csv', delimiter=";")
# home = home.rename(columns={"ra": "RA (2000)", "dec": "DEC (2000)"}).replace(np.nan, '', regex=True)

# last_update = float(open("../data/last_update.txt", "r").read())
# intro = open("../website_source/navigation_dwarf_novae.txt", "r").read()
# footer = open("../website_source/footer_dwarf_novae.txt", "r").read()
# first_spec = []
# last_spec = []
# since_last_spec = []
# num_spec = []
# name_website = []
# for dwarf_nova in dwarf_novae["star_name_string"]: ## why symbiotic_stars in novae part ?
#     if dwarf_nova in symbiotic_stars["star_name_string"]:
#         first_spec.append(str(np.min(Time(all_spectra[all_spectra["star_name_string"]==dwarf_nova]["date"])).value[:10]))
#         last_spec.append(str(np.max(Time(all_spectra[all_spectra["star_name_string"]==dwarf_nova]["date"])).value[:10]))
#         since_last_spec.append('<script>var date1, date2;date1 = new Date();date2 = new Date( "'+str(np.max(Time(all_spectra[all_spectra["star_name_string"]==dwarf_nova]["date"])).value[:10])+' 00:00:00" );var res = Math.abs(date1 - date2) / 1000;var days = Math.floor(res / 86400);document.write(days);</script>')
#         num_spec.append(str(len(all_spectra[all_spectra["star_name_string"]==dwarf_nova])))
#         name_website.append('<a href="'+dwarf_nova+'.html">'+dwarf_novae["name"][dwarf_novae["star_name_string"]==dwarf_nova][0]+'</a>')
#     else:
#         try:
#             first_spec.append(str(np.min(Time(all_spectra[all_spectra["star_name_string"]==dwarf_nova]["date"])).value[:10]))
#             last_spec.append(str(np.max(Time(all_spectra[all_spectra["star_name_string"]==dwarf_nova]["date"])).value[:10]))
#             since_last_spec.append('<script>var date1, date2;date1 = new Date();date2 = new Date( "'+str(np.max(Time(all_spectra[all_spectra["star_name_string"]==dwarf_nova]["date"])).value[:10])+' 00:00:00" );var res = Math.abs(date1 - date2) / 1000;var days = Math.floor(res / 86400);document.write(days);</script>')
#             num_spec.append(str(len(all_spectra[all_spectra["star_name_string"]==dwarf_nova])))
#             name_website.append('<a href="'+dwarf_nova+'.html">'+dwarf_novae["name"][dwarf_novae["star_name_string"]==dwarf_nova][0]+'</a>')
#             if np.max(all_spectra[all_spectra["star_name_string"]==dwarf_nova]["last_update"]) > 0: #last_update-10000000
#                 star_intro = open("../website_source/"+dwarf_nova+".txt", "r").read()
#                 star_info = '<div class="col-sm-6">\n    <div class="card">\n      <div class="card-body">\n\n        <p class="card-text">Number of spectra:   '+str(len(all_spectra[all_spectra["star_name_string"]==dwarf_nova]))+'</p>\n<p class="card-text">First spectrum:   '+str(np.min(Time(all_spectra[all_spectra["star_name_string"]==dwarf_nova]["date"])).value[:10])+'</p>\n<p class="card-text">Last spectrum:   '+str(np.max(Time(all_spectra[all_spectra["star_name_string"]==dwarf_nova]["date"])).value[:10])+'</p>\n<br>\n<p class="card-text" style="margin-top:0.36cm;"><i>send spectra to francoismathieu.teyssier [at] gmail.com & arasdatabase [at] gmail.com</i></p>\n      </div>\n    </div>\n  </div>\n\n</div>\n\n<br><style>table {text-align: center;}table thead th {text-align: center;}</style>'
#                 current = df[df["star_name_string"]==dwarf_nova]
#                 campaign_string=[]
#                 try:
#                     if campaigns["campaign_type"][np.array(campaigns["star_name_string"][:]).tolist().index(dwarf_nova)] == "Ongoing campaign":
#                         campaign_type = "bg-success"
#                     elif campaigns["campaign_type"][np.array(campaigns["star_name_string"][:]).tolist().index(dwarf_nova)] == "Dwarf Nova in outburst":
#                         campaign_type = "bg-danger"
#                     else:
#                         campaign_type = "bg-dark"
#                     try:
#                         campaign_string = '<div class="card text-white '+campaign_type+' mb-3">\n<div class="card-body">\n<h5 class="card-title">'+campaigns["campaign_type"][np.array(campaigns["star_name_string"][:]).tolist().index(dwarf_nova)]+'</h5>\n<p class="card-text"><p class="card-text">'+campaigns["campaign_text"][np.array(campaigns["star_name_string"][:]).tolist().index(dwarf_nova)]+'</p>\n</div>\n</div>\n<br>\n\n'
#                     except:
#                         campaign_string = '<div class="card text-white '+campaign_type+' mb-3">\n<div class="card-body">\n<h5 class="card-title">'+campaigns["campaign_type"][np.array(campaigns["star_name_string"][:]).tolist().index(dwarf_nova)]+'</h5></div>\n</div>\n<br>\n\n'

#                 except:
#                     campaign_string=''
#                 if dwarf_nova !="chcyg": ## à supprimer
#                     campaign_string = campaign_string + '<a href="archives/'+dwarf_nova+'.zip" class="btn btn-secondary">Download all spectra as *.zip file (' + str(round(os.stat('../archives/'+nova+'.zip').st_size/(1048576),1))+' MB)</a>'
#                 else:
#                     current_year_string = str(np.max(Time(all_spectra[all_spectra["star_name_string"]==dwarf_nova]["date"])).value[:4])
#                     campaign_string = campaign_string + '<a href="archives/'+dwarf_nova+'1.zip" class="btn btn-secondary">Download 2011-2018 spectra as *.zip file (' + str(round(os.stat('../archives/'+nova+'1.zip').st_size/(1048576),1))+' MB)</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+'<a href="archives/'+nova+'2.zip" class="btn btn-secondary">Download 2019-'+current_year_string +' spectra as *.zip file (' + str(round(os.stat('../archives/'+dwarf_nova+'2.zip').st_size/(1048576),1))+' MB)</a><br><br>'

#                 file_string = []
#                 image_string = []
#                 resolution_string = []
#                 wavelength_string = []
#                 for i in range(len(current)):
#                     file_string.append('<a href="spectra/'+current.iloc[i]["file"]+'" download target="_blank"><svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-download" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M.5 8a.5.5 0 0 1 .5.5V12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8.5a.5.5 0 0 1 1 0V12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V8.5A.5.5 0 0 1 .5 8z"/><path fill-rule="evenodd" d="M5 7.5a.5.5 0 0 1 .707 0L8 9.793 10.293 7.5a.5.5 0 1 1 .707.707l-2.646 2.647a.5.5 0 0 1-.708 0L5 8.207A.5.5 0 0 1 5 7.5z"/><path fill-rule="evenodd" d="M8 1a.5.5 0 0 1 .5.5v8a.5.5 0 0 1-1 0v-8A.5.5 0 0 1 8 1z"/></svg></a>')
#                     image_string.append('<a href="figures/'+current.iloc[i]["image"]+'" target="_blank"><svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-eye" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8zM1.173 8a13.134 13.134 0 0 0 1.66 2.043C4.12 11.332 5.88 12.5 8 12.5c2.12 0 3.879-1.168 5.168-2.457A13.134 13.134 0 0 0 14.828 8a13.133 13.133 0 0 0-1.66-2.043C11.879 4.668 10.119 3.5 8 3.5c-2.12 0-3.879 1.168-5.168 2.457A13.133 13.133 0 0 0 1.172 8z"/><path fill-rule="evenodd" d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0z"/></svg></a>')
#                     if current.iloc[i]["Resolution"] < 500:
#                         resolution_string.append('')
#                     elif current.iloc[i]["Resolution"] < 900:
#                         resolution_string.append('<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>')
#                     elif current.iloc[i]["Resolution"] < 1800:
#                         resolution_string.append('<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>')
#                     elif current.iloc[i]["Resolution"] < 4500:
#                         resolution_string.append('<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>')
#                     elif current.iloc[i]["Resolution"] < 9000:
#                         resolution_string.append('<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>')
#                     else:
#                         resolution_string.append('<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#007bff" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>')
#                     wavelength_string_temp = ''
#                     if current.iloc[i]["&lambda;<sub>min</sub>"] < 3600:
#                         wavelength_string_temp = wavelength_string_temp + '<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#A74AC7" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>'
#                     if current.iloc[i]["&lambda;<sub>min</sub>"] < 4100 and current.iloc[i]["&lambda;<sub>max</sub>"] > 4120:
#                         wavelength_string_temp = wavelength_string_temp + '<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#151B8D" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>'
#                     if current.iloc[i]["&lambda;<sub>min</sub>"] < 4670 and current.iloc[i]["&lambda;<sub>max</sub>"] >4680:
#                         wavelength_string_temp = wavelength_string_temp + '<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#4AA02C" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>'
#                     if current.iloc[i]["&lambda;<sub>min</sub>"] < 5870 and current.iloc[i]["&lambda;<sub>max</sub>"] > 5880:
#                         wavelength_string_temp = wavelength_string_temp + '<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#EAC117" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>'
#                     if current.iloc[i]["&lambda;<sub>min</sub>"] < 6550 and current.iloc[i]["&lambda;<sub>max</sub>"] > 6570:
#                         wavelength_string_temp = wavelength_string_temp + '<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#E42217" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>'
#                     if current.iloc[i]["&lambda;<sub>max</sub>"] >7500:
#                         wavelength_string_temp = wavelength_string_temp + '<svg xmlns="http://www.w3.org/2000/svg" width="5" height="16" fill="#8C001A" class="bi bi-square-fill" viewBox="1 0 5 16"><path d="M0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V2z"/></svg>'
#                     wavelength_string.append(wavelength_string_temp)

#                 current["File"] = file_string
#                 current["Preview"] = image_string
#                 current['<div style="display:none;">Resolution</div>'] = resolution_string
#                 current['<div style="display:none;"Wavelength</div>'] = wavelength_string

#                 table = current.to_html(index=False, escape=False,classes="display", table_id = "table_id",border=0, columns=["Date","Time (UT)","JD 24..","Observer","Site","Resolution",'<div style="display:none;">Resolution</div>',"&lambda;<sub>min</sub>","&lambda;<sub>max</sub>",'<div style="display:none;"Wavelength</div>',"File","Preview","Comments"])
#                 website = open("../"+dwarf_nova+".html", "w")
#                 try:
#                     website.write(intro+"\n"+star_intro+star_info+campaign_string+"\n"+table+footer)
#                 except:
#                     website.write(intro+"\n"+star_intro+star_info+"\n"+table+footer)
#                 website.close()
#         except:
#             print("")
#             first_spec.append(str("-"))
#             last_spec.append(str("-"))
#             since_last_spec.append(str("-"))
#             num_spec.append(str(0))
#             name_website.append(dwarf_novae["name"][dwarf_novae["star_name_string"]==dwarf_nova][0])

# home["First spectrum"] = first_spec
# home["Last spectrum"] = last_spec
# home["No. of spectra"] = num_spec
# home["Days since last"] = since_last_spec
# home["Name"] = name_website
# camp_string = []
# surv_string = []
# outb_string = []
# for stars in campaigns["star_name_string"]:
#     if campaigns["campaign_type"][campaigns["star_name_string"]==stars] == "Dwarf Nova in outburst":
#         try:
#             outb_string = outb_string + ", " + dwarf_novae["name"][dwarf_novae["star_name_string"]==stars][0]
#         except:
#             outb_string = dwarf_novae["name"][dwarf_novae["star_name_string"]==stars][0]

# if not camp_string:
#     camp_string = ""
# if not surv_string:
#     surv_string = ""
# if not outb_string:
#     outb_string = ""
# home_table = home.to_html(index=False, escape=False,classes="display", table_id = "table_id",border=0, columns=["Name","RA (2000)", "DEC (2000)", "No. of spectra", "First spectrum", "Last spectrum", "Days since last"])
# sym_info = '<p class="card-text">Number of stars: '+str(len(home))+'\n</p><p class="card-text">Number of spectra: '+str(home.astype({'No. of spectra': 'int32'})["No. of spectra"].sum(axis=0))+'\n</p><p class="card-text">Last update: '+str(Time.now().isot)[0:10]+', '+str(Time.now().isot)[11:16]+'</p>\n<br><br>\n<a href="observers.html" class="btn btn-secondary">Observers</a>\n        <a href="observatories.html" class="btn btn-secondary">Observatories</a>\n\n      </div>\n    </div>\n  </div>\n\n  <div class="col-sm-6">\n    <div class="card">\n      <div class="card-body">\n        <h5 class="card-title">Stars of special interest</h5>\n<p class="card-text" style="margin-bottom:2.358cm;">Dwarf novae in outburst: '+outb_string
# home_top = open("../website_source/home_top_dwarf_novae.txt", "r").read()
# home_footer = open("../website_source/home_footer_dwarf_novae.txt", "r").read()
# home_info = open("../website_source/home_info_dwarf_novae.txt", "r").read()
# home_website = open("../dwarf_novae.html", "w")
# home_website.write(home_top+sym_info+home_info+home_table+home_footer)
# home_website.close()

# last_update = open("../data/last_update.txt", "w")
# last_update.write(str(Time.now().unix))
# last_update.close()
