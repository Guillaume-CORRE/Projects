# -*- coding: utf-8 -*-
# 1)   Importation des modules nécessaires
import tkinter as tk
from tkinter import ttk
import modelisationf as md
from tkinter import messagebox
import sys


root = tk.Tk() 
root.title("Résolution exercice 14")
root.geometry('700x300')
root.configure(bg="bisque3")


def minitest(event):
    
    # Obtenir l'élément sélectionné
    nombre_année= int(entreeannee.get())
    main_oeuvre_cap= int(entreecapacité.get())
    if nombre_année < 3 or main_oeuvre_cap < 200:
        if nombre_année < 3:
            messagebox.showerror("Gestion de l'erreur", "Il faut au minimum 3 années")
        elif main_oeuvre_cap < 200:
            messagebox.showerror("Gestion de l'erreur", "Il faut que la main d'oeuvre minimale soit de 200")
    else:    
        select = listeCombo.get()

        result = tk.Label(root)
        tab= tk.Label(root)
        texte=tk.Label(root)


        if select == "Productivité": 
            texte['text']="Voici le tableau des capacité de production \n par années et par industries :"
            tab["text"]= md.resultat_modele_1(md.resolution_modele1_3(md.modele1,nombre_année, main_oeuvre_cap)[2], nombre_année)
            result["text"]= 'La somme des capacités de production à la dernière année \n est de ' + str(round(md.resolution_modele1_3(md.modele1,nombre_année,main_oeuvre_cap)[3],2)) +' millions'
        elif select== "Production": 
            texte['text']="Voici le tableau des production \n par années et par industries :"
            tab["text"]=md.resultat_modele_2(md.resolution_modele2(md.modele2,nombre_année,main_oeuvre_cap)[0], nombre_année)
            result["text"]= 'La somme des productions des deux dernières années \n est de ' + str(round(md.resolution_modele2(md.modele2,nombre_année,main_oeuvre_cap)[2],2)) +' millions'
        elif select=="Main d'oeuvre":
            texte['text']="Voici le tableau de la main d'oeuvre utilisée \n par années et par industries : "
            tab['text']=md.resultat_modele_3(md.resolution_modele1_3(md.modele3,nombre_année,main_oeuvre_cap)[0],md.resolution_modele1_3(md.modele3,nombre_année,main_oeuvre_cap)[1],nombre_année)
            result['text']="La somme de la main d'oeuvre pour les " + str(nombre_année)+" années \n est de: "+str(round(md.resolution_modele1_3(md.modele3,nombre_année,main_oeuvre_cap)[3],2)) +' millions'

        texte.grid(column=0,row=5)
        tab.grid(column=1,row=5,sticky="nsew")
        tab.configure(bg="bisque2")
        result.grid(column=1,row=6,sticky="nsew")
        texte.configure(bg="bisque2")
        result.configure(bg="bisque2")
        
labelChoix = tk.Label(root, text = "Choississez la variable à maximiser !")
labelChoix.configure(bg="bisque2")
labelannee=tk.Label(root,text= "Sur combien d'années voulez-vous maximiser (Renseigner un entier) ? ")
labelannee.configure(bg="bisque2")
labelcapacité=tk.Label(root,text= "Quelle est la main d'oeuvre par an (Renseigner un entier)")
labelcapacité.configure(bg="bisque2")


# 2) - créer la liste Python contenant les éléments de la liste Combobox
listeProduits=["Productivité", "Production","Main d'oeuvre"]

# 3) - Création de la Combobox via la méthode ttk.Combobox()
listeCombo = ttk.Combobox(root, values=listeProduits, background="bisque2")
entreeannee= ttk.Entry(root,background="bisque2")
entreecapacité= ttk.Entry(root,background="bisque2")


labelChoix.grid(column=0,row=2)
listeCombo.grid(column=1,row=2)

labelannee.grid(column=0,row=0)
entreeannee.grid(column=1,row=0)

labelcapacité.grid(column=0,row=1)
entreecapacité.grid(column=1,row=1)

 
# 4) - Choisir l'élément qui s'affiche par défaut
listeCombo.current(0)

listeCombo.bind("<<ComboboxSelected>>", minitest)

root.mainloop()