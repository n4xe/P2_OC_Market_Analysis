import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Déclaration des listes titres et prix

list_title = []
list_price = []

# Session conserve les cookies entre les requêtes

with requests.Session() as session:
    url_fiction_category = "http://books.toscrape.com/catalogue/category/books/fiction_10/index.html"
    page_fiction_category = requests.get(url_fiction_category)
    while True:
        page_requests = session.get(url_fiction_category)
        soup = BeautifulSoup(page_requests.content, 'html.parser')

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

        url_fiction_category = urljoin(url_fiction_category, next_link["href"])

#ecriture du csv avec les résultats des pages

print(list_title)
header = ["Titles", "Prices"]
with open('Extract_fiction.csv', 'w') as csv_file:
    writer = csv.writer(csv_file, delimiter=",")
    writer.writerow(header)
    for i in range(len(list_title)):
        lign = [list_title[i], list_price[i]]
        writer.writerow(lign)