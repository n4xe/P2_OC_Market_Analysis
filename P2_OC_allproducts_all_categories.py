import csv
import requests
import os
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from function_clean_links import clinks
from function_clean_names import cnames
#-*- coding: utf-8 -*-


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
ETAPE 1 : RECUPERER LES CATEGORIES ET LES LIENS VIA LA PAGE D'ACCUEIL (INDEX) 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

url_index_page = "http://books.toscrape.com/catalogue/category/books_1/index.html"  # URL de la page
index_page = requests.get(url_index_page)  # Utilisation de Request
soup = BeautifulSoup(index_page.content, 'html.parser')  # Utilisation de BS4 pour parser

"""
1.a Récupérations des noms et des liens de chaque catégorie
"""

dirty_category_names = []  # Liste de noms de catégories non nettoyés
dirty_category_links = []  # Liste de liens de catégories non nettoyés

link_tags = soup.find_all("li", class_=None)  # Recherche de toutes les balises "li" qui n'ont pas de classe

for links in link_tags:
    a = links.find("a")
    href = a["href"]  # Recherche des href dans les balises a pour chacunes des balises "li"

    dirty_category_names.append(a.text)  # Ajout des noms de catégories non nettoyées
    dirty_category_links.append("http://books.toscrape.com/catalogue/category//" + href)
    # Ajout des liens non nettoyés dans la liste

"""
1.b Nettoyage des noms et des liens de chaque catégorie
"""

# Nettoyage des liens et des noms créés pour qu'ils soient fonctionnels grâce à des fonctions créées
cleaned_names = cnames(names=dirty_category_names)
cleaned_links = clinks(links=dirty_category_links)

# Création du dictionnaire Nom/Liens
category_links_dictionary = {"Names": cleaned_names, "Links": cleaned_links}

# print(category_links_dictionary)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
ETAPE 2 : PARCOURIR CHAQUE LIEN ET APPLIQUER UNE BOUCLE DE SCRAPPING 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""
2.a Déclaration des éléments voulus + Création de la boucle for (itération range catégorie, soit 40)
"""

liste_elements = ["product_page_urls", "upc", "title", "prices_inc_tax", "prices_ex_tax", "nb_available",
                  "product description", "category", "review", "image"]

for category in (range(len(cleaned_links))):

    # Premier URL = 1ere valeur du dictionnaire soit le lien de la catégorie 'travel'
    url_actuel = cleaned_links[category]
    actual_category = cleaned_names[category]
    print(actual_category + " category is being scrapped")

    """
    2.b Création du dossier de récupération des fichiers + images
    """

    repository_folder = \
        (r"C:\Users\valen\OneDrive\Bureau\extract books csv\{} folder extract".format(cleaned_names[category]))

    os.makedirs(repository_folder, exist_ok=True)  # Si le dossier existe déjà, alors cela ne le recréé pas
    print\
        (cleaned_names[category] + " folder has been created" + " Please find the link after : " + repository_folder)

    # Déclaration du nom du fichier csv de la catégorie (on utilise les clés du dictionnaire)
    filename = "Extract from {}.csv".format(actual_category)

    # Chemin = chemin du repository + nom du fichier
    path = os.path.join(repository_folder, filename)

    with open(path, 'w', encoding="utf-8") as csv_file:  # Création du csv avec comme en-tête les éléments voulus
        writer = csv.writer(csv_file, delimiter=",")
        writer.writerow(liste_elements)

    """
     2.c Boucle tant que qui ira dans les liens de chaque catégories qui viendra verifier la présence d'un lien next
     pour la pagination
    """

    while True:
        page_request = requests.get(url_actuel)  # Parcours de la page de la catégorie représentée par url_actuel
        soup = BeautifulSoup(page_request.content, 'html.parser')
        book_link_tags = soup.find_all("div", class_="image_container") # scraping de tous les liens
        # des livres de la page n


        page_books = []
        #  future liste des urls de chaque livre de la page

        for books in book_link_tags:  # on va dans chacun des livres de la catégorie, page n
            a_book = books.find("a")
            href_book = a_book["href"]  # puis on cherche les hrefs (liens)
            page_books.append("http://books.toscrape.com/catalogue/" + href_book)  # que l'on collera à la suite
            page_books = [e.replace('../', '') for e in page_books]

            """
                2.d Pour chaque liens de la liste "page_books", soient tous les livres d'une page, il faudra
                scrapper toutes les infos voulues en rentrant un par un dans chaque livre
            """

            for elements in range(len(page_books)):
                page_request = requests.get(page_books[elements])
                soup_book = BeautifulSoup(page_request.content, 'html.parser')
                product_page_url = page_books[elements]

                data = []
                data.append(product_page_url)

                table = soup_book.find("table", attrs={"class": "table table-striped"})
                for i in table.find_all("td"):
                    td = i.text
                    data.append(td)
                title = soup_book.find("h1")
                ctitle = title.string
                data.append(ctitle)

                product_description = soup_book.find("p", class_=None)
                data.append(product_description)

                image = soup_book.find("img")
                src = image["src"]
                src_image_root = requests.compat.urljoin(product_page_url, src)
                data.append(src_image_root)
                print(data)

                to_remov = {",": "", "\;": "", "\.": "", "\:": "", "\!": "", "\?": "", "\)": "", "\(": "", " ": "_",
                            "\*": "_", "\/": "_", "\-":"_", '"':'_', "'": "_", "__": "_"}
                for char in to_remov.keys():
                    ctitle = re.sub(char, to_remov[char], ctitle)

                ctitle = (ctitle[:150] + '..') if len(ctitle) > 150 else ctitle

                image_save = "{}.jpg".format(ctitle)
                path_image = os.path.join(repository_folder, image_save)
                webs = requests.get(src_image_root)
                with open(path_image, 'wb') as f:
                    f.write(webs.content)

                data.append(cleaned_names[category])

                with open(path, 'a', encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(data)
                    data.clear()
                    page_books.clear()

        next_link = soup.find("a", text="next")
        if next_link is None:
            print("{} category scraped".format(actual_category))
            break
        url_actuel = urljoin(url_actuel, next_link["href"])