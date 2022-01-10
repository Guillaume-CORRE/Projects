"""Description.

Module auxiliaire pour la résolution de l'exercice 14.
"""

import numpy as np
import pandas as pd
from itertools import product

import gurobipy as gp
from gurobipy import GRB

from typing import Dict, Tuple, List

# Nos industries
industries=['charbon','acier','transport']

#Stock initiaux
stock_init = ({'charbon' : 150,
             'acier' : 80,
             'transport' : 100})

#Capacité initiales
capacite_init = ({'charbon' : 300,
             'acier' : 350,
             'transport' : 280})

#Ce qui doit etre produit au minimum chaque année
prod_minimale = ({'charbon' : 60,
             'acier' : 60,
             'transport' : 30})

coeff_production = {
    ('charbon', 'charbon'): 0.1,
    ('charbon', 'acier'): 0.5,
    ('charbon', 'transport'): 0.4,
    ('acier', 'charbon'): 0.1,
    ('acier', 'acier'): 0.1,
    ('acier', 'transport'): 0.2,
    ('transport', 'charbon'): 0.2,
    ('transport', 'acier'): 0.1,
    ('transport', 'transport'): 0.2,
    ('main_oeuvre', 'charbon'): 0.6,
    ('main_oeuvre', 'acier'):0.3,
    ('main_oeuvre', 'transport'):0.2
}

# main_oeuvre à la production
main_oeuvre_production = ({'charbon': 0.6,
                     'acier': 0.3,
                     'transport': 0.2})
   
# coeff pour extra capacite
coeff_capacite = {
    ('charbon', 'charbon'): 0.0,
    ('charbon', 'acier'): 0.7,
    ('charbon', 'transport'): 0.9,
    ('acier', 'charbon'): 0.1,
    ('acier', 'acier'): 0.1,
    ('acier', 'transport'): 0.2,
    ('transport', 'charbon'): 0.2,
    ('transport', 'acier'): 0.1,
    ('transport', 'transport'): 0.2
}

# main d'oeuvre pour extra capacite
main_oeuvre_extra = ({'charbon': 0.4,
                      'acier': 0.2,
                      'transport': 0.1})

# Paramètres de temps
def annee1_5(nombre_année:int)->list:
    """Creer une liste d'année allant de 1 à nombre d'année (5 dans le problème particulier)
    Exemple: 
    >>> annee1_5(2)
    >>> [1, 2]
    """
    annee1_5=[]
    for i in range(1,nombre_année+1):
        annee1_5.append(i)
    return(annee1_5)

def annee0_5(nombre_année:int)->list:
    """Creer une liste d'année allant de 0 à nombre d'année (5 dans le problème particulier)
    Exemple: 
    >>> annee0_5(2)
    >>> [0, 1, 2]
    """
    annee0_5=[]
    for i in range(nombre_année+1):
        annee0_5.append(i)
    return(annee0_5)

def annee0_6(nombre_année:int)->list:
    """Creer une liste d'année allant de  0 à nombre d'année + 1 (6 dans le problème particulier)
    Exemple: 
    >>> annee0_6(2)
    >>> [0, 1, 2, 3]
    """
    annee0_6=[]
    for i in range(nombre_année+2):
        annee0_6.append(i)
    return(annee0_6)
    
def annee1_7(nombre_année:int)->list:
    """Creer une liste d'année allant de 1 à nombre d'année + 2 (7 dans le problème particulier)
    Exemple: 
    >>> annee1_7(2)
    >>> [1, 2, 3, 4]
    """
    annee1_7=[]
    for i in range(1,nombre_année+3):
        annee1_7.append(i)
    return(annee1_7)

def annee1_6(nombre_année:int)->list:
    """Creer une liste d'année allant de 1 à nombre d'année + 1 (6 dans le problème particulier)
    Exemple: 
    >>> annee1_6(2)
    >>> [1, 2, 3]
    """
    annee1_6=[]
    for i in range(1,nombre_année+2):
        annee1_6.append(i)
    return(annee1_6)

# Préparation pour la création de nos variables en fonction de l'industrie et du temps
def industrie0_6(nombre_année:int)->set:
    """Permet d'obtenir un set comprenant chaque industrie pour chaque année de 0 à nombre d'année +1, sera utilise pour la construction de nos variables production et stock
    Exemple:
    >>> industrie0_6(2)
    >>> {('acier', 0),
         ('acier', 1),
         ('acier', 2),
         ('charbon', 0),
         ('charbon', 1),
         ('charbon', 2),
         ('transport', 0),
         ('transport', 1),
         ('transport', 2)}
    """
    industrie_0_6 = set(product(industries, annee0_6(nombre_année) ))
    return industrie_0_6
    
def industrie1_7(nombre_année:int)->set:
    """Permet d'obtenir un set comprenant chaque industrie pour chaque année de 1 à nombre d'année +2, sera utilise pour la construction de notre variable extracap
    Exemple:
    >>> industrie1_7(1)
    >>> {('acier', 1),
         ('acier', 2),
         ('acier', 3),
         ('charbon', 1),
         ('charbon', 2),
         ('charbon', 3),
         ('transport', 1),
         ('transport', 2),
         ('transport', 3)}
    """
    industrie_1_7 = set(product(industries, annee1_7(nombre_année) ))
    return industrie_1_7
    
def industrie1_6(nombre_année:int)->set:
    """Permet d'obtenir un set comprenant chaque industrie pour chaque année de 1 à nombre d'année +1, sera utilise pour la construction de notre variable productioncap 
    Exemple:
    >>> industrie1_6(2)
    >>> {('acier', 1),
         ('acier', 2),
         ('acier', 3),
         ('charbon', 1),
         ('charbon', 2),
         ('charbon', 3),
         ('transport', 1),
         ('transport', 2),
         ('transport', 3)}
    """
    industrie_1_6 = set(product(industries, annee1_6(nombre_année) ))
    return industrie_1_6

###########################################################################################################################
def list_index(nombre_année:int)->list: 
    """Retourne une liste d'annees allant de 1 au nombre d'année voulues.
    La fonction va être utiliser afin de choisir le nombre d'index dans nos tableaux de résultats.
    Exemple:
    >>> list_index(5)
    >>> ['Année 1', 'Année 2', 'Année 3', 'Année 4', 'Année 5']
    """
    index=[]
    for numeroannee in range(1,nombre_année+1):
        index.append("Année {}".format(numeroannee))
    return index

########################################################################################################################################
########################################################################################################################################

statique = gp.Model('Modele_statique')
modele1 = gp.Model('Mon_modele_question1')
modele2 = gp.Model('Mon_modele_question2')
modele3 = gp.Model('Mon_modele_question3')


def variable_statique(modele:gp.Model)->Dict[str, gp.Var]:
    """Creer les variables liées à la production statique pour industrie.
    """
    prod_statique = modele.addVars(industries, lb=0, name="static_prod")
    return prod_statique

    

def variable_production(modele:gp.Model, nombre_année:int)->Dict[Tuple[str, int],gp.Var]:
    """Creer les variables de production pour chaque années dans le nombre d'année +1 et chaque industries.
    Exemple :
    >>> variable_production(modele1, 1)
    >>>
    >>> {('acier', 1): <gurobi.Var *Awaiting Model Update*>,
         ('transport', 2): <gurobi.Var *Awaiting Model Update*>,
         ('charbon', 2): <gurobi.Var *Awaiting Model Update*>,
         ('charbon', 1): <gurobi.Var *Awaiting Model Update*>,
         ('acier', 2): <gurobi.Var *Awaiting Model Update*>,
         ('acier', 0): <gurobi.Var *Awaiting Model Update*>,
         ('transport', 1): <gurobi.Var *Awaiting Model Update*>,
         ('transport', 0): <gurobi.Var *Awaiting Model Update*>,
         ('charbon', 0): <gurobi.Var *Awaiting Model Update*>}
    """
    production = modele.addVars(industrie0_6(nombre_année), lb=0, ub=capacite_init, name="production")
    return production



def variable_stock(modele:gp.Model, nombre_année:int)->Dict[Tuple[str, int],gp.Var]:
    """Creer les variables de stock pour chaque années dans le nombre d'année +1 et chaque industries
    """
    stock = modele.addVars(industrie0_6(nombre_année), lb=0, name="stock")
    return stock



def variable_extracap(modele:gp.Model, nombre_année:int)->Dict[Tuple[str, int],gp.Var]:
    """Creer les variables d'extra capacité pour chaque années dans le nombre d'année +2 et chaque industries
    """
    extra_cap = modele.addVars(industrie1_7(nombre_année), lb=0, name="extra_cap")
    return extra_cap



def variable_productioncap(modele:gp.Model, nombre_année:int)->Dict[Tuple[str, int],gp.Var]:
    """Creer les variables de capacité de production pour chaque années dans le nombre d'année +1 et chaque industries
    """
    production_cap = modele.addVars(industrie1_6(nombre_année) ,name="capacite_production")
    return production_cap

#########################################################################################################################################
#########################################################################################################################################
#########################################################################################################################################

def objectif_statique(modele:gp.Model)->None:
    """Definit l'objectif du modèle statique
    """
    modele.setObjective(0)
    

def objectifs(modele:gp.Model, production:Dict[Tuple[str, int],gp.Var], extra_cap:Dict[Tuple[str, int],gp.Var], production_cap:Dict[Tuple[str, int],gp.Var], nombre_année:int)->None:
    """Permet de definir l'objectif à maximiser en fonction du modèle choisit.
    Entrée: notre modele, les variables nécessaires pour la création de l'objectif et le nombre d'années de travail
    Sortie: la fonction objectif du modèle
    """
    if modele==modele1:
        objectif=modele.setObjective((gp.quicksum(production_cap[industrie,nombre_année] for industrie in industries) ), GRB.MAXIMIZE)
        return objectif
    elif modele==modele2:
        objectif=modele.setObjective(
    (gp.quicksum(production[industrie,nombre_année-1] + production[industrie,nombre_année] for industrie in industries )),
    GRB.MAXIMIZE)
        return objectif
    elif modele==modele3:
        objectif=modele.setObjective(
    (gp.quicksum(main_oeuvre_production[industrie]*production[industrie,annee+1] for industrie in industries for annee in annee1_5(nombre_année)) 
     + gp.quicksum(main_oeuvre_extra[industrie]*extra_cap[industrie,annee+2] for industrie in industries for annee in annee1_5(nombre_année))), GRB.MAXIMIZE)
        return objectif
    
#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################

def contrainte_statique(modele:gp.Model, prod_statique:Dict[str, gp.Var])->Dict[Tuple[str],gp.Constr]:
    """Creer les contraintes associés au modèle statique prenant en compte les variables associé au modèle
    """
    statique_contrainte = modele.addConstrs(
(prod_statique[industrie] == gp.quicksum(coeff_production[industrie,industrie_2]*prod_statique[industrie_2] for industrie_2 in industries) 
+ prod_minimale[industrie] for industrie in industries), name='statique_contrainte' )
    return statique_contrainte


    
def contrainte_production1(modele:gp.Model, production:Dict[Tuple[str, int],gp.Var], stock:Dict[Tuple[str, int],gp.Var], extra_cap:Dict[Tuple[str, int],gp.Var], nombre_année:int)->Dict[Tuple[str,int],gp.Constr]:
    """Créer la contrainte de production du modèle pour les années 1 à nombre d'année pour les modèles 1 et 3
    Exemple: 
    >>> contrainte_production(modele1, production, stock, extra_cap, 2)
    >>>
    >>> {('charbon', 1): <gurobi.Constr *Awaiting Model Update*>,
         ('charbon', 2): <gurobi.Constr *Awaiting Model Update*>,
         ('acier', 1): <gurobi.Constr *Awaiting Model Update*>,
         ('acier', 2): <gurobi.Constr *Awaiting Model Update*>,
         ('transport', 1): <gurobi.Constr *Awaiting Model Update*>,
         ('transport', 2): <gurobi.Constr *Awaiting Model Update*>}
    """
    contrainte_1 = modele.addConstrs(( production[industrie, annee] + stock[industrie,annee]  == 
                              gp.quicksum(coeff_production[industrie,industrie_2]*production[industrie_2, annee + 1] for industrie_2 in industries) 
                              + gp.quicksum(coeff_capacite[industrie,industrie_2]*extra_cap[industrie_2, annee + 2] for industrie_2 in industries ) 
                              + stock[industrie, annee+1] + prod_minimale[industrie] for industrie in industries for annee in annee1_5(nombre_année) ), name='cont_cont' )
    return contrainte_1



def contrainte_production2(modele:gp.Model, production:Dict[Tuple[str, int],gp.Var], stock:Dict[Tuple[str, int],gp.Var], extra_cap:Dict[Tuple[str, int],gp.Var], nombre_année:int)->Dict[Tuple[str,int],gp.Constr]:
    """Créer la contrainte de production du modèle 2 pour les années 0 à 5 "pour le modèle 2, nous n'avons pas de contrainte de minimum de production par année"
    """
    contrainte_1_2 = modele.addConstrs(( production[industrie, annee] + stock[industrie,annee]  == 
                              gp.quicksum(coeff_production[industrie,industrie_2]*production[industrie_2, annee + 1] for industrie_2 in industries) 
                              + gp.quicksum(coeff_capacite[industrie,industrie_2]*extra_cap[industrie_2, annee + 2] for industrie_2 in industries ) 
                              + stock[industrie, annee+1]  for industrie in industries for annee in annee0_5(nombre_année) ), name='cont_cont' )
    return contrainte_1_2


    
def contrainte_production0(modele:gp.Model, production:Dict[Tuple[str, int],gp.Var], stock:Dict[Tuple[str, int],gp.Var], extra_cap:Dict[Tuple[str, int],gp.Var])->Dict[Tuple[str,int],gp.Constr]:
    """Créer la contrainte de production pour l'année 0 pour les modèles 1 et 3
    """
    contrainte_2 = modele.addConstrs(( production[industrie,0] + stock[industrie,0]  == 
                                  gp.quicksum(coeff_production[industrie,industrie_2]*production[industrie_2,1] for industrie_2 in industries) 
                                  + gp.quicksum(coeff_capacite[industrie,industrie_2]*extra_cap[industrie_2,2] for industrie_2 in industries ) 
                                  + stock[industrie,1] + 0 for industrie in industries), name='cont_cont_2' )
    return contrainte_2    



def contrainte_main_oeuvre(modele:gp.Model, production:Dict[Tuple[str, int],gp.Var], extra_cap:Dict[Tuple[str, int],gp.Var], nombre_année:int, main_oeuvre_cap:int)->Dict[Tuple[str,int],gp.Constr]:
    """Creer la contrainte de main_oeuvre par annéee et industrie
    """
    contrainte_main_oeuvre = modele.addConstrs((main_oeuvre_cap >= 
                                          gp.quicksum(main_oeuvre_production[industrie]*production[industrie,annees] for industrie in industries)
                                          +gp.quicksum(main_oeuvre_extra[industrie]*extra_cap[industrie,annees+1] for industrie in industries)
                                           for industrie in industries for annees in annee1_6(nombre_année) ), name="cont_main_oeuvre")
    return contrainte_main_oeuvre


    
def contrainte_capacite1(modele:gp.Model, production_cap:Dict[Tuple[str, int],gp.Var], extra_cap:Dict[Tuple[str, int],gp.Var], nombre_année:int)->Dict[Tuple[str,int],gp.Constr]:
    """Definit la première contrainte de capacité par industires et années
    """
    capacite_prod_1 = modele.addConstrs((production_cap[industrie,annee] == 
                                     capacite_init[industrie] 
                                     +gp.quicksum(extra_cap[industrie,annee_bis] for annee_bis in range(2,annee+1)) for industrie in industries for annee in annee1_6(nombre_année) ), name='cont_production_cap')
    return capacite_prod_1


    
def contrainte_capacite2(modele:gp.Model, production:Dict[Tuple[str, int],gp.Var], production_cap:Dict[Tuple[str, int],gp.Var], nombre_année:int)->Dict[Tuple[str,int],gp.Constr]:
    """ Deuxième contrainte de capacité qui dit que la production d'une année ne peut pas excéder la capacité de production la même année.
    """
    
    contrainte_capacite_2 = modele.addConstrs((production[industrie,annee] <= production_cap[industrie,annee] for industrie in industries for annee in annee1_6(nombre_année) ), name='cont_cap_4')
    return contrainte_capacite_2



def initialisation_annee0(production:Dict[Tuple[str, int],gp.Var], stock:Dict[Tuple[str, int],gp.Var])->None:
    """Fonction qui initialise les données pour l'année 0 de nos modèles
    On n'a pas de production et les stocks à l'année zéro sont initialisés.
    """
    for industrie in industries: 
        production[industrie,0].ub=0
        stock[industrie,0].lb=stock_init[industrie]
        stock[industrie,0].ub=stock_init[industrie]
        
        
    
def production_annee6(production:Dict[Tuple[str, int],gp.Var], prod_statique:Dict[str, gp.Var], nombre_année:int)->None:
    """Fonction qui définit une production statique pour l'année 6
    Pour l'année 6, la production sera celle obtenue lors de la résolution du modèle statique
    """
    for industrie in industries:
        production[industrie,nombre_année+1].lb=prod_statique[industrie].x
        
        
        
def capacite_annee6_7(extra_cap:Dict[Tuple[str, int],gp.Var], nombre_année:int)->None:
    """Fonction qui définit qu'il n'y aura pas d'augmentation de capacité à partir de l'année 6.
    Nous arretons notre process à l'année 5 dans l'exemple particulier, donc on arrete la possibilité d'augmenter le capacité à l'année 6
    """
    for annees in range(nombre_année+1,nombre_année+3):
        for industrie in industries:
            extra_cap[industrie,annees].ub=0
            
            

######################################################################################################################################################################################################################################################            
def resolution_statique(modele:gp.Model)->Dict[str, gp.Var]:
    """Fonction qui permet de résoudre le problème statique
    En prenant la variable, la contrainte et la fonction objectif du modèle, elle renvoie les résultats pour chacunes des industries.
    """
    variable1=variable_statique(modele)
    contrainte1=contrainte_statique(modele,variable1)
    objectif=objectif_statique(modele)
    modele.Params.LogToConsole = 0
    modele.optimize()
    return variable1


        
def resolution_modele1_3(modele:gp.Model, nombre_année:int, main_oeuvre_cap:int)->Tuple[Dict[Tuple[str,int],gp.Var], Dict[Tuple[str,int],gp.Var], Dict[Tuple[str,int],gp.Var], float]:
    """Fonction qui permet la résolution des modèles 1 et 3. 
    En prenant les variables et contraintes associés à ces modèles ainsi que la fonction objective.
    Ressort les résultats pour les variables à maximiser et la valeur max total du programme.
    """
    variable1=variable_production(modele, nombre_année)
    variable2=variable_stock(modele, nombre_année)
    variable3=variable_extracap(modele, nombre_année)
    variable4=variable_productioncap(modele, nombre_année)
    objectif=objectifs(modele,variable1,variable3,variable4, nombre_année)
    contrainte1=contrainte_production1(modele,variable1,variable2,variable3, nombre_année)
    contrainte2=contrainte_production0(modele,variable1,variable2,variable3)
    contrainte3=contrainte_main_oeuvre(modele,variable1,variable3, nombre_année,main_oeuvre_cap)
    contrainte4=contrainte_capacite1(modele,variable4,variable3, nombre_année)
    contrainte5=contrainte_capacite2(modele,variable1,variable4, nombre_année)
    initialisation_annee0(variable1,variable2)
    production_stable=production_annee6(variable1,resolution_statique(statique),nombre_année)
    extra_cap6_7=capacite_annee6_7(variable3, nombre_année)
    modele.Params.LogToConsole = 0
    modele.optimize()
    valeur_max = modele.objval
    return  variable1, variable3, variable4, valeur_max



def resolution_modele2(modele:gp.Model, nombre_année:int, main_oeuvre_cap:int)->(Dict[Tuple[str,int],gp.Var], Dict[Tuple[str,int],gp.Var], float):
    """Fonction qui permet la résolution du modèle 2.
    En prenant les variables et contraintes associés à ce modèle ainsi que la fonction objective.
    Ressort les résultats pour les variables ainsi que la valeur max.
    """
    variable1=variable_production(modele, nombre_année)
    variable2=variable_stock(modele, nombre_année)
    variable3=variable_extracap(modele, nombre_année)
    variable4=variable_productioncap(modele, nombre_année)
    objectif=objectifs(modele,variable1,variable3,variable4, nombre_année)
    contrainte1=contrainte_production2(modele,variable1,variable2,variable3, nombre_année)
    contrainte3=contrainte_main_oeuvre(modele,variable1,variable3, nombre_année, main_oeuvre_cap)
    contrainte4=contrainte_capacite1(modele,variable4,variable3, nombre_année)
    contrainte5=contrainte_capacite2(modele,variable1,variable4, nombre_année)
    initialisation_annee0(variable1,variable2)
    production_stable=production_annee6(variable1,resolution_statique(statique),nombre_année)
    extra_cap6_7=capacite_annee6_7(variable3, nombre_année)
    modele.Params.LogToConsole = 0
    modele.optimize()
    valeur_max = modele.objval
    return variable1, variable3, valeur_max

######################################################################################################################################################################################################################################################

def resultat_statique(prod_statique:Dict[str, gp.Var])->None:
    """Retourne les résultats du modèle statique par industries.
    """
    print("Les résultats pour le modèle statique sont : ")
    for industrie in industries:
        if (prod_statique[industrie].x > 1e-6):
            unite_statique_prod ='{:,.2f}'.format(prod_statique[industrie].x)
        print(f" {unite_statique_prod} unités de {industrie} ")
        
        
               
def resultat_modele_1(production_cap:Dict[Tuple[str,int],gp.Var], nombre_année:int)->pd.DataFrame:
    """retourne les résultats du modèle 1 sous forme de tableau
    """
    res_prod_cap={}
    for industrie in industries:
        my_list_4 = []
        for annee in annee1_5(nombre_année):
            my_list_4.append('{:,.2f}'.format(production_cap[industrie,annee].x ) )
        res_prod_cap[industrie] = my_list_4
        capacite_prod= pd.DataFrame(res_prod_cap, index=list_index(nombre_année))
    return capacite_prod



def resultat_modele_2(production:Dict[Tuple[str,int],gp.Var], nombre_année:int)->pd.DataFrame:
    """Retourne les résultats du modèle 2 sous forme de tableau
    """
    res_prod_cap={}
    for industrie in industries:
        my_list_4 = []
        for annee in annee1_5(nombre_année):
            my_list_4.append('{:,.2f}'.format(production[industrie,annee].x ) )
        res_prod_cap[industrie] = my_list_4
        capacite_prod= pd.DataFrame(res_prod_cap, index=list_index(nombre_année))
    return capacite_prod



def resultat_modele_3(production:Dict[Tuple[str,int],gp.Var], extra_cap:Dict[Tuple[str,int],gp.Var], nombre_année:int)->pd.DataFrame:
    """Retourne les résultats du modèle 3 sous forme de tableau
    On rentre les variable qui nous intéressent lié à la main d'oeuvre :la production et l'extra_capacite
    On obtient un data frame avec pour chaque années et chaque industries la quantité de main d'oeuvre utilisée.
    """
    dict_resultat={}
    for industrie in industries:
        liste_resultat=[]
        for annee in range(1,nombre_année+1):
            liste_resultat.append(round(main_oeuvre_production[industrie],1)*round(production[industrie,annee+1].x,1) + round(main_oeuvre_extra[industrie],1)*round(extra_cap[industrie,annee+2].x,1))
        dict_resultat[industrie]=liste_resultat
        
    somme2=[]
    for n in range(0,nombre_année):
        somme=[]
        for industrie in industries: 
            somme.append(dict_resultat[industrie][n])
        somme2.append(somme)
    final=[]
    for somme in somme2:
        final.append(round(sum(somme),2))
            
    result=dict_resultat
    result['Total']=final
        
    tab_MO = pd.DataFrame(result, index=list_index(nombre_année))
    return(tab_MO)


##########################################################################################################################

#Pour pouvoir choisir les coefficient avant le programme, mais ne marche pas si on rentre de mauvaises valeurs. En effet, il faut que l'on puisse satisfaire la production minimale en fonction des stocks, ect..

#def liste_coeff_production():
    #dico={}
    #for i in industries:
        #for j in industries: 
            #print("Quantité nécessaire pour produire un", i,"à partir d'un", j)
            #dico[i,j]=float(input())
    #return dico

#coeff_production=liste_coeff_production()