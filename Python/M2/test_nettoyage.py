"""Description.
Tests de la bibliothèque nettoyage_donnees.

All tests passed
"""
import pandas as pd
import numpy as np

from nettoyage_donnees import (
    amazon_prix_modif,
    regroupement_donnees,
    nettoyage_note,
    nettoyage_RAM,
    nettoyage_resolution,
    nettoyage_poids,
    poids_echelle,
    nettoyage_stockage,
    nettoyage_taille,
    nettoyage_systeme,
    nettoyage_autonomie,
    nettoyage_processeur,
    nettoyage_coeurs,
    na_processeur,
    data_categorie,
)


def test_amazon_prix_modif():
    """Test."""
    entree_1 = pd.DataFrame(["143€"], columns=["Prix"])
    sortie = pd.DataFrame(["143"], columns=["Prix"])
    calculee = amazon_prix_modif(entree_1)
    assert calculee.all().all() == sortie.all().all()


def test_regroupement_donnees():
    """Test."""
    entree_1 = pd.DataFrame([1, 2], columns=["A"])
    entree_2 = pd.DataFrame([3, 4], columns=["A"])
    sortie = pd.DataFrame([(0, 1), (1, 2), (0, 3), (1, 4)], columns=["index", "A"])
    calculee = regroupement_donnees(entree_1, entree_2)
    assert calculee.all().all() == sortie.all().all()


def test_nettoyage_note():
    """Test."""
    entree = pd.DataFrame([" 4", "4,2", "4sur5\xa0étoiles"], columns=["Note"])
    sortie = pd.DataFrame(["4", "4.2", "4"], columns=["Note"])
    calculee = nettoyage_note(entree)
    assert calculee.all().all() == sortie.all().all()


def test_nettoyage_RAM():
    """Test."""
    entree = pd.DataFrame(
        [" 4", "xxh64i", "2Go", "(lamémoirefournieestsoudée)"], columns=["RAM"]
    )
    sortie = pd.DataFrame(["4", "64", "2"], columns=["RAM"])
    calculee = nettoyage_RAM(entree)
    assert calculee.all().all() == sortie.all().all()


def test_nettoyage_resolution():
    """Test."""
    entree = pd.DataFrame(
        [("djdkis1366*768cjikks", "df"), ("WQHD", "kkf"), ("2,5K", "test")],
        columns=["Résolution", "Resolution"],
    )
    sortie = pd.DataFrame(["1366x768", "2560x1440"], columns=["Résolution"])
    calculee = nettoyage_resolution(entree)
    assert calculee.all().all() == sortie.all().all()


def test_nettoyage_poids():
    """Test."""
    entree = pd.DataFrame(
        ["2Kilogrammes", "Livres", "302.2*217*16mm"], columns=["Poids"]
    )
    sortie = pd.DataFrame(["2", "1.400"], columns=["Poids"])
    calculee = nettoyage_poids(entree)
    assert calculee.all().all() == sortie.all().all()


def poids_echelle():
    """Test."""
    entree = pd.DataFrame(["990"], columns=["Poids"])
    sortie = pd.DataFrame(["0.990"], columns=["Poids"])
    calculee = poids_echelle(entree)
    assert calculee.all().all() == sortie.all().all()


def test_nettoyage_Stockage():
    """Test."""
    entree = pd.DataFrame(["1To", "1\.024To", "512", "SSD"], columns=["Stockage"])
    sortie = pd.DataFrame(["1000", "1024", "512", "32"], columns=["Stockage"])
    calculee = nettoyage_stockage(entree)
    assert calculee.all().all() == sortie.all().all()


def test_nettoyage_autonomie():
    """Test."""
    entree = pd.DataFrame(["8heures"], columns=["Autonomie"])
    sortie = pd.DataFrame(["8"], columns=["Autonomie"])
    calculee = nettoyage_autonomie(entree)
    assert calculee.all().all() == sortie.all().all()


def test_nettoyage_taille():
    """Test."""
    entree = pd.DataFrame(["12Pouces", "14,4", "1xSATA/NVMe"], columns=["Taille"])
    sortie = pd.DataFrame(["12", "14.4"], columns=["Taille"])
    calculee = nettoyage_taille(entree)
    assert calculee.all().all() == sortie.all().all()


def test_nettoyage_systeme():
    """Test."""
    entree = pd.DataFrame(["Chrome", "10s"], columns=["Systeme_exploitation"])
    sortie = pd.DataFrame(["12", "Windows 10"], columns=["Systeme_exploitation"])
    calculee = nettoyage_systeme(entree)
    assert calculee.all().all() == sortie.all().all()


def test_nettoyage_processeur():
    """Test."""
    entree = pd.DataFrame(["cpui3", "cpuA12", "Atom"], columns=["Processeur"])
    sortie = pd.DataFrame(
        ["Intel Core i3", "AMD A12", "Intel Atom"], columns=["Processeur"]
    )
    calculee = nettoyage_processeur(entree)
    assert calculee.all().all() == sortie.all().all()


def test_nettoyage_coeurs():
    """Test."""
    entree = pd.DataFrame(["Double"], columns=["Coeurs"])
    sortie = pd.DataFrame(["2"], columns=["Coeurs"])
    calculee = nettoyage_coeurs(entree)
    assert calculee.all().all() == sortie.all().all()


def test_na_processeur():
    """Test."""
    entree = pd.DataFrame(
        [("None", "APPLE", "Oui"), ("Intel Core i5", "ASUS", "None")],
        columns=["Processeur", "Marque", "NA"],
    )
    sortie = pd.DataFrame(
        [("Apple M1", "APPLE", "Oui"), ("Intel Core i5", "ASUS", np.NaN)],
        columns=["Processeur", "Marque", "NA"],
    )
    calculee = na_processeur(entree)
    assert calculee.all().all() == sortie.all().all()


def test_data_categorie():
    """Test."""
    entree = pd.DataFrame(["875.18"], columns=["Prix"])
    sortie = pd.DataFrame(["Entre 800 et 1150"], columns=["Prix"])
    calculee = data_categorie(entree)
    assert calculee.all().all() == sortie.all().all()
