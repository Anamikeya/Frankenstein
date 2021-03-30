import PySide2

from database import *
from pathlib import Path
from glob import glob
import numpy as np

#Temporary folder location
watchlist=[Path("C:\Assets\Cykelklubben\Leaves")]

folder=watchlist[0]

for folder in watchlist:
    files=list(folder.rglob("*"))

    #file=files[0]
    #print(file.name)

    for x in files:
        print(str(x))

    print(f'{len(files)} files total')

def scan(folder):
    print("Scanning folder")


if __name__=="__main__":
    pass
