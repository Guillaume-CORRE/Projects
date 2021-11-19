#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description.

Tests pour les fonctions
"""

import gurobipy as gp
from modelisationf import (list_index, annee0_5, industrie0_6,variable_production)

    
def test_annee0_5():
    """Creer une liste avec le nombre d'année voulue de l'année 0 à 5
    """
    entree=5
    sortie=[0,1,2,3,4,5]
    calculee = annee0_5(entree)
    assert calculee == sortie
    
def test_industrie0_6():
    entree = 1
    sortie = {('acier', 0),
 ('acier', 1),
 ('acier', 2),
 ('charbon', 0),
 ('charbon', 1),
 ('charbon', 2),
 ('transport', 0),
 ('transport', 1),
 ('transport', 2)}
    calculee = industrie0_6(entree)
    assert calculee == sortie
    
def test_list_index():
    """Test."""
    entree = 5
    sortie = ["Année 1", "Année 2", "Année 3", "Année 4", "Année 5"]
    calculee = list_index(entree)
    assert calculee == sortie

    
## Ne marche pas à cause des "<"
#def test_variable_production():
#    entree1 = gp.Model("Model_test")
#    entree2 = 2
#    sortie={('charbon', 1): <gurobi.Var *Awaiting Model Update*>,
 #('acier', 0): <gurobi.Var *Awaiting Model Update*>,
 #('acier', 1): <gurobi.Var *Awaiting Model Update*>,
 #('charbon', 0): <gurobi.Var *Awaiting Model Update*>,
 #('transport', 2): <gurobi.Var *Awaiting Model Update*>,
 #('acier', 2): <gurobi.Var *Awaiting Model Update*>,
 #('transport', 1): <gurobi.Var *Awaiting Model Update*>,
 #('charbon', 2): <gurobi.Var *Awaiting Model Update*>,
 #('transport', 0): <gurobi.Var *Awaiting Model Update*>}
  #  calculee = variable_production(entree1,entree2)
  #  assert calculee == sortie
    
    