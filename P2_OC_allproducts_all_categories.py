import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

#je liste tous les liens de la page d'accueil qui me serviront à les visiter 1 par 1 puis à récupérer les données par lien

url_index_page = "http://books.toscrape.com/catalogue/category/books_1/index.html"
index_page = requests.get(url_index_page)
soup = BeautifulSoup(index_page.content, 'html.parser')

#Je créé un dictionnaire qui récupèrera les liens de chaque catégories avec pour clé les catégories et pour valeur les liens
dirty_category_names = []
dirty_category_links = []
link_tags = soup.find_all("li", class_=None)
for links in link_tags:
    a = links.find("a")
    href = a["href"]
    dirty_category_links.append("http://books.toscrape.com/catalogue/category/"+ href)
    dirty_category_names.append(a.text)
    clean_category_links = [e.replace('../', '') for e in dirty_category_links]
    clean_n_category_names = [b.replace(" ", "") for b in dirty_category_names]
    clean_category_names = [b.replace('\n', '') for b in clean_n_category_names]
    n = 2
    del clean_category_links[:n]
    del clean_category_names[:n]
#print(clean_category_links)
#print(clean_category_names)

links_per_categories_dic = {}
for key in clean_category_names:
    for value in clean_category_links:
        links_per_categories_dic[key] = value
        clean_category_links.remove(value)
        break
print(links_per_categories_dic)
'''
with open('Categories_links.csv', 'w') as csv_file_link:
    writer = csv.writer(csv_file_link, delimiter=",")
    for i in range(len(list_categories_cleaned)):
        lign = [list_categories_cleaned[i]]
        writer.writerow(lign)
'''

# Déclaration des listes titres et prix
list_title = []
list_price = []

# Session conserve les cookies entre les requêtes
for items in links_per_categories_dic.items():
    url_actuel = items[1]
    while True:
        page_request = requests.get(url_actuel)
        soup = BeautifulSoup(page_request.content, 'html.parser')

        title = soup.find_all("h3")
        for titles in title:
            list_title.append(titles.string)
        price = soup.find_all("p", class_="price_color")
        for prices in price:
            list_price.append(prices.string)

#on cherche dans les balises <a> le texte next avec bs, qui nous permettra de le coller à notre url initial grâce à urljoin
        next_link = soup.find("a", text="next")
        if next_link is None:
            break

        url_actuel = urljoin(url_actuel, next_link["href"])
        print (url_actuel)




#ecriture du csv avec les résultats des pages
header = ["Titles", "Prices"]
with open('Extracttest.csv', 'w') as csv_file:
    writer = csv.writer(csv_file, delimiter=",")
    writer.writerow(header)
    for i in range(len(list_title)):
        lign = [list_title[i], list_price[i]]
        writer.writerow(lign)
