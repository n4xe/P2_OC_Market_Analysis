import re

def clinks(list_to_clean, to_remove):
    cleaned_list = []
    #
    for l in range(len(list_to_clean)):
        for chars in to_remove.keys():
            list_to_clean[l] = re.sub(chars, to_remove[chars], list_to_clean[l])

        cleaned_list.append(list_to_clean[l])
    m = 2
    del cleaned_list[:m]
    return (cleaned_list)