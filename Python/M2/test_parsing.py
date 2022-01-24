"""Description.
Tests de la bibliothèque Parsing.

ALL test passed
"""
from bs4 import BeautifulSoup as BS

from parsing import test_description, donnees_description, note, prix, donnees_table

path = f"C:/Users/Guillaume CORRE/Machine_learning/Projet/Page_1"
with open(path + f"/article_1.html", "r", encoding="utf8") as fichier:
    code = fichier.read()
soupe = BS(code, "lxml")


elements_description = ["Processeur"]
elements_table = ["Marque"]
description = soupe.find_all(attrs={"class": ["fpBlocTitle"]})[0]
caracteristiques = dict()


def test_test_description():
    sortie = "oui"
    calculee = test_description(description)
    assert calculee == sortie


def test_note():
    sortie = {"Note": "3,5"}
    calculee = note(soupe, caracteristiques)
    assert calculee == sortie


def test_prix():
    sortie = {"Note": "3,5", "Prix": "269"}
    calculee = prix(soupe, caracteristiques)
    assert calculee == sortie


def test_donnees_description():
    sortie = {"Note": "3,5", "Prix": "269", "Processeur": "Intel Atom"}
    calculee = donnees_description(elements_description, description, caracteristiques)
    assert calculee == sortie


def test_donnees_table():
    sortie = {
        "Note": "3,5",
        "Prix": "269",
        "Processeur": "Intel Atom",
        "Marque": "THOMSON",
    }
    calculee = donnees_table(soupe, elements_table, caracteristiques)
    assert calculee == sortie
