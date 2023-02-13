import csv
import requests
from bs4 import BeautifulSoup

url_book_1 = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
page_book_1 = requests.get(url_book_1)
soup = BeautifulSoup(page_book_1.content, 'html.parser')

title = soup.find_all("h1")
for titles in title:
    print(titles.string)

price = soup.find_all("p", class_="price_color")
for prices in price:
    print(prices.string)
header = ["title", "price"]

with open('Extract.csv', 'w') as csv_file:
    writer = csv.writer(csv_file, delimiter=",")
    writer.writerow(header)

    for title, price in zip(titles, prices):
        lign = [title, price]
        writer.writerow(lign)