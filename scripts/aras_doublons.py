from astropy.io import ascii
import pandas as pd





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

nb =0

# df = pd.read_csv('../data/all_spectra.csv', delimiter=";")
# df1 =df.sort_values(by=["star_name_string","jd"])
# print(df1)

df1 = pd.read_csv('../data/all_spectra_sort.csv', delimiter=",")





nLines = len(df1)
print(nLines)
for n in range(1,nLines):
    if df1.jd[n]==df1.jd[n-1]:
    # if df1.file[n]==df1.file[n-1]:
    # if df1.date[n]==df1.date[n-1] and df1.time[n]==df1.time[n-1]:    
        nb = nb+1
        print(nb)
        print(n)
        print(df1.file[n-1])
        print(df1.file[n])
        
     
df1.to_csv('../data/all_spectra_sort.csv',index=False)