import re

def clinks(links):
    cleaned_links = []
    to_remove = {"/../" : "", " ": "", "\n": ""}
    for l in range(len(links)):
        for chars in to_remove.keys():
            links[l] = re.sub(chars, to_remove[chars], links[l])

        cleaned_links.append(links[l])
    m = 2
    del cleaned_links[:m]
    return (cleaned_links)



