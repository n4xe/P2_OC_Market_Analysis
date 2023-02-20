
def fonction_csv(categories,titles,prices):
    for c in categories:
        with open("Categories_", {categories}*, ".csv", "w") as csv_file:
            writer = csv.writer(csv_file, delimiter=",")
            header = ["Titles", "Prices"]
            for i in range(len(titles)):
                lign = [titles[i], prices[i]]
                writer.writerow(lign)


categories = ["Fiction, Aventure"]
titles = ["Bonjour", "Lavie"]
prices = ["52.2€", "58.2€"]
fonction_csv(categories,titles,prices)
