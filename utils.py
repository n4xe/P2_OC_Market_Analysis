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

"""
#python program to check if a directory exists
import os
path = "pythonprog"
# Check whether the specified path exists or not
isExist = os.path.exists(path)
if not isExist:

   # Create a new directory because it does not exist
   os.makedirs(path)
   print("The new directory is created!")
"""


