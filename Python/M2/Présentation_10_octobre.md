# Projet Machine Learning : Guillaume CORRE

## Objectif :
- Estimer le prix d'un ordinateur portable en fonctions de certaines caractéristiques (Processeur, RAM, Taille, elements externes,...)
- Mais plus précisement, d'estimer un modèle qui pourra être réutilisé par un vendeur par exemple lorsqu'un client viendra lui demander des informations sur le prix d'un ordinateur.
- Le client précise le type d'ordinateur qu'il veut et le vendeur ajuste les caractéristiques et le modèle donne une gamme de prix pour l'ordinateur voulu.

## Plusieurs Etapes :

1. Scrapping des pages HTML des sites Amazon et Cdicount.
2. Parsing HTML de ces pages afin d'obtenir les données.
3. Nettoyage de la base de données.
4. Visualisation des données et application des modèles de machine learning.

## 1. Scrapping

Dans cette partie, utilisation des deux librairies qui sont `BeautifulSoup` et `Selenium`.
L'objectif final est pour chaque site, de récupérer le nombre de pages et le nombre d'articles par page voulu et de ranger tous les backups dans des dossiers en fonction de la page.

### Difficultés particulières rencontrées : 
- Sur Cdiscount: 

    Le captcha lors de l'ouverture de l'adresse du site au bout de 1 semaine de test de scrapping. Vu que c'était seulement à l'ouverture du site et non par la suite, je le faisais à la main.


- Sur Amazon : 

    Les pages de produit Apple qui sont propres à la marque et qui n'avaientt pas de bouton pour revenir en arrière lorsque je connaissais pas la fonction driver.back()
    
    La présentation html du site qui change quand on relance le code et donc des boutons qui ne se trouvent pas au bon endroit. Heureusement je suis tombé sur seulement 2 types de pages.

## 2. Parsing HTML des backups

Dans cette partie, utilisation de la librairie `BeautifulSoup`.
L'objectif final est pour chaque backup de récupérer les informations voulues et de les ranger dans un dictionnaire. De mettre tous ces dictionnaires dans une liste et de créer un fichier JSON pour stocker les données récupérées.

### Difficultés particulières rencontrées : 

- Sur CDiscount, certains produits avaient une première description et d'autres non, il fallait donc d'abord récupérer la première description et ensuite récupérer les infos supplémentaires dans le tableau descriptif sans faire de doublons. Mise en place d'un test pour déterminer si il y a une première description et récupération de données différente en fonction du résultat du test.

- Comme lors du scrapping, les produtis apple ont une page  dédiés et donc leurs tableaux pour récupérer les élements ne sont pas les mêmes d'un point de vu code html.

## 3. Nettoyage des données

Dans cette partie, utilisation de la librairie `Pandas` et des expressions régulières.
Tout d'abord, j'ai transformé les données json en un dataframe pandas pour les données Amazon et Cdiscount. Premières modification pour que les deux dataframes aient des colonnes identiques et regroupement des deux.
Nettoyage colonne par colonne, très long et rebarbatif, prise en compte du fais que les données sont très mal renseignées sur ces sites et toujours de manière différentes. 
Gestion des données manquantes très délicate.
J'ai au final deux bases de données : une avec le prix (la variable à prédire) en numérique et une autre avec la variable prix en classe (ce qui nous intéressent dans l'objectif du projet).

## 5. Visualisation et ML

Dans cette partie, utilisation de la librairie `seaborn` pour les graphiques et `scikit-learn` pour le ML.
Du fait d'avoir gardé deux bases de données dans la partie précèdente, j'ai pu comparer les résultats en fonction de la mise en place de modèle de regression ou de classification.

Cette partie se décompose en 4 étapes:

- Visualisation des données
- Préparation des données
- Application des différents modèles de ML
- Evaluation du meilleur modèle


# Conclusion

D'un point de vue machine learning, je ne pense pas que mon modèle soit super bon du à 2 problèmes principaux qui sont :
- La qualité des données renseignées sur ces sites de ventes en ligne.
- Le manque de données finales du à ces problèmes de qualité des données.

On passe de 1100 données au départ(ce qui n'est pas énorme mais peut être suffisant) à moins de 700 en ayant géré un grand nombre de données manquantes. 
De plus, le fait de gardé les observations avec données manquantes pour arriver à environ 1000 données n'amélioraient pas les modèles.
