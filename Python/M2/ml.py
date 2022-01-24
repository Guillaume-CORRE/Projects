# -*- coding: utf-8 -*-

"""Description.

Module auxiliaire pour l'analyse graphique et la mise en place des modèles de machine learning afin
d'obtenir la meileur prédiction.
"""

from serde.json import from_json, to_json
from rich.table import Table
from rich import print
import json
import sklearn
import random
import numpy as np
import pandas as pd
from joblib import load, dump
import time

from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score

from sklearn import preprocessing, utils
from sklearn.preprocessing import MinMaxScaler, PolynomialFeatures, OneHotEncoder
from sklearn.feature_selection import SelectKBest, chi2, mutual_info_classif


from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    recall_score,
    precision_score,
    classification_report,
)

from sklearn.pipeline import Pipeline

from sklearn.dummy import DummyClassifier
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.naive_bayes import GaussianNB, MultinomialNB, CategoricalNB

from sklearn.linear_model import (
    LogisticRegression,
    LinearRegression,
    Ridge,
    Lasso,
    ElasticNet,
)

from sklearn.svm import SVC, SVR
from sklearn.ensemble import (
    RandomForestRegressor,
    RandomForestClassifier,
    GradientBoostingRegressor,
    GradientBoostingClassifier,
    AdaBoostRegressor,
)
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.neural_network import MLPClassifier, MLPRegressor


def import_donnees() -> pd.DataFrame:
    """
    Importation du fichier csv contenant la base de données nettoyée.
    """
    data_cls = pd.read_csv("data_nettoyee_classe.csv")  ##Import base de données
    data_cls = data_cls.replace(
        np.NaN, True
    )  ##Seul les mac manquait des valeurs pour hdmi,camera et usb
    data_cls = data_cls * 1  ##Pour mettre en binaire les true et false
    data_cls = data_cls.drop(columns={"index", "Résolution"})
    return data_cls


def select_features(X_train, y_train, X_test):
    """Fonction permettant de choisir le nombre de features (colonnes) que l'on utilisera pour les
        modèle de Machine learning. Pren en input les donnees test et train pour avoir en output
        les donnees test et train avec le bon nombres de colonnes (features).
    """
    fs = SelectKBest(score_func=chi2, k=40)
    fs.fit(X_train, y_train)
    X_train_fs = fs.transform(X_train)
    X_test_fs = fs.transform(X_test)
    return X_train_fs, X_test_fs, fs


def resume_modeles():
    resume = Table()
    resume.add_column("Score")
    resume.add_column("Modele")
    resume.add_column("Meilleur choix de Paramètres")
    for score, modele in sorted(
        [(score, modele) for modele, score in resultats.items()], key=lambda x: x[0]
    ):
        try:
            mod_str = str(modele.best_estimator_)
            resume.add_row(
                str(score), mod_str[: mod_str.find("(")], str(modele.best_params_)
            )
        except AttributeError:
            mod_str = str(modele)
            resume.add_row(str(score), mod_str[: mod_str.find("(")], "")
    print(resume)


def tab_erreur(score_entrainement: float, score_test: float, accuracy: float):
    """ Fonction qui donne les résultats du meilleur modèle
    """
    Score = Table()
    Score.add_column("")
    Score.add_column("Score entrainement")
    Score.add_column("Score test")
    Score.add_column("Accuracy")
    Score.add_row(
        "Résultats meilleur modèle",
        str(score_entrainement),
        str(score_test),
        str(accuracy),
    )
    print(Score)


def tableau_comparaison(y_true: np.array, y_pred: np.array, nb_obs: int):
    """Fonction permettant de récupérer les valeurs réelles et prédites et de les comparer
        pour déterminer si elles sont équivalentes ou non. Le tout est présenté dans un tableau.
    """
    liste_bon_mauvais = []
    for obs in range(len(y_true)):
        if y_pred[obs] == y_true[obs]:
            liste_bon_mauvais.append("Bon")
        else:
            liste_bon_mauvais.append("Mauvais")

    tab_res = Table()
    tab_res.add_column("Valeurs Réelles")
    tab_res.add_column("Valeurs Prédites")
    tab_res.add_column("Correspondance")
    for obs_2 in range(nb_obs):
        tab_res.add_row(
            str(y_true[obs_2]), str(y_pred[obs_2]), liste_bon_mauvais[obs_2]
        )
    print(tab_res)
