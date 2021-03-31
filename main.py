import PySide2

from database import *
from pathlib import Path
from glob import glob
import numpy as np

#Temporary folder location
watchlist=[Path("C:\Assets\Cykelklubben\Leaves"),Path("C:\Assets\Cykelklubben\License")]

folder=watchlist[0]



def scan(folder):
    print("Scanning folder")
    allfiles = []

    for folder in watchlist:
        files = list(folder.rglob("*"))
        allfiles.extend(files)
        # file=files[0]
        # print(file.name)

        for x in files:
            print(str(x))

    print(f'{len(allfiles)} files total')

    return allfiles


if __name__=="__main__":
    pass
