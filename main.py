import PySide2

from pathlib import Path
from glob import glob
import numpy as np
from blom import init_logger,get_logger

#Temporary folder location
watchlist=[Path("C:\Assets\Cykelklubben\Leaves"),Path("C:\Assets\Cykelklubben\License")]

folder=watchlist[0]

l=init_logger('frankenstein')


from time import sleep
a=timer()
sleep(5)

print(a)

def scan(folder):
    l.info("Scanning folder")

    allfiles = []

    for folder in watchlist:
        files = list(folder.rglob("*"))
        allfiles.extend(files)
        # file=files[0]
        # print(file.name)

        for x in files:
            l.info(str(x))

    l.info(f'{len(allfiles)} files total')

    return allfiles


if __name__=="__main__":
    scan(folder)

    pass
