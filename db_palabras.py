import nltk
from nltk.corpus import stopwords

# Descarga el corpus de palabras comunes en español
nltk.download('stopwords')

# Obtiene la lista de palabras comunes en español
palabras_comunes_espanol = stopwords.words('spanish')

# Imprime las primeras 200 palabras como ejemplo

with open('palabras4.txt','w',encoding="UTF-8") as file:
    for i in palabras_comunes_espanol:
        #if len(i)==4: 
        file.write(i+"\n")

