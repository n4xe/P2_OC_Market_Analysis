import csv
import requests
from bs4 import BeautifulSoup

url_music_category = "http://books.toscrape.com/catalogue/category/books/music_14/index.html"
page_music_category = requests.get(url_music_category)
soup = BeautifulSoup(page_music_category.content, 'html.parser')
print(page_music_category)

title = soup.find_all("h3")
list_title = []
for titles in title:
    list_title.append(titles.string)

price = soup.find_all("p", class_="price_color")
list_price = []
for prices in price:
    list_price.append(prices.string)

header = ["title", "price"]
with open('Extract_music.csv', 'w') as csv_file:
    writer = csv.writer(csv_file, delimiter=",")
    writer.writerow(header)
    for i in range(len(list_title)):
        lign = [list_title[i], list_price[i]]
        writer.writerow(lign)