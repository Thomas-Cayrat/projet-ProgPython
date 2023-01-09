#classe Auteur qui répertorie les auteurs et leurs nombre de documents
class Author:
#constructeur de la classe Auteur
    def __init__(self, name, ndoc, production):
        self.name = name
        self.ndoc = ndoc
        self.production = production
        
#méthode qui ajoute un document au dictionnaire production et incrémente le ndoc associé
    def add(self, document):
        self.production[self.ndoc] = document
        self.ndoc += 1
        
#méthode qui renvoie un print propre
    def __str__(self):
        return("Le nom de l'auteur est : " + self.name + " il a écrit " + ndoc + " articles.")
