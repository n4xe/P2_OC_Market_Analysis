import re

text_title = "it's baby?"
to_remov = {",": "", "\;": "", "\.": "", "\:": "", "\!": "", "\?": "", "\)": "", "\(": "", " ": "_",
            "'": "_", "__": "_"}
for char in to_remov.keys():
    text_title = re.sub(char, to_remov[char], text_title)
    print(text_title)

