#classe qui génère des Documents de type Reddit ou Arxiv suivant le type du Document en question
class DocumentGenerator:
    @staticmethod #factory pattern
    def factory(titre, auteur, date, url, texte, type):
        if type == "Arxiv" : return ArxivDocument(titre, auteur, date, url, type, texte)
        if type == "Reddit" : return RedditDocument(titre, auteur, date, url, type, texte)
        assert 0, "Erreur : " + type #si le type entré est inconnu

#classe Document, classe mère de RedditDocument et ArxivDocument
class Document:
#constructeur de la classe Document
    def __init__(self, titre, auteur, date, url, type, texte="vide"):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.type = type
        self.texte = texte

#méthode qui affiche correctement les différents attributs du Document en question
    def affichage(self):
        print("Titre: " + self.titre)
        print("Auteur: " + self.auteur)
        print("Date: " + self.date)
        print("URL: " + self.url)
        print("Type: " + self.type)
        print("Texte: " + self.texte)

#méthode qui retourne le type du Document en question
    def getType(self):
        return self.type

#méthode qui retourne un print propre
    def __str__(self):
        return("Le titre du doc est : " + self.titre)
    
#classe RedditDocument, classe fille de Document, correspondant aux articles provenant de Reddit
class RedditDocument(Document):
#constructeur de la classe RedditDocument
    def __init__(self, titre, auteur, date, url, texte, type="Reddit"):
        #constructeur de Document ou Document.__init(self,...,...,...)
        super().__init__(titre, auteur, date, url, texte, type)
        self.nbCommentaire = 0 # nouvelle variable propre à Reddit

#méthode qui retourne les différentes caractéristiques 
    def getCaracteristique(self):
        return self.nbCommentaire

#méthode qui retourne le nombre de commentaire 
    def getNbCommentaire(self):
        return self.nbCommentaire

#méthode qui initialise le nombre de commentaire
    def setNbCommentaire(self,nbCommentaire):
        self.nbCommentaire = nbCommentaire
        
#méthode qui retourne le type du RedditDocument
    def getType(self):
        return self.type
    
#méthode qui retourne un print propre
    def __str__(self):
        return "Reddit Document object : " + self.titre +" et "+ str(self.getCaracteristique())

#classe ArxivDocument, classe fille de Document, correspondant aux articles provenant de Arxiv
class ArxivDocument(Document):
#constructeur de la classe ArxivDocument
    def __init__(self, titre, auteur, date, url, texte, type="Arxiv"):
        # constructeur de Document ou Document.__init(self,...,...,...)
        super().__init__(titre, auteur, date, url, texte, type)
        self.listeAuteur = auteur  # nouvelle variable propre à Arxiv
        
#méthode qui retourne les différentes caractéristiques
    def getCaracteristique(self):
        return self.listeAuteur
    
#méthode qui retourne la liste des auteurs
    def getListeAutheurs(self):
        return self.listeAuteur
    
#méthode qui initialise la liste des auteurs
    def setListeAutheurs(self, listeAuteur):
        self.listeAuteur = listeAuteur
        
#méthode qui retourne le type du ArxivDocument
    def getType(self):
        return self.type
    
#méthode qui retourne un print propre
    def __str__(self):
        return "Arxiv Document object : " + self.titre + " et " + str(self.getCaracteristique())
