# Présentation de l'Exercice 14:

## Enoncé

Une économie est consistuée de 3 industries: charbon, acier et transport.

Chaque unité produite par une de ces industries (comptabilisée par 1 euros de valeur produite) nécessite des entrées des 3 industries. Ces entrées sont décalées d'un an entre production et exploitation suivant la règle

| Materiau | Charbon+1 | Acier+1 | Transport+1 |
| --- | --- | --- | --- | 
| Charbon | 0.1 | 0.5 | 0.4 | 
| Acier | 0.1 | 0.1 | 0.2 |
| Transport | 0.2 | 0.1 | 0.2 |
| Main oeuvre | 0.6 | 0.3 | 0.2 | 

Pour augmenter la capacité de production de 1 deux ans plus tard on a les couts suivants

| Materiau | Charbon+1 | Acier+1 | Transport+1 |
| --- | --- | --- | --- | 
| Charbon | 0 | 0.7 | 0.9 | 
| Acier | 0.1 | 0.1 | 0.2 |
| Transport | 0.2 | 0.1 | 0.2 |
| Main_oeuvre | 0.4 | 0.2 | 0.1 |

On peut stocker des produits d'année en année, les stockes et les capacités de production actuelles sont de

| Materiau | Stock_init | Capacité_init |
| --- | --- | --- | 
| Charbon | 150 | 300 | 
| Acier | 80 | 350 | 
| Transport | 100 | 280 | 

La capacité totale de main d'oeuvre est de 470M par année

On veut étudier les scénarios suivant:

- Maximiser la capacité de production totale après 5 ans tout en produisant au moins 60M charbon 60M acier et 30M transport par an. (Question 1)
- Maximiser la production totale des 4e et 5e années. (Question 2)
- Maximiser le main d'oeuvre requise sur l'ensemble des 5 ans en assurant le minimum de production du premier scénario. (Question 3)

## Méthode de résolution :

Mis en application sur Python via Guroby.

Pour la résolution, nous aurons l'année 0 prise en compte afin de pouvoir initialiser toute nos variables.
De plus, nous irons au-delà de l'année 5 afin de faire un modèle logique. En effet, vu que la capacité de production peut-être augementé jusqu'à l'année 5, il nous fait simuler jusqu'à l'année 7. La simulation se fera sur la base d'une modèle statique qui permet le bon déroulement de notre économie en fonction de la production minimale nécessaire par année et les coefficients de production de l'économie.

### Les parametres : 

- nombre_annee = nombre(s) d'année(s) d'observation(s) (5 pour nos problèmes).
- stock_init[i] = stock initiale pour l'industrie i
- capacite_init[i] = capacite initiale pour l'industrie i
- prod_minimale[i] = production_minimale demandée par année pour l'industrie i 
- coeff_production[i,j] = production d'un input i pour l'industrie j
- coeff_capacite[i,j] = capacite d'un input i pour l'industrie j.
- main_oeuvre_prod[i] = capacite de main_oeuvre nécessaire pour produire 1 input de l'industrie i
- main_oeuvre_extra[i] = capacite de main_oeuvre nécessaire pour augmenter de 1 la capacité l'industrie i
- main_oeuvre_cap = capacite de la main d'oeuvre
- industrie_a_b = Chaque industrie pour chaque années, les années allant de a à b.

### Les variables : 

- static_prod[i] = production statique pour l'industrie i 
- production[i,annee] = production pour l'industrie i à l'année annee.
- stock[i, annee] = stock pour l'industrie i a l'annee annee.
- extra_cap[i, annee] = capacite pour l'industrie i que l'on peut augmenter à l'année annee
- production_cap[i, annee] = capacite disponible pour l'industrie i à l'année annee.

### Les fonctions objectives : 

- Pour la première question : 
 $$\sum_{i=industrie} capacite de production[i,5]$$
- Pour la seconde question : 
$$\sum_{i=industrie} production[i,4]+ production[i,5]$$
- Pour la question 3 : 
$$\sum_{i=industrie}\sum_{annee=annees} mainoeuvreprod[i]*production[i, annee+1] + mainoeuvreextra[i]*extracap[i, annee+2]$$

## Modèle statique (pour les années 6 et 7): 

Nous supposons que la demande exogène reste constante jusqu'à et au-delà de l'année 5, le niveau des stocks reste constant et qu'il n'y a pas d'augmentation de la capacité de production
après l'année 5.

Ici on veut résoudre le système : 

\begin{cases}
x=0.1x+0.5y+0.4z+60\\
y=0.1x+0.1y+0.2z+60\\
z=0.2x+0.1y+0.2z+30
\end{cases}

Avec x,y et z les industries

La contrainte pour résoudre ce problème est : 
$$prodstatique[i] = demande[i] + \sum_{j=industrie} coeffproduction[i,j]*prodstatique[j]$$

### Les contraintes : 

#### Contrainte de capacité :

On écrit une contrainte qui va être la définition de la variable productive_cap. On ajoute pour chaque année l'extra capacité produite 2 ans plus tôt à la capacité de production initiale.

- $$productivecap[i, annee] = capaciteinit[i] + \sum_{y=2}^{annee} = extracap[i, y]$$

#### Contrainte pour année 1 à 5 (question 1 et 3):

- $$ production[i, annee] = \sum_{j=industries} coeffproduction[i,j]*production[j, annee+ 1] + \sum_{j=industries} coeffcapacite[i,j]*extracap[j, annee+2] + stock[i, annee + 1] -stock[i, annee]  + prodminimale[i]$$

#### Contrainte pour année 0 (question 1 et 3):

- $$production[i, annee] = \sum_{i=industries} coeffproduction[i,j]*production[i, annee+ 1] + \sum_{i=industries} coeffcapacite[i,j]*extracap[i, annee+2] + stock[i, annee + 1] -stock[i, annee] + 0$$

#### Contrainte main d'oeuvre (Question 1, 2 et 3):

- $$\sum_{j=industries} mainoeuvreprod[j]*production[j, annee] + \sum_{j=industries} mainoeuvrecap[j]*extracap[j, annee+1] \leq mainoeuvrecap$$

#### Contrainte de production et capacité:
- $$production[i, annee] \leq capacite de production[i, annee]$$

#### Les contraintes aux bornes : 

La production est nulle à l'année 0 :
$$\sum_{i=industries} production[i,0].lb=0$$

Les stocks à l'année 0 sont les stocks initiaux
$$\sum_{i=industries} stock[i,0].lb=stockinit[i] \\
\sum_{i=industries} stock[i,0].ub=stockinit[i] $$

A partir de l'année 6, tous est constant, il n'y a pas d'augmentation de capacité 

$$\sum_{i=industries} extracap[i,6].ub=0 \\
\sum_{i=industries} extracap[i,7].ub=0$$



## Les Résultats : 

1) Pour le modèle statique : On a une production constante de :
 - 166.40 unités de charbon 
 - 105.67 unités de acier 
 - 92.31 unités de transport 
 
2) Pour la question 1, en utilisant la fonction objectif associé et toutes les contraintes, on obtient comme valeur maximale de capacité de production à l'année 5 de : **2141 millions**. Avec comme capacité à l'année 5 pour les industries :
 - 1511 millions de capacité de charbon disponible
 - 350 millions de capacité d'acier disponible
 - 280 millions de capacité de transport disponible
 
3) Pour la question 2, en utilisant la fonction objectif associé et toutes les contraintes sauf celle qui nécessite une demande constante respectée, on obtient comme valeur maximale de production aux années 4 et 5 de : **2618 millions**. Avec comme capacité à l'année 5 pour les industries :
 - 430.5 millions de charbon produit pour chaque années
 - 359.4 millions d'acier produit chaque années 
 - 519.38 millions de transport produit chaque années
 
3) Pour la question 3, en utilisant la fonction objectif associé et toutes les contraintes comme la question 1, on obtient comme valeur maximale de main d'oeuvre pour les 5 premières années de: **2073 millions**.

## Limites du projet et axes d'améliorations : 

- Faire une librairie avec les fonctions bien testées.
- Pouvoir laisser l'utilisateur rentrer les coefficients de production et de capacité.
- Réaliser une application plus élaborée avec manuel d'utilisation.