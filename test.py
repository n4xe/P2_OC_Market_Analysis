import re
a = '''hello? there A-Z-R_T(,**), world, welcome to python.
this **should? the next line#followed- by@ an#other %million^ %%like $this.'''

for k in a.split("\n"):
    print(re.sub(r"[^a-zA-Z0-9]+", ' ', k))