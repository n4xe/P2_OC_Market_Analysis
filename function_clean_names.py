import re
def cnames(names):
    cleaned_names = []
    to_remove = {" ": "", "\n": ""}

    for n in range(len(names)):
        for chars in to_remove.keys():
            names[n] = re.sub(chars, to_remove[chars], names[n])
        cleaned_names.append(names[n])
    m = 2
    del cleaned_names[:m]
    return (cleaned_names)