# delete duplicates (criterions: objname, jd, observer)
# and sort all_spectra by objname and jd
# fmt - 2022-01-21

import pandas as pd


# Spectra

df = pd.read_csv(r'C:\Users\franc\OneDrive\Documents\GitHub\database\data/all_spectra.csv', delimiter=";")
n0=len(df.index)
df =df.sort_values(by=["star_name_string","jd"])
df = df.drop_duplicates(subset=["star_name_string", "jd","observer"], keep='last')
df.to_csv('../data/all_spectra.csv',index=False,sep = ';')
n1=len(df.index)
print("nb doublons removed = ",n0-n1)

# Symbiotics table




    