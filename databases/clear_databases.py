"""This module is a helper function for clearing databases"""

import os

cwd = os.getcwd()
files = os.listdir(cwd)

for i in files:
    if i.endswith(".db"):
        os.remove(i)
