import PySide2
from pathlib import Path
from glob import glob
import numpy as np
from blom import init_logger,timer
import sqlite_utils as sql
import sqlite3

#Temporary folder location
watchlist=[Path("C:\Assets\Cykelklubben\Leaves"),Path("C:\Assets\Cykelklubben\License")]
folder=watchlist[0]

l=init_logger('frankenstein')

db=sql.Database('database.db')


db["cats"].create({
    "id": int,
    "name": str,
    "weight": float,
}, pk="id")



print(db.table_names())

def scan(folder):
    scan_timer=timer(format='s')
    l.info("Scanning folder")

    allfiles = []

    for folder in watchlist:
        files = list(folder.rglob("*"))
        allfiles.extend(files)
        # file=files[0]
        # print(file.name)

        for x in files:
            l.info(str(x))

    l.info(f'{len(allfiles)} files total in {scan_timer}')

    return allfiles



def scan_old(folder):
    scan_timer=timer(format='s')
    l.info("Scanning folder")

    allfiles = []

    for folder in watchlist:
        files = list(folder.rglob("*"))
        allfiles.extend(files)
        # file=files[0]
        # print(file.name)

        for x in files:
            l.info(str(x))

    l.info(f'{len(allfiles)} files total in {scan_timer}')

    return allfiles


if __name__=="__main__":
    scan(folder)

    pass
