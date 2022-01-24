# -*- coding: utf-8 -*-

"""Description.

Module auxiliaire pour l'obtention des backups html des annonces pour ordinateurs portables neufs pour les sites marchands CDiscount et Amazon. Range les backups dans des dossiers par page du site.

"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as BS
import os 
from time import sleep, time


########### CDiscount #################################
########################################################


def cookies(soupe:BS):
    """Fonction permettant de passer l'étape des cookies sur CDiscount
    """
    elem = soupe.find(text="Accepter")
    bouton = nav.find_element(By.ID, "footer_tc_privacy_button_3")
    bouton.click()
    sleep(2)
    
def recherche():
    """Fonction permettant de taper l'élement de recherche voulu et de lancer la recherche
    """
    recherche = nav.find_element(By.XPATH, "//div[@class='hSrcInput']/input[1]")
    #recherche.screenshot("recherche.png")
    recherche.send_keys("Ordinateur portable")
    sleep(3)
    recherche.send_keys(Keys.ENTER)
    sleep(2)
    
def neuf():
    code = nav.page_source
    soupe=BS(code) 
    neuf = soupe.find_all(attrs={"value": ["Neuf ou occasion/neuf"]})[0]
    neuf = neuf.parent.get_text(strip=True)
    neuf_b = nav.find_element(By.XPATH, f"//span[@title='{neuf}']") 
    #neuf_b.screenshot("neuf_b.png")
    neuf_b.click()
    sleep(3)

def retour():
    """Fonction permettant de revenir en arrière, driver.back() plus facile.
    """
    code= nav.page_source
    soupe = BS(code)
    #retour = soupe.find(text = "Retour aux offres")
    retour = nav.find_element(By.CLASS_NAME, "bcBack")
    #retour.screenshot("retour.png")
    retour.click()
    
def changer_page(num_page:int):
    """Fonction permettant de changer de page. Soit on passe à la page suivante(suivante) soit on peut 
    revenir à la prècèdente (retour). Permet de changer de page malgrès le changement de code html entre la
    page 1 et les suivantes.
    """
    if num_page < 1:
        changer_page = nav.find_element(By.CLASS_NAME, "btBlue")
        changer_page.click()
        sleep(5)
    else:
        changer_page_2 = nav.find_elements(By.CLASS_NAME, "btBlue")
        retour, suivant = changer_page_2
        suivant.click()
        sleep(5)
        
def une_page(num_page:int, nb_articles:int)->str:
    """Fonction permettant de récupérer les backups html des annonces d'une page en fonction
    du nombre d'article voulu par page.
    Exemple: 
    >>> une_page(1, 1)
    >>> path + \article_1.html
    """
    for num_article in range(3, nb_articles+3):#47
        sleep(3)
        liens =  nav.find_elements(By.XPATH, "//a[@class='jsPrdtBILA prdtBILA']")[num_article]
        liens.click()
        sleep(6)
        path = f"C:/Users/Guillaume CORRE/Machine_learning/Projet/Page_{num_page+1}"
        with open(path + f"/article_{num_article-2}.html", "w", encoding="utf8") as fichier:
            fichier.write(nav.page_source)
        sleep(4)
        nav.back()
        
def all_backup(nb_articles:int, nb_page:int)->str:
    """Fonction permettant de récupérer les annonces en fonction du nombre de pages et du
    nombre d'article par page voulu. Range les backup html dans des dossiers.
    Exemple: 
    >>> all_backup(1, 1)
    >>> path + \Page_1\article_1.html
    """
    nav = webdriver.Chrome()
    nav.get("https://www.cdiscount.com")
    code = nav.page_source
    soupe = BS(code)
    cookies(soupe)
    sleep(2)
    recherche()
    sleep(2)
    neuf()
    sleep(2)
    for num_page in range(0, nb_page-1):#21
        os.mkdir(f"Page_{num_page+1}")
        une_page(num_page, nb_articles-1)
        sleep(4)
        changer_page(num_page)
        sleep(6)
    nav.quit()
    
def retour_page_1():
    """Fonction permettant de revenir à la première page de la recherche
    """
    retour_debut = nav.find_element(By.CLASS_NAME, "jsFirstPage")
    retour_debut.screenshot("retour_debut.png")
    retour_debut.click()
    
########### Amazon #################################
########################################################

def cookies_amazon(soupe:BS):
    """Fonction permettant de passer le problème des cookies sur Amazon
    """
    elem = soupe.find(text="Accepter les cookies")
    bouton = nav.find_element(By.CLASS_NAME, "a-button-inner") 
    bouton.click()
    sleep(2)
    
def recherche_amazon():
    """Fonction permettant de taper l'élement de recherche voulu dans la barre de recherche
     Cdiscount et de lancer la recherche
    """
    recherche = nav.find_element(By.ID, "twotabsearchtextbox")
    #recherche.screenshot("recherche.png")
    recherche.send_keys("Ordinateur Portable")
    sleep(3)
    recherche.send_keys(Keys.ENTER)
    
def neuf_amazon():
    """Fonction permettant de chercher l'item "Neuf" et de cliquer dessus.
    Dépend du format d'affichage de la page.
    """
    try:
        neuf = nav.find_elements(By.XPATH, "//a[@class='a-link-normal sf-filter-floatbox aok-inline-block    aok-align-bottom s-no-hover s-no-underline']")
        indice = len(neuf)
        neuf = nav.find_elements(By.XPATH, "//a[@class='a-link-normal sf-filter-floatbox aok-inline-block aok-align-bottom s-no-hover s-no-underline']")[indice - 6]
        #neuf.screenshot("neuf_amazon.png")
        neuf.click()
        sleep(2)
    except:
        neuf = nav.find_elements(By.XPATH, "//span[@class='a-list-item']")
        indice = len(neuf)
        neuf = nav.find_elements(By.XPATH, "//span[@class='a-list-item']")[indice - 3]
        #neuf.screenshot("neuf_amazon.png")
        neuf.click()
        sleep(2)
        
def retour_amazon():
    """Fonction permettant de revenir à la page précèdente".
    """
    retour = nav.find_element(By.PARTIAL_LINK_TEXT, 'Retour aux résultats')
    #retour.screenshot("retour_amazon.png")
    nav.get(retour.get_attribute('href'))
    
def suivant_amazon():
    """Fonction permettant de passer à la page suivante et cherchant l'item "Suivant".
    """
    suivant = nav.find_element(By.PARTIAL_LINK_TEXT, 'Suivant')
    #suivant.screenshot("suivant_amazon.png")
    suivant.click()
    
    
def une_page_amazon(num_page:int, nb_articles:int)->str:
    """Fonction permettant de récuperer les annonces d'une page en fonction du nombre que l'on veut".
    Exemple: 
    >>> une_page_amazon(1, 1)
    >>> path + \article_1.html
    """
    for num_article in range(0, nb_articles-1): #41
        sleep(3)
        liens = nav.find_elements(By.XPATH, "//span[@class='a-price']")[num_article]
        liens.click()
        sleep(5)
        path = f"C:/Users/Guillaume CORRE/Machine_learning/Projet/Pageamazon_{num_page+1}"
        with open(path + f"/article_{num_article+1}.html", "w", encoding="utf8") as fichier:
            fichier.write(nav.page_source)
        sleep(3)
        nav.back()
        
def all_backup_amazon(nb_pages: int, nb_articles:int)->str:
    """Fonction permettant de récuperer le nombre d'annonce sur un nombre de page défini
    et qui va classer les backup html dans des dossiers en fonction de la page".
    Exemple: 
    >>> all_backup_amazon(1, 1)
    >>> path + \Page_1\article_1.html
    """
    nav = webdriver.Chrome()
    nav.get("https://www.amazon.fr")
    sleep(6)
    code = nav.page_source
    soupe = BS(code)
    cookies_amazon(soupe)
    sleep(3)
    recherche_amazon()
    sleep(3)
    neuf_amazon()
    sleep(3)
    for num_page in range(0, nb_pages-1): #7
        os.mkdir(f"Pageamazon_{num_page+1}")
        une_page_amazon(num_page, nb_articles-1)
        sleep(6)
        suivant_amazon()
        sleep(6)
    nav.quit()