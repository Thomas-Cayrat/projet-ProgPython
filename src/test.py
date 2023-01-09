import unittest


class TestDocument(unittest.TestCase):
    def setUp(self):
        # Création d'un objet Document
        self.doc = Document('Titre1', 'Auteur1', '2022-01-01', 'http://url1', 'Type1')

    def test_titre(self):
        # Vérification de l'attribut titre
        self.assertEqual(self.doc.titre, 'Titre1')

    def test_auteur(self):
        # Vérification de l'attribut auteur
        self.assertEqual(self.doc.auteur, 'Auteur1')

    def test_date(self):
        # Vérification de l'attribut date
        self.assertEqual(self.doc.date, '2022-01-01')

    def test_url(self):
        # Vérification de l'attribut url
        self.assertEqual(self.doc.url, 'http://url1')

    def test_type(self):
        # Vérification de l'attribut type
        self.assertEqual(self.doc.type, 'Type1')

    def test_texte(self):
        # Vérification de l'attribut texte
        self.assertEqual(self.doc.texte, 'vide')

    def test_affichage(self):
        # Vérification de la méthode affichage
        self.assertIsNone(self.doc.affichage())

    def test_getType(self):
        # Vérification de la méthode getType
        self.assertEqual(self.doc.getType(), 'Type1')

    def test_str(self):
        # Vérification de la méthode __str__
        self.assertEqual(str(self.doc), 'Le titre du doc est : Titre1')

class TestRedditDocument(unittest.TestCase):
    def test_getNbCommentaire(self):
        doc = RedditDocument("titre", "auteur", "date", "url", "texte")
        self.assertEqual(doc.getNbCommentaire(), 0)

    def test_setNbCommentaire(self):
        doc = RedditDocument("titre", "auteur", "date", "url", "texte")
        doc.setNbCommentaire(10)
        self.assertEqual(doc.getNbCommentaire(), 10)

    def test_getType(self):
        doc = RedditDocument("titre", "auteur", "date", "url", "texte")
        self.assertEqual(doc.getType(), "Reddit")

    def test_str_representation(self):
        doc = RedditDocument("titre", "auteur", "date", "url", "texte")
        self.assertEqual(str(doc), "Reddit Document object : titre et 0")

if __name__ == '__main__':
    unittest.main()


class TestArxivDocument(unittest.TestCase):
    def setUp(self):
        # Création d'un objet ArxivDocument
        self.arxiv_doc = ArxivDocument('Titre2', ['Auteur2', 'Auteur3'], '2022-02-01', 'http://url2', 'Type2')

    def test_liste_auteurs(self):
        # Vérification de l'attribut listeAuteur
        self.assertEqual(self.arxiv_doc.listeAuteur, ['Auteur2', 'Auteur3'])

    def test_get_caracteristique(self):
        # Vérification de la méthode getCaracteristique
        self.assertEqual(self.arxiv_doc.getCaracteristique(), ['Auteur2', 'Auteur3'])


class TestDocumentGenerator(unittest.TestCase):
    def test_factory_returns_ArxivDocument(self):
        doc = DocumentGenerator.factory("titre", "auteur", "date", "url", "texte", "Arxiv")
        self.assertIsInstance(doc, ArxivDocument)
        self.assertEqual(doc.getType(), "Arxiv")

    def test_factory_returns_RedditDocument(self):
        doc = DocumentGenerator.factory("titre", "auteur", "date", "url", "texte", "Reddit")
        self.assertIsInstance(doc, RedditDocument)
        self.assertEqual(doc.getType(), "Reddit")

    def test_factory_raises_error_for_invalid_type(self):
        with self.assertRaises(AssertionError) as context:
            DocumentGenerator.factory("titre", "auteur", "date", "url", "texte", "invalid_type")
        self.assertEqual(str(context.exception), "Erreur : invalid_type")

if __name__ == '__main__':
    unittest.main()
