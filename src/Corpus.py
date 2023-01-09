import Author
import regex
import re
import pickle
import pandas as pd

# Un singleton est un patron de conception qui permet
# de s'assurer qu'une classe de dispose que d'une et une seule instance.
def singleton(class_):
    instances = {} #initialisation de instances
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

#classe Corpus qui répertorie les différentes données composant le corpus
@singleton #pattern singleton
class Corpus:
#constructeur de la classe Corpus
    def __init__(self, nom, authors, id2doc, ndoc, naut):
        self.nom = nom
        self.authors = authors
        self.id2doc = id2doc
        self.ndoc = ndoc
        self.naut = naut

#méthode qui trie les dates et les affiches par ordre décroissant
    def trie_date(self, nombre_doc):
        datesdico = []
        for i in range(len(self.id2doc)):
            datesdico.append(self.id2doc[i].date)
        datessorted = sorted(datesdico, reverse=True)
        for i in range(nombre_doc):
            print(datessorted[i])

#méthode qui trie les titres par ordre alphabétique puis les affiche
    def trie_titre(self, nombre_doc):
        titlesdico = []
        for i in range(len(self.id2doc)):
            titlesdico.append(self.id2doc[i].titre)
        titlessorted = sorted(titlesdico)
        for i in range(nombre_doc):
            print(titlessorted[i])
            
#méthode qui sauvegarde au format csv le corpus
    def save(self, df, nom):
        df.to_csv(nom + ".csv", sep="\t", encoding="utf-8")
        
#méthode qui ouvre et retourne corpus à l'aide de pickle
    def load(cls, file_path):
        with open(file_path,'rb') as f:
            return pickle.load(f)

#méthode qui transforme la recherche en regex puis applique la recherche à l'ensemble du texte
    def search(self, keyword):
        #concaténer l'intégralité des chaînes des documents du corpus
        txt = ""
        for i in range(len(self.id2doc)):
            txt += self.id2doc[i].texte
        #compiler l'expression régulière
        regex = re.compile(keyword)
        #diviser la chaîne concaténée en phrases
        sentences = txt.split('.')
        #créer une liste de phrases qui contiennent le mot-clé
        keyword_sentences = []
        for sentence in sentences:
            if regex.search(sentence):
                keyword_sentences.append(sentence)
        return keyword_sentences

#méthode qui découpe et rtourne les phrases trouvé avec le mot, et le contexte de droit et le contexte de gauche
    def concorde(self, keyword, size):
        #concaténer l'intégralité des chaînes des documents du corpus
        txt = ""
        for i in range(len(self.id2doc)):
            txt += self.id2doc[i].texte
        phrases = txt.split('.')
        tab = []
        for phrase in phrases:
            if regex.search(keyword, phrase):
                start = regex.search(keyword, phrase).start()
                end = regex.search(keyword, phrase).end()
                left_context = phrase[max(0, start - size):start]
                right_context = phrase[end:end + size]
                tab.append([keyword, left_context, right_context, phrase])
        return pd.DataFrame(tab, columns=['Expression', 'Contexte gauche', 'Contexte droit', 'Phrase'])

#méthode qui nettoie le text en remplacant les "\n" en " " et en mettant en minuscule
    def nettoyer_texte(self):
        #concaténer l'intégralité des chaînes des documents du corpus
        txt = ''
        for i in range(len(self.id2doc)):
            txt += self.id2doc[i].texte
        result = txt.lower()
        regex = re.compile('\n')
        result = regex.sub(' ', result)
        print(result)
        return result
