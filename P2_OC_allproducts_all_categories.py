import csv
import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

"""
Listage de tous les liens de la page d'accueil qui me serviront
à les visiter 1 par 1 puis à récupérer les données par lien
"""

url_index_page = "http://books.toscrape.com/catalogue/category/books_1/index.html"
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
    dirty_category_links.append("http://books.toscrape.com/catalogue/category/" + href)  # Ajout des liens dans la liste
    dirty_category_names.append(a.text)

    # Nettoyage des liens créés pour qu'ils soient fonctionnels
    clean_category_links = [e.replace('../', '') for e in dirty_category_links]
    clean_n_category_names = [e.replace(" ", "") for e in dirty_category_names]
    clean_category_names = [e.replace('\n', '') for e in clean_n_category_names]
    n = 2
    del clean_category_links[:n]  # Suppression des deux premiers éléments de la liste qui ne sont pas des catégories
    del clean_category_names[:n]

# Création d'un dictionnaire - ajout des items de la liste de liens comme valeurs et des items de la liste de comme clés
links_per_categories_dic = {}
for key in clean_category_names:
    for value in clean_category_links:
        links_per_categories_dic[key] = value
        clean_category_links.remove(value)
        break

# Déclaration des listes titres, prix et images
list_title = []
list_price = []
list_image = []

"""
Création d'une boucle for
qui viendra appliquer pour chaque valeur du dictionnaire (lien des catégories) le code dans la boucle for
"""
for items in links_per_categories_dic.items():
    url_actuel = items[1]  # Premier URL = 1ere valeur du dictionnaire, soit le lien de la catégorie 'travel'
    while True:  # Boucle while true qui viendrant confirmer si il y a un lien "next" ou non pour la pagination
        page_request = requests.get(url_actuel)
        soup = BeautifulSoup(page_request.content, 'html.parser')

        title = soup.find_all("h3")

        for titles in title:
            list_title.append(titles.string)  # Ajout des titres de la page visitée (grace au lien)

            # Nettoyage des titres pour les utiliser comme nommage des images
            name_file = [e.replace(' ...', '') for e in list_title]
            name_file_1 = [e.replace(' ', '_') for e in name_file]
            name_file_2 = [e.replace("'", '_') for e in name_file_1]
            name_file_3 = [e.replace("’", '_') for e in name_file_2]
            name_file_4 = [e.replace(",", '_') for e in name_file_3]
            name_file_5 = [e.replace(":", '') for e in name_file_4]
            name_file_6 = [e.replace(".", '') for e in name_file_5]
            name_file_7 = [e.replace("/", '') for e in name_file_6]
            name_file_8 = [e.replace("?", '') for e in name_file_7]
            name_file_9 = [e.replace("*", '') for e in name_file_8]
            name_file_10 = [e.replace('"', '') for e in name_file_9]

        price = soup.find_all("p", class_="price_color")  # Ajout des prix de la page visitée (grace au lien)
        for prices in price:
            list_price.append(prices.string)

        image = soup.find_all("div", class_="image_container")  # Ajout des images de la page visitée (grace au lien)
        for images in image:
            b = images.find("img")
            src_image = b["src"]
            # Récupération du lien url racine présent dans le html
            src_image_root = requests.compat.urljoin(url_actuel, src_image)
            list_image.append(src_image_root)

        """
        Recherche dans les balises <a> le texte 'next' avec bs
        qui nous permettra de coller le chemin du next à notre url initial grâce à urljoin
        """

        next_link = soup.find("a", text="next")
        if next_link is None:  # S'il n y a pas de lien next, alors

            # Création d'un dossier de la catégorie concernée (en premier Travel)
            repository_folder = (r"C:\Users\valen\OneDrive\Bureau\extract books csv\{} folder extract".format(items[0]))
            os.makedirs(repository_folder, exist_ok=True)  # S'il existe déjà, alors cela ne le recréé pas
            # Déclaration du nom du fichier csv de la catégorie (on utilise les clés du dictionnaire)
            filename = "Extract {}.csv".format(items[0])
            # Le chemin sera donc la composition du chemin du dossier + le nom du fichier
            path = os.path.join(repository_folder, filename)
            header = ["Titles", "Prices"]  # Headers de mon CSV

            with open(path, 'w') as csv_file:  # Création du CSV
                writer = csv.writer(csv_file, delimiter=",")
                writer.writerow(header)

                for i in range(len(list_title)):
                    lign = [list_title[i], list_price[i]]  # Ecriture des titres et prix
                    writer.writerow(lign)
                    webs = requests.get(list_image[i])  # Récupération des images affiliées au titre dans 'list_image'
                    image_name = "{}.jpg".format(name_file_10[i])  # Nommage conventionel de l'image 'name_file_10'
                    path_image = os.path.join(repository_folder, image_name)

                    """
                    A chaque titre/prix écrit dans le csv
                    l'image en jpg est créée dans le dossier de la catégorie du livre avec pour nom le nom du livre
                    """
                    with open(path_image, 'wb') as f:
                        f.write(webs.content)

            # Suppression des données des listes pour recommencer la boucle avec nouvelle catégorie
            list_title.clear()
            list_price.clear()
            list_image.clear()

            """
                Break répond à isNone :
                s'il n'ya pas de next link, on ne recommence pas la boucle et on change de catégorie
                """
            break

        """
            Sinon, on recommence la boucle avec le next link
            qui est un url join de l'url de la catégorie et de l'url de la page suivante
            """
        url_actuel = urljoin(url_actuel, next_link["href"])
