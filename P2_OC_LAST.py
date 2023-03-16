import csv
import requests
import os
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from function_clean_links import clinks
from function_clean_names import cnames



"""
Listage de tous les liens de la page d'accueil qui me serviront
à les visiter 1 par 1 puis à récupérer les données par lien
"""

url_index_page = "http://books.toscrape.com/catalogue/category/books_1/index.html" #the welcome page
index_page = requests.get(url_index_page)
soup = BeautifulSoup(index_page.content, 'html.parser')

"""
Je créé un dictionnaire qui récupèrera les liens de chaque catégories
avec pour clé les catégories et pour valeur les liens
"""
dirty_category_names = []  # il faudra nettoyer les bouts de liens html récupérés pour qu'ils soient fonctionnels
dirty_category_links = []

link_tags = soup.find_all("li", class_=None)

for links in link_tags:
    a = links.find("a")
    href = a["href"]
    dirty_category_names.append(a.text)
    dirty_category_links.append("http://books.toscrape.com/catalogue/category//" + href)  # Ajout des liens dans la liste

# Nettoyage des liens et des noms créés pour qu'ils soient fonctionnels
cleaned_names = cnames(names=dirty_category_names)
cleaned_links = clinks(links=dirty_category_links)

category_links_dictionary = {"Names": cleaned_names, "Links": cleaned_links}
print(category_links_dictionary)

"""
Création d'une boucle for
qui viendra appliquer pour chaque valeur du dictionnaire (lien des catégories) le code dans la boucle for
"""
liste_elements = ["product_page_urls", "upc","titles","prices_inc_tax","prices_ex_tax","nb_available",
                  "product description","categories","review","image"]