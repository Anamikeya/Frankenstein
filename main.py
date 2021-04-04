import PySide2
from pathlib import Path
from glob import glob
import numpy as np
from blom import init_logger, timer
import sqlite_utils as sql
import sqlite3

# Temporary folder location
watchlist = [Path("C:\Assets\Cykelklubben\Leaves"), Path("C:\Assets\Cykelklubben\License")]
folder = watchlist[0]

l = init_logger('frankenstein')

db = sql.Database('database.db')

print(db.table_names())

#get all data
#list(db[str(folder)].rows)

def scan_all(watchlist):
    scan_timer = timer(format='s')
    l.info(f"Scanning all {len(watchlist)} folders in watchlist")

    allfiles = []

    for folder in watchlist:
        l.info(f"Scanning folder {folder}")
        files_folders = list(folder.rglob("*"))
        l.info(f"Found {len(files_folders)} files and folders total")
        files = [x for x in files_folders if x.is_file()]
        l.info(f'Found {len(files)} files')
        l.info(f'Found {len(files_folders)-len(files)} folders')


        db[str(folder)].insert({"path": 'hgfhgf'})
        for file in files:
            db[str(folder)].insert({"path": str(file)})


        for x in files:
            l.info(str(x))

    l.info(f'{len(allfiles)} files total in {scan_timer}')

    return allfiles


def scan_old(folder):
    scan_timer = timer(format='s')
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


if __name__ == "__main__":
    scan(folder)

    pass
