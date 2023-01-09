#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 08/05/2020
@author: tcayrat and edekkers
"""

#importation des bibliothèques
import praw
import Document
from Document import RedditDocument
from Document import ArxivDocument
import Author
import datetime
import Corpus
import pandas as pd
import urllib.request
import xmltodict
import numpy as np
import pickle

# initialisation des variables
id2Doc = {}
indice = 0
id2Auth = {}


###### partie Reddit
# token reddit pour la connexion
reddit = praw.Reddit(client_id='vshamQJ433InaW81aGu0HQ', client_secret='1dDABCzyPr81NMBvjvGfL4PwYXoStg', user_agent='API')

#intitulée de la recherche
subr = reddit.subreddit('football')
#initialisation des textes Reddit
textes_Reddit = []
#nettoie et envoie les textes Reddit dans un dictionnaire id2Doc
for post in subr.hot(limit=100):
    texte = post.title
    texte = texte.replace("\n", " ")
    textes_Reddit.append(texte)
    dRed = Document.DocumentGenerator.factory(post.title, post.author, datetime.datetime.fromtimestamp(post.created), post.url, post.selftext, "Reddit")
    id2Doc[indice] = dRed
    indice += 1
    # S'il y a plusieurs auteurs
    if not (post.author.name in id2Auth):
        aRed = Author.Author(post.author.name, 0, {})
        aRed.add(dRed)
        id2Auth[post.author.name] = aRed
    if (post.author.name in id2Auth):
        aRed = id2Auth.get(post.author.name)
        aRed.add(dRed)
        id2Auth[post.author.name] = aRed

###### partie Arxiv
textes_Arxiv = []

#recuperation des données de Axiv

#intitulée de la recherche
query = "football"
url = 'http://export.arxiv.org/api/query?search_query=all:' + query + '&start=0&max_results=100'
url_read = urllib.request.urlopen(url).read()

# url_read est un "byte stream" qui a besoin d'être décodé
data =  url_read.decode()

dico = xmltodict.parse(data) #génération du fichier Json
docs = dico['feed']['entry']
#nettoie et envoie les textes Arxiv dans un dictionnaire id2Doc
for d in docs:
    texte = d['title']+ ". " + d['summary']
    texte = texte.replace("\n", " ")
    textes_Arxiv.append(texte)
    dArx = Document.DocumentGenerator.factory(d["title"], d["author"], datetime.datetime.strptime(d["published"], "%Y-%m-%dT%H:%M:%SZ"), d.get('@href'), d["summary"], "Arxiv")
    id2Doc[indice] = dArx
    indice += 1
    #S'il y a plusieurs auteurs
    if len(d["author"]) > 1:
        for auth in d["author"]:
            if not (auth.get("name") in id2Auth):
                aArx = Author.Author(auth.get("name"), 0, {})
                aArx.add(dArx)
                id2Auth[auth.get("name")] = aArx
            if (auth.get("name") in id2Auth):
                aArx = id2Auth.get(auth.get("name"))
                aArx.add(dArx)
                id2Auth[auth.get("name")] = aArx
    else:
        if not (d["author"].get("name") in id2Auth):
            aArx = Author.Author(d["author"].get("name"), 0, {})
            aArx.add(dArx)
            id2Auth[d["author"].get("name")] = aArx
        if (d["author"].get("name") in id2Auth):
            aArx = id2Auth.get(d["author"].get("name"))
            aArx.add(dArx)
            id2Auth[d["author"].get("name")] = aArx

#on concatène les textes de Reddit et Arxiv :
corpus = textes_Reddit + textes_Arxiv

#print la longueur du corpus
print("Longueur du corpus : " + str(len(corpus)))

for doc in corpus:
    # print le nombre de phrases et de mots de chaque Documents dans le Corpus
    print("Nombre de phrases : " + str(len(doc.split("."))))
    print("Nombre de mots : " + str(len(doc.split(" "))))

print(corpus)

# print le type de chaque Documents dans le Corpus
for i in id2Doc :
    print(id2Doc[i].getType())

nb_phrases = [len(doc.split(".")) for doc in corpus]
print("Moyenne du nombre de phrases : " + str(np.mean(nb_phrases)))

nb_mots = [len(doc.split(" ")) for doc in corpus]
print("Moyenne du nombre de mots : " + str(np.mean(nb_mots)))

print("Nombre total de mots dans le corpus : " + str(np.sum(nb_mots)))


corpus_plus100 = [doc for doc in corpus if len(doc)>100]
chaine_unique = " ".join(corpus_plus100)

# ouvre et sauvegarde le corpus dans "out.pkl"
with open("out.pkl", "wb") as f:
    pickle.dump(corpus_plus100, f)
with open("out.pkl", "rb") as f:
    corpus_plus100 = pickle.load(f)


aujourdhui = datetime.datetime.now()
print(aujourdhui)

#création du corpus
c = Corpus.Corpus("Corpus", id2Auth, id2Doc, len(id2Auth), len(id2Doc))
c.trie_date(1) # test unitaire de l'utilisation de la méthode trie_date de Corpus
c.trie_titre(3) # test unitaire de l'utilisation de la méthode trie_titre de Corpus
df = pd.Series(id2Doc).to_frame()
c.save(df, "test")
print(c.concorde('game', 5))
data = c.concorde('game', 5)
data.to_csv('data.csv', index=False, sep=",")
