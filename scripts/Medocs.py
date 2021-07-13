import os
import xlwings as xw



os.chdir(r'C:\Users\franc\OneDrive\Documents\Pau') 
data = []
n = -1
Fichier = []

indice = []
Produit = []
Aspect= []
Ingredient1 = []
Ingredient2 = []
Ingredient3 = []
Ingredinent4 = []
textetab= []
wb = xw.Book('Results.xlsx') 
shtName = '1'
sht = wb.sheets[shtName]




with open("ListeMedocs.txt", "r") as f:     #ouvre le fichier txt
       
       
       # lines = f.readlines() 
       for line in f:  
           n = n+1               #lit les lignes du fichier
                            #sauvegarde la ligne initiale - Travil sur Line
           Line0 = line
           Line = line.lower() 
           
           print(n)      

           Line = Line.replace(' de ',' ')      #ménage des mots superfux
           Line = Line.replace("d'",'')
           Line = Line.replace("l'",'')
           Line = Line.replace("?",'')
           Line = Line.replace(" en ",' ')
           Line = Line.replace(",",'')
           Line = Line.replace("seche",'')
           Line = Line.replace("double",'')#Hg
           Line = Line.replace("doux",'')#Hg
           
           
           mots = Line.split()                  #découpe la ligne en mots
           indice.append(n)
           Aspect.append('')
           if 'sirop'in mots:
               Aspect.insert(n,"sirop")
           if 'eau'in mots:
               Aspect.insert(n,"eau")
           if 'suc'in mots:
               Aspect.insert(n,"suc")
           if 'huille'in mots or "huile" in mots:
               Aspect.insert(n,"huile")
           if 'pommade'in mots:
               Aspect.insert(n,"pommade")
           if 'onguent'in mots:
               Aspect.insert(n,"onguent")
           if 'emplatre'in mots:
               Aspect.insert(n,"emplatre")
           if 'gomme'in mots:
               Aspect.insert(n,"gomme") 
           if 'extrait'in mots:
               Aspect.insert(n,"extrait")
           if 'sel' in mots:
               Aspect.insert(n,"sel")        
           if 'terre' in mots:
               Aspect.insert(n,"solide")             
           if 'concasse' in mots:
               Aspect.insert(n,"solide")         
           if 'entiere' in mots:
               Aspect.insert(n,"solide")    
           if 'poudre' in mots:
               Aspect.insert(n,"poudre")
           if 'pillule' in mots or 'pillules' in mots or 'pilules' in mots:
               Aspect.insert(n,"pillules") 
           if 'creme' in mots:
               Aspect.insert(n,"creme") 
           if 'vin' in mots:
               Aspect.insert(n,"liquide")     
           if 'prã©cipitã© ' in mots:
               Aspect.insert(n,"solide")       
           if 'liqueur' in mots:
               Aspect.insert(n,"liqueur")          
           if 'broyã©es' in mots:
               Aspect.insert(n,"solide")   
           if 'concassã©' in mots:
               Aspect.insert(n,"solide")    
           if 'jus' in mots:
               Aspect.insert(n,"jus")   
           if 'fleurs' in mots:
               Aspect.insert(n,"végétaux")   
           if 'follicules' in mots:
               Aspect.insert(n,"végétaux")   
           if 'mauve' in mots:
               Aspect.insert(n,"végétaux") 
           if 'racines' in mots or 'racine' in mots:
               Aspect.insert(n,"végétaux") 
           if 'camphre' in mots or 'racine' in mots:
               Aspect.insert(n,"huile")    
            
           sht.range(n+1,1).value =str(n)
           sht.range(n+1,2).value = Line0
           sht.range(n+1,3).value = Line
           sht.range(n+1,4).value = Aspect[n]
           
           
          

# with open (fichier,'w') as f:
#     fichier_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#     fichier_writer.writerow(Line)


