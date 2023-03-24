import csv
import requests
import os
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from utils import clinks

print("Hello, welcome to the Web Book Scraping program made for the Books Online company.\n"
      "This program will scrap all required and useful data from the website http://books.toscrape.com/.\n"
      "If you have any issues with the present program please send an email at : valentin.simioni@outlook.com\n")

input("\n \n !Press enter to continue and scrap book data!")


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
STEP 1 : COLLECT CATEGORY NAMES AND LINKS THROUGH INDEX PAGE (ETL CATEGORIES)
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

url_index_page = "http://books.toscrape.com/catalogue/category/books_1/index.html"  # Web page URL
index_page = requests.get(url_index_page)  # Use of Request
soup = BeautifulSoup(index_page.content, 'html.parser')  # Use of BS4 to parser

"""
1.a Collect raw category names and links (E)
"""

dirty_category_names = []  # List of uncleaned category names
dirty_category_links = []  # List of uncleaned category links

link_tags = soup.find_all("li", class_=None)  # Search of "li" tags without class_

for links in link_tags:
    a = links.find("a")
    href = a["href"]  # Search of "href" in the "a" tags for each "li" tags

    dirty_category_names.append(a.text)  # Add of scraped but uncleaned category names
    dirty_category_links.append("http://books.toscrape.com/catalogue/category//" + href)
    # Add of scraped but uncleaned category links by joining URL + scraped HREF


"""
1.b Cleaning of raw category names and links (T)
"""

# Cleaning of raw category names and links with the use of function created
to_remove_links = {"/../": "", " ": "", "\n": ""}  # dictionary for links. Keys : to remove, Values : to replace
to_remove_names = {" ": "", "\n": ""}  # dictionary for names. Keys : to remove, Values : to replace

cleaned_links = clinks(list_to_clean=dirty_category_links, to_remove=to_remove_links)
cleaned_names = clinks(list_to_clean=dirty_category_names, to_remove=to_remove_names)

# Creation of names/links dictionary with cleaned data (L)
category_links_dictionary = {"Names": cleaned_names, "Links": cleaned_links}

# print(category_links_dictionary)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
STEP 2 : SCAN OF EACH CATEGORY LINKS BY APPLYING A SCRAPING LOOP
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""
2.a Declaration of required elements + "for" loop creation (category range iteration, == 40)
"""

elements_list = ["product_page_urls", "title", "upc", "prices_inc_tax", "prices_ex_tax", "nb_available", "rating",
                 "product description", "image", "category"]

book_qty = soup.find("form", class_="form-horizontal")  # book quantity to display scraping achievement
qty_string = book_qty.find("strong").text
qty = int(qty_string)
qty_scraped = 0

for category in (range(len(cleaned_links))):

    # First ULR == 1st dict value == "travel" category link. Will take next one after the end of the loop.
    actual_url = cleaned_links[category]
    actual_category = cleaned_names[category]
    print("\n" + actual_category + " category is being scraped")

    """
    2.b Creation of the data saving folder 
    """

    main_repository = "Extractions"
    isExist_main = os.path.exists(main_repository)
    if not isExist_main:
        os.makedirs(main_repository)

    path = "Extractions/ {} folder extract".format(cleaned_names[category])
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory if it does not exist
        os.makedirs(path)
        print(cleaned_names[category] + " folder has been created." + " Please find the folder in your env: " + path)

    # Declaration of the csv file name of the category (we use the dictionary keys)
    filename = "Extract from {}.csv".format(actual_category)

    # File path = repository path + file name
    path_file = os.path.join(path, filename)

    with open(path_file, 'w') as csv_file:  # Creation of the csv with the required elements as headers
        writer = csv.writer(csv_file, delimiter=",")
        writer.writerow(elements_list)

    """
     2.c While loop that will go in the link of the current category and will check the presence of a next link
     for the pagination. If true : next page. If false : for loop iteration
    """

    while True:
        page_request = requests.get(actual_url)  # Scan of the page of the category represented by url_actual
        soup = BeautifulSoup(page_request.content, 'html.parser')
        book_link_tags = soup.find_all("div", class_="image_container")  # Scraping of all links
        # of books on page 'n'

        page_books = []
        # list of urls for each book on the page

        for books in book_link_tags:  # We go to each book of the category, page n (n+1 if next page, n+2 ..)
            a_book = books.find("a")
            href_book = a_book["href"]  # We look for the hrefs (links)
            page_books.append("http://books.toscrape.com/catalogue/" + href_book)  # that we will join to url web page
            page_books = [e.replace('../', '') for e in page_books]

            for book, item in enumerate(page_books):
                qty_scraped += 1

            """
            2.d For each link of the list "page_books", list of all the books of the page, we will scrape all the 
            information we want by entering one by one in each book links
            """
            required_data = []

            for elements in range(len(page_books)):
                page_request = requests.get(page_books[elements])
                soup_book = BeautifulSoup(page_request.content, 'html.parser')
                product_page_url = page_books[elements]

                # Data is the scraped required data list
                # at the end of each loop, it will be saved in the csv and then cleared

                required_data.append(product_page_url)  # First element requested: url of the book

                title = soup_book.find("h1")
                title_text = title.string
                required_data.append(title_text)  # Book title

                table = soup_book.find("table", attrs={"class": "table table-striped"})
                for i in table.find_all("td"):
                    td = i.text
                    required_data.append(td)  # Upc, price, availability

                reviews = {"one star": "star-rating One",
                           "two stars": "star-rating Two",
                           "three stars": "star-rating Three",
                           "four stars": "star-rating Four",
                           "five stars": "star-rating Five"}

                rating = soup_book.find("div", class_="col-sm-6 product_main")
                for value in reviews.values():
                    rating_par = rating.find("p", class_="{}".format(value))
                    if rating_par is not None:
                        #  print("{}".format(value))
                        required_data.append("{}".format(value))

                product_description = soup_book.find("p", class_=None)
                if product_description is not None:
                    product_description = product_description.string
                    required_data.append(product_description)
                else:
                    product_description = "No description"
                    required_data.append(product_description)

                image = soup_book.find("img")
                src = image["src"]
                src_image_root = requests.compat.urljoin(product_page_url, src)
                required_data.append(src_image_root)  # url of the image taken directly from the source in the html

                required_data.append(cleaned_names[category])  # Category

                del required_data[3]  # We delete the elements in excess (because of the scraping of the table)
                del required_data[5]
                del required_data[6]

                """
                2.e Formatting of the book title to save and name the corresponding image in jpg 
                + save in the folder of the category
                """

                to_remove_title = {",": "", r"\;": "", r"\.": "", r"\:": "", r"\!": "", r"\?": "", r"\)": "", r"\(": "",
                                   " ": "_", r"\*": "_", r"\/": "_", r"\-": "_", '"': '_', "'": "_", "__": "_"}
                for char in to_remove_title.keys():
                    title_text = re.sub(char, to_remove_title[char], title_text)

                # If the title of the image > 150 characters, we shorten it to save it
                title_text = (title_text[:150] + '..') if len(title_text) > 150 else title_text

                image_save = "{}.jpg".format(title_text)
                path_image = os.path.join(path, image_save)
                webs = requests.get(src_image_root)
                with open(path_image, 'wb') as f:
                    f.write(webs.content)  # Save the jpg image in the folder

                """
                2.f Adding data by updating the initially created csv
                """

                with open(path_file, 'a', encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(required_data)
                    # print(required_data)
                    required_data.clear()
                    page_books.clear()

        next_link = soup.find("a", string="next")  # We look for a next link
        if next_link is None:  # If no next link, we go to the next category (close the while loop)
            print("{} category scraped".format(actual_category))
            remaining_qty = qty - qty_scraped
            percentage_left = (qty_scraped/qty)*100
            print(str(remaining_qty) + " book(s) left to scrap. \n" + "Achievement = " + str(percentage_left) + " %")
            break
        # Otherwise, we join the current url by pasting the href to perform the pagination
        actual_url = urljoin(actual_url, next_link["href"])
