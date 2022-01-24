# -*- coding: utf-8 -*-

"""Description.

Module auxiliaire pour l'importation des données JSON, le nettoyage et la prise en charge des valeurs manquantes. On obtient une base de données propres prête à l'emploie pour le machine learning.

"""

from serde import deserialize, serialize
import re
from serde.json import from_json, to_json
from dataclasses import dataclass
import json
import pandas as pd
import numpy as np


@serialize
@deserialize
@dataclass
class Annonce:
    Prix: str
    Processeur: str
    RAM: int
    Résolution: str
    Poids: float
    Autonomie: str
    Stockage: int
    Systeme_exploitation: str
    Marque: str
    Taille: str
    Coeur: int
    USB: str
    HDMI: str
    Note: str


def donnees_cdiscount() -> pd.DataFrame:
    """ Fonction permettant de creer un premier dataframe pour CDiscount en important le json et 
        en appliquant des premières modifications de base.
    """

    with open("data.json", "rb") as fp:
        data = json.load(fp)

    df = pd.read_json("data.json")
    df["Processeur"] = df["Processeur"] + "" + df["CPU"]
    df["Interfaces"] = (
        df["Interfaces"] + "" + df["Caméra"] + df["Lecteur de carte mémoire"]
    )

    df.drop(
        [
            "Indice de réparabilité",
            "Grand écran",
            "Son",
            "Lecteur de carte mémoire",
            "Caméra",
            "Capacité",
            "CPU",
        ],
        axis=1,
        inplace=True,
    )

    df.rename(
        columns={
            "Durée de fonctionnement": "Autonomie",
            "Stockage principal": "Stockage",
            "Système d'exploitation": "Systeme_exploitation",
            "Taille écran": "Taille",
            "Nombre de coeurs": "Coeurs",
        },
        inplace=True,
    )

    df = df.assign(b_USB="test")
    df = df.assign(b_HDMI="test")
    df = df.assign(Resolution="test")

    return df


def amazon_prix_modif(df: pd.DataFrame) -> pd.DataFrame:
    """ Nettoyage de la colonne prix Amazon pour s'adapter au dataframe CDiscount
    """
    df_amazon = df
    df_amazon.Prix = df_amazon.Prix.str.replace("€", "")
    df_amazon.Prix = df_amazon.Prix.str.replace(" ", "")
    df_amazon.Prix = df_amazon.Prix.str.replace(",", ".", regex=True)
    df_amazon.Prix = df_amazon.Prix.str.replace("\u202f", "")
    return df_amazon


def donnees_amazon() -> pd.DataFrame:
    """ Fonction permettant de creer un premier dataframe pour Amazon en important le json et 
        en appliquant des premières modifications de base.
    """
    with open("data_amazon.json", "rb") as fp:
        data_amazon = json.load(fp)

    df_amazon = pd.read_json("data_amazon.json")

    df_amazon.rename(
        columns={
            "Type de processeur": "Processeur",
            "Taille de la mémoire vive": "RAM",
            "Résolution de l'écran": "Résolution",
            "Taille du disque dur": "Stockage",
            "Durée de vie moyenne (en heures)": "Autonomie",
            "Poids du produit": "Poids",
            "Nombre de ports USB": "b_USB",
            "Taille de l'écran": "Taille",
            "Logiciels inclus": "Logiciels",
            "Système d'exploitation": "Systeme_exploitation",
            "Nombre de coeurs": "Coeurs",
            "Nombre de ports HDMI": "b_HDMI",
            "Marque du processeur": "CPU_name",
        },
        inplace=True,
    )

    df_amazon["Interfaces"] = (
        df_amazon["Logiciels"]
        + df_amazon["Type de connecteur"]
        + df_amazon["Interface du matériel informatique"]
    )
    df_amazon["Processeur"] = df_amazon["Processeur"] + df_amazon["CPU_name"]

    df_amazon.drop(
        [
            "CPU_name",
            "GPU",
            "séries",
            "Interface du matériel informatique",
            "couleur",
            "Nom de modèle",
            "Entrée de l'interface humaine",
            "Fabricant de CPU",
            "Logiciels",
            "Type de connecteur",
        ],
        axis=1,
        inplace=True,
    )

    return df_amazon


def regroupement_donnees(df_1: pd.DataFrame, df_2: pd.DataFrame) -> pd.DataFrame:
    """ Regroupement des deux dataframes
    """
    data = pd.concat([df_1, df_2])
    data = pd.DataFrame(data)
    data = data.reset_index()
    return data


###### Debut Nettoyage ###################


def nettoyage_note(df: pd.DataFrame) -> pd.DataFrame:
    """ Nettoyage de la colonne "Note"
    """
    data = df
    data.Note.str.lower()
    data.Note = data.Note.str.replace(" ", "", regex=True)
    data.Note = data.Note.str.replace(",", ".", regex=True)
    data.Note = data.Note.str.replace("sur5\xa0étoiles", "", regex=True)
    return data


def nettoyage_RAM(df: pd.DataFrame) -> pd.DataFrame:
    """ Nettoyage de la colonne "RAM"
    """
    data = df
    data.RAM = data.RAM.str.replace(" ", "")

    liste_RAM = ["512", "256", "128", "64", "16"]
    for element in liste_RAM:
        data.loc[data.RAM.str.contains(element) == True, "RAM"] = f",{element},Go"

    liste_RAM_2 = ["8Go|8GB|^8$", "6Go|6GB", "4Go|4GB|4MB|^4$", "2Go|2GB"]
    i = 8
    for element_ram in liste_RAM_2:
        motif = re.compile(element_ram)
        data.RAM.str.contains(motif)
        data.loc[data.RAM.str.contains(motif) == True, "RAM"] = f"{i}Go"
        i = i - 2

    indexNames = data[data["RAM"] == "(lamémoirefournieestsoudée)"].index
    data.drop(indexNames, inplace=True)
    data.RAM = data.RAM.str.replace(",", "")

    data.RAM = data.RAM.str.replace("Go", "")

    return data


def nettoyage_resolution(df: pd.DataFrame) -> pd.DataFrame:
    """ Nettoyage de la colonne "Résolution"
    """
    data = df
    data.Résolution = data.Résolution + data["Resolution"]
    data.Résolution = data.Résolution.str.replace(" ", "")

    data.Résolution = data.Résolution.str.replace(
        ".*1366.768.*", "1366x768", regex=True
    )
    data.Résolution = data.Résolution.str.replace(
        ".*2280.1920*", "2280x1920", regex=True
    )
    data.Résolution = data.Résolution.str.replace(
        ".*1920.1080.*", "1920x1080", regex=True
    )
    data.Résolution = data.Résolution.str.replace(
        ".*1600.900.*", "1600x900", regex=True
    )
    data.Résolution = data.Résolution.str.replace(
        ".*1440.900.*", "1440x900", regex=True
    )
    data.Résolution = data.Résolution.str.replace(
        ".*2560.1600.*", "2560x1600", regex=True
    )
    data.Résolution = data.Résolution.str.replace(
        ".*2256.1504.*", "2256x1504", regex=True
    )
    data.Résolution = data.Résolution.str.replace(
        ".*3072.1920.*", "3072x1920", regex=True
    )
    data.Résolution = data.Résolution.str.replace(
        ".*3000.2000.*", "3000x2000", regex=True
    )
    data.Résolution = data.Résolution.str.replace(
        ".*1536.1024.*", "1536x1024", regex=True
    )
    data.Résolution = data.Résolution.str.replace(
        ".*1200.1920.*", "1200x1920", regex=True
    )
    data.Résolution = data.Résolution.str.replace(
        ".*2280x1920.*", "2280x1920", regex=True
    )
    data.Résolution = data.Résolution.str.replace(
        ".*1280.800.*", "1280x800", regex=True
    )
    data.Résolution = data.Résolution.str.replace(
        ".*1024.600.*", "1024x600", regex=True
    )
    data.Résolution = data.Résolution.str.replace(
        ".*3840.2160.*", "3840x2160", regex=True
    )
    data.Résolution = data.Résolution.str.replace(
        ".*2560.1440.*", "2560x1440", regex=True
    )
    data.Résolution = data.Résolution.str.replace(
        ".*2160.1440.*", "2160x1440", regex=True
    )
    data.Résolution = data.Résolution.str.replace(
        ".*2880.1800.*", "2880x1800", regex=True
    )
    data.Résolution = data.Résolution.str.replace(
        ".*1280.1040.*", "1280x1040", regex=True
    )
    data.Résolution = data.Résolution.str.replace(
        ".*3840.2400.*", "3840x2400", regex=True
    )
    data.Résolution = data.Résolution.str.replace(
        ".*2048.1536.*", "2048.1536", regex=True
    )
    data.Résolution = data.Résolution.str.replace(
        ".*1920.1200.*", "1920x1200", regex=True
    )
    data.Résolution = data.Résolution.str.replace(
        "None2736x1824", "2736x1824", regex=True
    )
    data.Résolution = data.Résolution.str.replace(
        ".*1920.1280.*", "1920x1280", regex=True
    )
    data.Résolution = data.Résolution.str.replace(
        ".*2496.1664.*", "2496x1664", regex=True
    )
    data.Résolution = data.Résolution.str.replace(".*720p*", "1366x768", regex=True)
    data.Résolution = data.Résolution.str.replace(".*1080p.*", "1920x1080", regex=True)
    data.Résolution = data.Résolution.str.replace(".*WQHD.*", "2560x1440", regex=True)
    data.Résolution = data.Résolution.str.replace(
        "1366x768HDReadyLinesPerInch", "1368x768", regex=True
    )
    data.Résolution = data.Résolution.str.replace(
        "None4KUltraHDPixels", "3840x2160", regex=True
    )

    data.Résolution = data.Résolution.str.replace(".*None.*", "None", regex=True)

    indexNames = data[data["Résolution"] == "4200dpitest"].index
    data.drop(indexNames, inplace=True)
    indexNames = data[data["Résolution"] == "2,5Ktest"].index
    data.drop(indexNames, inplace=True)
    data.drop(["Resolution"], axis=1, inplace=True)

    return data


def nettoyage_poids(df: pd.DataFrame) -> pd.DataFrame:
    """ Nettoyage de la colonne "Poids"
    """
    data = df
    data.Poids = data.Poids.str.replace("Kilogrammes", "")
    data.Poids = data.Poids.str.replace("KG", "")
    data.Poids = data.Poids.str.replace("Kg", "")
    data.Poids = data.Poids.str.replace("kg", "")
    data.Poids = data.Poids.str.replace("Grammes", "g")
    data.Poids = data.Poids.str.replace(".*1500g", "1.500", regex=True)
    data.Poids = data.Poids.str.replace("0\.01 ", "1.000", regex=True)
    data.Poids = data.Poids.str.replace("0\.02 ", "1.200", regex=True)
    data.Poids = data.Poids.str.replace("g", "")
    data.Poids = data.Poids.str.replace(" ", "")
    data.Poids = data.Poids.str.replace(",", ".")

    motif = re.compile("Livres")
    data.loc[data.Poids.str.contains(motif) == True, "Poids"] = "1.400"

    indexNames = data[data["Poids"] == "302.2*217*16mm"].index
    data.drop(indexNames, inplace=True)
    indexNames = data[data["Poids"] == "en0"].index
    data.drop(indexNames, inplace=True)

    return data


def poids_echelle(df: pd.DataFrame) -> pd.DataFrame:
    """ Mise à l'échelle pour que toutes les données soient en kg
    """
    data = df
    data.Poids = data.Poids.str.replace("990", "0.990")
    data.Poids = data.Poids.str.replace("999", "0.999")
    data.Poids = data.Poids.str.replace("980?", "0.980", regex=True)
    data.Poids = data.Poids.str.replace("553", "0.553")
    data.Poids = data.Poids.str.replace("544", "0.544")
    data.Poids = data.Poids.str.replace("989.*", "0.989", regex=True)
    data.Poids = data.Poids.str.replace("870", "0.870")
    data.Poids = data.Poids.str.replace("906", "0.906")
    data.Poids = data.Poids.str.replace("2410", "2.410")
    data.Poids = data.Poids.str.replace("1750", "1.750")
    data.Poids = data.Poids.str.replace("1500", "1.5")
    data.Poids = data.Poids.str.replace("1740", "1.740")
    data.Poids = data.Poids.str.replace("1300", "1.300")
    data.Poids = data.Poids.str.replace("1400", "1.400")
    data.Poids = data.Poids.str.replace("1420", "1.420")
    data.Poids = data.Poids.str.replace("1920", "1.920")
    data.Poids = data.Poids.str.replace("2600", "2.600")
    data.Poids = data.Poids.str.replace("3500", "3.500")
    data.Poids = data.Poids.str.replace("1050", "1.050")
    data.Poids = data.Poids.str.replace("1850", "1.850")
    data.Poids = data.Poids.str.replace("3319", "3.319")
    data.Poids = data.Poids.str.replace("2350", "2.350")
    data.Poids = data.Poids.str.replace("2460", "2.460")
    data.Poids = data.Poids.str.replace("2000", "2.0")
    data.Poids = data.Poids.str.replace("1340", "1.340")
    data.Poids = data.Poids.str.replace("3200", "3.2")
    data.Poids = data.Poids.str.replace("1980", "1.980")
    data.Poids = data.Poids.str.replace("1700", "1.7")
    data.Poids = data.Poids.str.replace("820", "0.820")
    data.Poids = data.Poids.str.replace("2.0.980", "2.980", regex=True)
    data.Poids = data.Poids.str.replace("10.980", "1.980", regex=True)
    data.Poids = data.Poids.str.replace("1.0.980", "0.980", regex=True)

    return data


def nettoyage_stockage(df: pd.DataFrame) -> pd.DataFrame:
    """ Nettoyage de la variable "Stockage"
    """
    data = df
    data.Stockage = data.Stockage.str.replace(" ", "")
    data.Stockage = data.Stockage.str.replace("1To", "1000Go")
    data.Stockage = data.Stockage.str.replace("2To", "2000Go")
    data.Stockage = data.Stockage.str.replace("1\.024To", "1024Go", regex=True)

    liste_stockage = [
        "2000",
        "1024",
        "1000",
        "756",
        "512",
        "500",
        "480",
        "256",
        "250",
        "128",
        "64",
        "16",
    ]
    for element in liste_stockage:
        data.loc[
            data.Stockage.str.contains(element) == True, "Stockage"
        ] = f"{element}Go"

    motif = re.compile("^320$")
    data.loc[data.Stockage.str.contains(motif) == True, "Stockage"] = f",320,Go"
    motif = re.compile("^32G.*")
    data.loc[data.Stockage.str.contains(motif) == True, "Stockage"] = f"32Go"
    data.Stockage = data.Stockage.str.replace("Go", "")
    data.Stockage = data.Stockage.str.replace("SSD", "32")

    return data


def nettoyage_autonomie(df: pd.DataFrame) -> pd.DataFrame:
    """ Nettoyage de la variable "Autonomie"
    """
    data = df
    liste_autonomie = ["Jusqu'à", "heures", "ans", "[(]", "[)]", "heures"]
    for element in liste_autonomie:
        data.Autonomie = data.Autonomie.str.replace(element, "", regex=True)
    return data


def nettoyage_systeme(df: pd.DataFrame) -> pd.DataFrame:
    """ Nettoyage de la variable "Systeme_exploitation"
    """
    data = df
    data.loc[
        data.Systeme_exploitation.str.contains("Chrome") == True, "Systeme_exploitation"
    ] = f"ChromeOS"
    data.loc[
        data.Systeme_exploitation.str.contains("Mac") == True, "Systeme_exploitation"
    ] = f"MacOS"
    data.loc[
        data.Systeme_exploitation.str.contains("mac") == True, "Systeme_exploitation"
    ] = f"MacOS"
    data.loc[
        data.Systeme_exploitation.str.contains("7") == True, "Systeme_exploitation"
    ] = f"Windows 7 Pro"
    data.loc[
        data.Systeme_exploitation.str.contains("DOS") == True, "Systeme_exploitation"
    ] = f"DOS"

    data.Systeme_exploitation = data.Systeme_exploitation.str.replace("français", "")
    data.Systeme_exploitation = data.Systeme_exploitation.str.replace(
        "Enterprise", "Pro"
    )

    motif = re.compile("10 Home|10 home|10 H|10H")
    data.loc[
        data.Systeme_exploitation.str.contains(motif) == True, "Systeme_exploitation"
    ] = f"Windows 10 Home"

    motif = re.compile("10s|10 S|S mode")
    data.loc[
        data.Systeme_exploitation.str.contains(motif) == True, "Systeme_exploitation"
    ] = f"Windows 10s"

    motif = re.compile("11 Home")
    data.loc[
        data.Systeme_exploitation.str.contains(motif) == True, "Systeme_exploitation"
    ] = f"Windows 11 Home"

    motif = re.compile("10 Pro| 10 pro|IoT")
    data.loc[
        data.Systeme_exploitation.str.contains(motif) == True, "Systeme_exploitation"
    ] = f"Windows 11 Pro"

    motif = re.compile("11 Pro")
    data.loc[
        data.Systeme_exploitation.str.contains(motif) == True, "Systeme_exploitation"
    ] = f"Windows 11 Pro"

    motif = re.compile("Familiale|Famille|10 F|10F")
    data.loc[
        data.Systeme_exploitation.str.contains(motif) == True, "Systeme_exploitation"
    ] = f"Windows 10 Famille"

    motif = re.compile("El Capitan")
    data.loc[
        data.Systeme_exploitation.str.contains(motif) == True, "Systeme_exploitation"
    ] = f"MacOS"

    motif = re.compile("Aucun système d'exploitation fourni|Sans OS|SANS OS")
    data.loc[
        data.Systeme_exploitation.str.contains(motif) == True, "Systeme_exploitation"
    ] = f"Aucun"

    motif = re.compile("Android")
    data.loc[
        data.Systeme_exploitation.str.contains(motif) == True, "Systeme_exploitation"
    ] = f"Android"

    motif = re.compile("None|Win10|Ordissimo|Logiciels")
    data.loc[
        data.Systeme_exploitation.str.contains(motif) == True, "Systeme_exploitation"
    ] = f"Windows 10 Home"

    motif = re.compile("^Windows 10$|^Windows$")
    data.loc[
        data.Systeme_exploitation.str.contains(motif) == True, "Systeme_exploitation"
    ] = f"Windows 10 Home"

    motif = re.compile("^Windows 11$")
    data.loc[
        data.Systeme_exploitation.str.contains(motif) == True, "Systeme_exploitation"
    ] = f"Windows 11 Home"

    motif = re.compile("11")
    data.loc[
        data.Systeme_exploitation.str.contains(motif) == True,"Systeme_exploitation"]= f"Windows 11"

    motif = re.compile("10")
    data.loc[
        data.Systeme_exploitation.str.contains(motif) == True,"Systeme_exploitation"]= f"Windows 10"

    return data


def nettoyage_marque(df: pd.DataFrame) -> pd.DataFrame:
    """ Nettoyage de la variable "Marque", si la marque est présente moins de 10 fois,
        on la classe comme "AUTRES".
    """
    data = df
    data.Marque = data.Marque.str.upper()

    liste_marque = [
        "NONE|N.A|AUCUNE",
        "APPLE",
        "ASUS|ASUSTEK",
        "SAMSUNG",
        "LG",
        "MICROSOFT",
        "LENOVO",
    ]
    liste_marque_2 = ["None", "APPLE", "ASUS", "SAMSUNG", "LG", "MICROSOFT", "LENOVO"]
    i = 0
    for element in liste_marque:
        element_2 = liste_marque_2[i]
        motif = re.compile(element)
        data.loc[data.Marque.str.contains(motif) == True, "Marque"] = f"{element_2}"
        i = i + 1

    indexNames = data[data["Marque"] == "DU PROCESSEUR\u200eINTEL"].index
    data.drop(indexNames, inplace=True)
    indexNames = data[data["Marque"] == "None"].index
    data.drop(indexNames, inplace=True)

    marque_low = data.Marque.value_counts().loc[lambda x: x < 10]
    marque_low = marque_low.index.tolist()

    for element in marque_low:
        data.loc[data.Marque == element, "Marque"] = "AUTRES"

    return data


def nettoyage_taille(df: pd.DataFrame) -> pd.DataFrame:
    """ Nettoyage de la variable "Taille écran"
    """
    data = df
    liste_taille = [
        '".*',
        "Pouces",
        "inch",
        "pouces",
        "Centimètres",
        "Décimètres",
        "Centièmes.*",
        "Pieds",
        "avec.*",
        " ",
    ]

    for element in liste_taille:
        data.Taille = data.Taille.str.replace(element, "", regex=True)

    data.Taille = data.Taille.str.replace(",", ".", regex=True)

    indexNames = data[data["Taille"] == "1xSATA/NVMe"].index
    data.drop(indexNames, inplace=True)

    return data


def nettoyage_processeur(df: pd.DataFrame) -> pd.DataFrame:
    """ Nettoyage de la variable Processeur
    """
    data = df
    data.Processeur = data.Processeur.str.replace(" ", "")

    liste_intel = ["i3", "i5", "i7", "i9", "Gemini"]
    for element in liste_intel:
        motif = re.compile(element)
        data.loc[
            data.Processeur.str.contains(motif) == True, "Processeur"
        ] = f"Intel Core {element}"

    liste_AMD = ["A4", "A9", "A12"]
    for element in liste_AMD:
        motif = re.compile(element)
        data.loc[
            data.Processeur.str.contains(motif) == True, "Processeur"
        ] = f"AMD {element}"

    motif = re.compile("Atom")
    data.loc[data.Processeur.str.contains(motif) == True, "Processeur"] = f"Intel Atom"

    motif = re.compile("Celeron|NoneIntel")
    data.loc[
        data.Processeur.str.contains(motif) == True, "Processeur"
    ] = f"Intel Celeron"

    motif = re.compile("Pentium")
    data.loc[
        data.Processeur.str.contains(motif) == True, "Processeur"
    ] = f"Intel Pentium"

    motif = re.compile("Ryzen|RSeries|NoneAMD")
    data.loc[data.Processeur.str.contains(motif) == True, "Processeur"] = f"AMD Ryzen"

    motif = re.compile("Athlon")
    data.loc[data.Processeur.str.contains(motif) == True, "Processeur"] = f"AMD Athlon"

    motif = re.compile("Radeon")
    data.loc[data.Processeur.str.contains(motif) == True, "Processeur"] = f"AMD Radeon"

    motif = re.compile("Xeon|E-Series")
    data.loc[data.Processeur.str.contains(motif) == True, "Processeur"] = f"Intel Xeon"

    motif = re.compile("N[0-9]{3}")
    data.loc[
        data.Processeur.str.contains(motif) == True, "Processeur"
    ] = f"Intel Celeron"

    motif = re.compile("Cortex")
    data.loc[data.Processeur.str.contains(motif) == True, "Processeur"] = f"Cortex A8"

    motif = re.compile("MediaTek|NoneMediaTek|NoneMediatek")
    data.loc[data.Processeur.str.contains(motif) == True, "Processeur"] = f"MediaTek"

    motif = re.compile("Snapdragon")
    data.loc[data.Processeur.str.contains(motif) == True, "Processeur"] = f"Snapdragon"

    motif = re.compile("3000")
    data.loc[data.Processeur.str.contains(motif) == True, "Processeur"] = f"AMD 3000"

    motif = re.compile("M1")
    data.loc[data.Processeur.str.contains(motif) == True, "Processeur"] = f"Apple M1"

    motif = re.compile("I5|IntelUHDGraphics|IntelIrisXeGraphics")
    data.loc[
        data.Processeur.str.contains(motif) == True, "Processeur"
    ] = f"Intel Core i5"

    motif = re.compile("5Y10Processor")
    data.loc[
        data.Processeur.str.contains(motif) == True, "Processeur"
    ] = f"Intel Core i5"

    motif = re.compile("I3|2Duo|m3|IntelHDGraphics")
    data.loc[
        data.Processeur.str.contains(motif) == True, "Processeur"
    ] = f"Intel Core i3"

    motif = re.compile("NoneNone|nan")
    data.loc[data.Processeur.str.contains(motif) == True, "Processeur"] = f"None"

    return data


def nettoyage_coeurs(df: pd.DataFrame) -> pd.DataFrame:
    """ Nettoyage de la variable "Nombre de coeurs"
    """
    data = df
    liste_coeurs = ["2|Double", "4|Quad|Quadri|None|5", "6", "8", "10"]
    i = 2
    for element in liste_coeurs:
        motif = re.compile(element)
        data.loc[data.Coeurs.str.contains(motif) == True, "Coeurs"] = f"{i}"
        i = i + 2

    return data


def nettoyage_interfaces(df: pd.DataFrame) -> pd.DataFrame:
    """ Création des variables Bluetooth, USB, HDMI, sortie_audio, Caméra et Cart_sd
        Prend True si présence de l'élement, False sinon
    """
    data = df
    data.Interfaces = data.Interfaces + data["b_USB"] + data["b_HDMI"]
    data.Interfaces = data.Interfaces.str.lower()

    liste_interface = [
        "bluetooth",
        "usb|\u200e",
        "hdmi|.*1$",
        "casque|microphone",
        "camera|webcam|oui",
        "sd",
    ]
    liste_interface_2 = [
        "Bluetooth",
        "USB",
        "HDMI",
        "Sortie_audio",
        "Caméra",
        "Carte_sd",
    ]
    i = 0
    for element in liste_interface:
        element_2 = liste_interface_2[i]
        motif = re.compile(element)
        data[element_2] = data.Interfaces.str.contains(motif)
        i = i + 1

    data.drop(["Interfaces", "b_USB", "b_HDMI"], axis=1, inplace=True)

    return data


def nettoyage_complet(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fonction appellant toutes les nettoyages colonnes par colonnes et renvoie un dataframe propre avant
    gestion des NA.
    """
    data = df

    data = nettoyage_note(data)
    data = nettoyage_RAM(data)
    data = nettoyage_resolution(data)
    data = nettoyage_poids(data)
    data = poids_echelle(data)
    data = nettoyage_stockage(data)
    data = nettoyage_autonomie(data)
    data = nettoyage_systeme(data)
    data = nettoyage_marque(data)
    data = nettoyage_taille(data)
    data = nettoyage_processeur(data)
    data = nettoyage_coeurs(data)
    data = nettoyage_interfaces(data)

    data = data.drop_duplicates(
        subset=None, keep="first", inplace=False, ignore_index=False
    )

    return data


##################### NA ###########################


def na_processeur(df: pd.DataFrame) -> pd.DataFrame:
    """ On donne la valeur la plus courante aux Na en fonction de la marque, car souvent une corrélation
        entre la marque et le processeur utilisé
    """
    data = df

    data.loc[
        (data.Processeur == "None") & (data.Marque == "APPLE"), "Processeur"
    ] = "Apple M1"
    data.loc[
        (data.Processeur == "None") & (data.Marque == "THOMSON"), "Processeur"
    ] = "Intel Celeron"
    data.loc[
        (data.Processeur == "None") & (data.Marque == "SIMBANS"), "Processeur"
    ] = "Intel Atom"
    data.loc[
        (data.Processeur == "None") & (data.Marque == "LENOVO"), "Processeur"
    ] = "Intel Core i5"

    data = data.replace("None", np.NaN)
    # data.Processeur = data.Processeur.fillna(data.Processeur.mode()[0])

    indexNames = data[data.Processeur.isnull()].index
    data.drop(indexNames, inplace=True)

    return data


def na_remplacement(df: pd.DataFrame) -> pd.DataFrame:
    """ Remplacement des NA par la médiane lorsque l'écart max entre min et max est pas trop grand
    """
    data = df

    median_RAM = data["RAM"].median()
    data["RAM"].fillna(median_RAM, inplace=True)

    median_Stockage = data["Stockage"].median()
    data["Stockage"].fillna(median_Stockage, inplace=True)

    median_Poids = data["Poids"].median()
    data["Poids"].fillna(median_Poids, inplace=True)

    median_Taille = data["Taille"].median()
    data["Taille"].fillna(median_Taille, inplace=True)

    data = data.drop(columns={"Autonomie", "Note"})

    data.RAM = data.RAM.replace(median_RAM, f"{median_RAM}")
    data.Stockage = data.Stockage.replace(median_Stockage, f"{median_Stockage}")

    data.RAM = data.RAM.str.replace(".0", "", regex=True)
    data.RAM = data.RAM.astype(int)
    motif = re.compile("\.")
    data.loc[data.Stockage.str.contains(motif) == True, "Stockage"] = "256"
    data.Stockage = data.Stockage.astype(int)

    return data


def na_final(df: pd.DataFrame) -> pd.DataFrame:
    """ Fonction qui permet de gerer les NA
    """
    data = df
    data = na_processeur(data)
    data = na_remplacement(data)

    return data


def data_categorie(df: pd.DataFrame) -> pd.DataFrame:
    """ Fonction permettant de changer la colonne prix en conne catégorielle pour la prédiction
    """
    data = df
    data.Prix = data.Prix.astype(float)
    data.loc[data.Prix < 250, "Prix"] = 1.0
    data.loc[(data.Prix >= 250) & (data.Prix < 400), "Prix"] = 2.0
    data.loc[(data.Prix >= 400) & (data.Prix < 600), "Prix"] = 3.0
    data.loc[(data.Prix >= 600) & (data.Prix < 800), "Prix"] = 4.0
    data.loc[(data.Prix >= 800) & (data.Prix < 1150), "Prix"] = 5.0
    data.loc[data.Prix >= 1150, "Prix"] = 6.0

    data.Prix = data.Prix.replace(1.0, "<250")
    data.Prix = data.Prix.replace(2.0, "Entre 250 et 400")
    data.Prix = data.Prix.replace(3.0, "Entre 400 et 600")
    data.Prix = data.Prix.replace(4.0, "Entre 600 et 800")
    data.Prix = data.Prix.replace(5.0, "Entre 800 et 1150")
    data.Prix = data.Prix.replace(6.0, ">1150")

    return data
