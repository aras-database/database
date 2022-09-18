from glob import glob
automatic = 1
print("Checking keywords.")
import aras_check_keywords_automatic
print("ok")
if (len(glob('../temporary/missing/observer/' + '*.fit'))+len(glob('../temporary/missing/site/' + '*.fit'))+len(glob('../temporary/missing/object/' + '*.fit'))+len(glob('../temporary/missing/observer/' + '*.fits'))+len(glob('../temporary/missing/site/' + '*.fits'))+len(glob('../temporary/missing/object/' + '*.fits')))>0:
    print("Problems with keywords detected. Input needed.")
    import aras_add_missing_keywords

if len(glob('../temporary/' + '*.csv'))>0:
    print("New keywords detected. Input needed.")
    import aras_new_keywords

print("Renaming the files.")
import aras_rename

print("Creating figures.")
import aras_create_figures

print("Writing entries to table.")
import aras_update_tables

print("Updating zip archives.")
import aras_update_archives

comments_anw = 2
while comments_anw == 2:
    #confirmation = input(str("Would you like to add comments to newly added spectra?  (Y/N)   "))
    confirmation = "N"
    if confirmation == "Y" or confirmation == "y":
        comments_anw=1
        print("Do not forget to run aras_update_websites.py after including comments to all_spectra.csv file!")
    elif confirmation == "N" or confirmation == "n":
        comments_anw=0
        print("Updating websites.")
        import aras_update_websites
        print("All done. You can commit to GitHub now.")
    else:
        print("Answer with Y or N.")
      
#Temporary T CrB campaign
import Monitoring_TCrB