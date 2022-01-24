# -*- coding: utf-8 -*-

"""Description.

Module auxiliaire pour l'obtention des données à partir des backups html. On va parser les differents codes 
html des backups pour chaque annonce et stocker les données dans un JSON pour chaque site.

"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as BS
from unidecode import unidecode
from typing import List, Dict
import re
import os
import json

########### CDiscount #################################
########################################################

elements_description = [
    "Processeur",
    "RAM",
    "Résolution",
    "Stockage principal",
    "Durée de fonctionnement",
    "Système d'exploitation",
    "Poids",
]

elements_table = [
    "Marque",
    "CPU",
    "Nombre de coeurs",
    "Indice de réparabilité",
    "Grand écran",
    "Caméra",
    "Son",
    "Lecteur de carte mémoire",
    "Capacité",
    "Interfaces",
    "Taille écran",
]

elements_table_2 = [
    "Processeur",
    "RAM",
    "Résolution",
    "Stockage principal",
    "Durée de fonctionnement",
    "Système d'exploitation",
    "Poids",
    "Marque",
    "CPU",
    "Nombre de coeurs",
    "Indice de réparabilité",
    "Grand écran",
    "Caméra",
    "Son",
    "Lecteur de carte mémoire",
    "Capacité",
    "Interfaces",
    "Taille écran",
]


def test_description(description: BS) -> str:
    """ Fonction permettant de déterminer si nous avons un premier tableau avec des
    informations nécéssaires ou non. Renvoi oui ou non
    """
    test = description.get_text() == "Les points forts :"
    if test == True:
        on_continue = "oui"
    else:
        on_continue = "non"
    return on_continue


def donnees_description(
    elements_description: list, description: BS, caractéristiques: dict
) -> dict:
    """ Fonction permettant de récupérer les élements de la liste descrpition et leurs valeurs.
     Renvoi un dictionnaire rempli avec l'élément et sa valeur.
    """
    lignes = description.parent.find_all("li")

    liste = []
    for ligne in lignes:
        liste.append(ligne.get_text(strip=True))

    for element in elements_description:
        str_match = list(filter(lambda x: element in x, liste))
        if not str_match:
            caractéristiques[element] = "None"
        else:
            caractéristiques[element] = str_match[0][len(element) + 3 :]
    return caractéristiques


def note(soupe: BS, caractéristiques: dict) -> dict:
    """ Fonction permettant de récupérer la note associée à l'article
    Rempli le dictionnaire contenant les informations liés à l'article en ajoutant la note.
    """
    try:
        note = soupe.find_all(attrs={"itemprop": ["ratingValue"]})[0].get_text(
            strip=True
        )
        caractéristiques["Note"] = note
    except:
        caractéristiques["Note"] = "None"


def prix(soupe: BS, caractéristiques: dict) -> dict:
    """ Fonction permettant de récupérer le prix associé à l'article
    Rempli le dictionnaire contenant les informations liés à l'article en ajoutant le prix.
    """
    prix = soupe.find_all(attrs={"itemprop": ["price"]})[0]
    prix = list(prix)
    caractéristiques["Prix"] = prix[0]
    return caractéristiques


def donnees_table(soupe: BS, elements_table: list, caractéristiques: dict) -> dict:
    """ Fonction permettant de récupérer les informations qui sont dans la table de description
    de l'article en fin de page. Récupère des élements différent en fonctions du
    résultat du test de description. Rempli le dictionnaire avec les nouveaux éléments.
    """
    liste_table = []

    table = soupe.find_all(name="table")[0]
    lignes_table = table.tbody.find_all("tr")
    header, *lignes_table = lignes_table

    for ligne_table in lignes_table:
        liste_table.append(ligne_table.get_text(strip=True))

    for element_table in elements_table:
        if element_table == "Taille écran":
            regex = re.compile(r"Type[0-9]")
            str_match = [z for z in liste_table if regex.match(z)]
            if not str_match:
                caractéristiques[element_table] = "None"
            else:
                caractéristiques[element_table] = str_match[0][len("Type") :]
        else:
            str_match = list(filter(lambda x: element_table in x, liste_table))
            if not str_match:
                caractéristiques[element_table] = "None"
            else:
                caractéristiques[element_table] = str_match[0][len(element_table) :]

    return caractéristiques


def parsing(
    elements_description: list, elements_table: list, elements_table_2: list
) -> List[Dict[str, str]]:
    """ Fonction permettant de récupérer le backup html, de récupérer les informations voulues
    et de les ranger dans une liste de dictionnaire. Chaque dictionnaire équivaut à un article.
    """
    donnees = []
    for page in range(1, 20):
        for article in range(1, 42):
            caractéristiques = {}
            path = f"C:/Users/Guillaume CORRE/Machine_learning/Projet/Page_{page}"
            with open(path + f"/article_{article}.html", "r", encoding="utf8") as fichier:
                code = fichier.read()
                soupe = BS(code, "lxml")
                description = soupe.find_all(attrs={"class": ["fpBlocTitle"]})[0]
                test_description(description)

                if (test_description(description)) == "oui":
                    prix(soupe, caractéristiques)
                    note(soupe, caractéristiques)
                    donnees_description(
                        elements_description, description, caractéristiques
                    )
                    donnees_table(soupe, elements_table, caractéristiques)
                    donnees.append(caractéristiques)

                else:
                    prix(soupe, caractéristiques)
                    note(soupe, caractéristiques)
                    donnees_table(soupe, elements_table_2, caractéristiques)
                    donnees.append(caractéristiques)

    with open("data.json", "w", encoding="utf8") as fp:
        json.dump(donnees, fp)
        
    return donnees


# with open('data.json', 'w', encoding="utf8") as fp:
#    json.dump(parsing(elements_description, elements_table, elements_table_2), fp)


########### Amazon #################################
########################################################

elements_detail = [
    "Type de processeur",
    "Taille de la mémoire vive",
    "Résolution de l'écran",
    "Taille du disque dur",
    "Durée de vie moyenne (en heures)",
    "Système d'exploitation",
    "Poids du produit",
    "Marque",
    "séries",
    "Marque du processeur",
    "Nombre de coeurs",
    "GPU",
    "Logiciels inclus",
    "Interface du matériel informatique",
    "Taille de l'écran",
    "couleur",
    "Nombre de ports HDMI",
    "Nombre de ports USB",
    "Type de connecteur",
    "Resolution",
]

elements_detail_apple = [
    "Fabricant de CPU",
    "Taille de la mémoire vive",
    "Résolution de l'écran",
    "Taille du disque dur",
    "Durée de vie moyenne (en heures)",
    "Système d'exploitation",
    "Poids du produit",
    "Marque",
    "Nom de modèle",
    "Marque du processeur",
    "Nombre de coeurs",
    "GPU",
    "Logiciels inclus",
    "Entrée de l'interface humaine",
    "Taille de l'écran",
    "couleur",
    "Nombre de ports HDMI",
    "Nombre de ports USB",
    "Type de connecteur",
    "Resolution",
]


def donnees_detail(
    soupe: BS,
    element_detail: list,
    element_detail_apple: list,
    caractéristiques_amazon: dict,
) -> dict:
    """ Fonction permettant de récupérer les informations qui sont dans la table de description
    de l'article en fin de page. Récupère des informations différente en fonction que 
    l'article soit apple ou non.Rempli le dictionnaire avec les nouveaux éléments.
    """
    detail = soupe.find_all(attrs={"id": ["productDetails_techSpec_section_1"]})

    if len(detail) == 0:
        detail_apple = soupe.find_all(attrs={"class": ["a-normal a-spacing-micro"]})[0]

        lignes_detail_apple = detail_apple.tbody.find_all("tr")
        liste_detail_apple = []
        for ligne_detail_apple in lignes_detail_apple:
            liste_detail_apple.append(ligne_detail_apple.get_text(strip=True))

        for element_detail in elements_detail_apple:
            str_match = list(filter(lambda x: element_detail in x, liste_detail_apple))
            if not str_match:
                caractéristiques_amazon[element_detail] = "None"
            else:
                caractéristiques_amazon[element_detail] = str_match[0][
                    len(element_detail) :
                ]
    else:
        detail = detail[0]
        lignes_detail = detail.tbody.find_all("tr")

        liste_detail = []
        for ligne_detail in lignes_detail:
            liste_detail.append(ligne_detail.get_text(strip=True))

        for element_detail in elements_detail:
            str_match = list(filter(lambda x: element_detail in x, liste_detail))
            if not str_match:
                caractéristiques_amazon[element_detail] = "None"
            else:
                caractéristiques_amazon[element_detail] = str_match[0][
                    len(element_detail) + 1 :
                ]


def prix_amazon(soupe: BS, caractéristiques_amazon: dict) -> dict:
    """ Fonction permettant de récupérer le prix de l'article et le stock dans le dictionnaire
    """
    prix_amazon = soupe.find_all(attrs={"class": ["a-offscreen"]})[0]
    prix_amazon = list(prix_amazon)
    caractéristiques_amazon["Prix"] = prix_amazon[0]
    return caractéristiques_amazon


def note_amazon(soupe: BS, caractéristiques_amazon: dict) -> dict:
    """ Fonction permettant de récupérer la note de l'article et la stock dans le dictionnaire
    """
    try:
        note_amazon = soupe.find_all(attrs={"data-hook": ["average-star-rating"]})[
            0
        ].get_text(strip=True)
        caractéristiques_amazon["Note"] = note_amazon
    except:
        caractéristiques_amazon["Note"] = "None"


def parsing_amazon(
    element_detail: list, element_detail_apple: list
) -> List[Dict[str, str]]:
    """ Fonction permettant de récupérer les informations de tous les backup html amazon
     et renvoie une liste de dictionnaire.
    """
    donnees_amazon = []
    for page in range(1, 8):
        if page == 7:
            taille = range(1, 15)
        else:
            taille = range(1, 41)
        for article in taille:
            caractéristiques_amazon = {}
            path = f"C:/Users/Guillaume CORRE/Machine_learning/Projet/Pageamazon_{page}"
            with open(path + f"/article_{article}.html", "r", encoding="utf8") as fichier:
                code = fichier.read()
                soupe = BS(code, "lxml")
                prix_amazon(soupe, caractéristiques_amazon)
                note_amazon(soupe, caractéristiques_amazon)
                donnees_detail(
                    soupe,
                    elements_detail,
                    element_detail_apple,
                    caractéristiques_amazon,
                )
                donnees_amazon.append(caractéristiques_amazon)

    with open("data_amazon.json", "w", encoding="utf8") as fp:
        json.dump(donnees_amazon, fp)
        
    return donnees_amazon


# with open('data_amazon.json', 'w', encoding="utf8") as fp:
#    json.dump(parsing_amazon(elements_detail, elements_detail_apple), fp)
