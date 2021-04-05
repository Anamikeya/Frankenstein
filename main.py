import PySide2
from pathlib import Path
from glob import glob
import numpy as np
from blom import init_logger, timer
import sqlite_utils as sql
import sqlite3

l = init_logger('frankenstein')
db = sql.Database('database.db')
watchlist = [Path("C:\Assets\Cykelklubben\Leaves"), Path("C:\Assets\Cykelklubben\License"),
             Path("Y:\Models"), Path("Y:\Footage"), Path("Y:\Other"), Path("Y:\HDRI"), Path("Y:\previews"),
             Path("Y:\Sound FX"), Path("Y:\Textures")]


def scan_all(watchlist):
    l.info(f"Scanning all {len(watchlist)} folders in watchlist")
    timer_scan_all_total = timer()

    for i, folder in enumerate(watchlist):
        l.info('#' * 50)
        l.info(f"Scanning folder {i} of {len(watchlist)}  {folder}")
        timer_scan = timer()
        files_folders = list(folder.rglob("*"))
        l.info(f"Found {len(files_folders)} files and folders total in {timer_scan}")

        # l.info('TODO cleaning db if exists')

        l.info(f'Checking which is file and folder (can prob be optimized)')
        timer_filefolder = timer()
        files = [x for x in files_folders if x.is_file()]
        l.info(f'Found {len(files)} files')
        l.info(f'Found {len(files_folders) - len(files)} folders')
        files_clean = [{'path': str(x)} for x in files]
        l.info(f'Took {timer_filefolder}')

        l.info('Writing to db')
        timer_db_write = timer()
        db[str(folder)].insert_all(files_clean)
        l.info(f'Took {timer_db_write}')

    l.info(f'Total took {timer_scan_all_total}')


def scan_folder_disk(folder):
    timer_scan_folder_disk = timer()
    l.info(f'Scanning folder {str(folder)}')
    files_folders = list(folder.rglob("*"))
    l.info(f'Scan took {timer_scan_folder_disk}')
    return files_folders


def scan_folder_db(folder):
    timer_scan_folder_db = timer()
    l.info(f'Scanning db for folder {str(folder)}')
    files = list(db[str(folder)].rows_where(select="path"))
    files_list = [x['path'] for x in files]
    l.info(f'Scan took {timer_scan_folder_db}')
    return files_list


if __name__ == "__main__":
    # Temporary folder location

    path=[Path('/Users/blom/Pictures')]

    scan_all(path)
    #scan_all(watchlist)
    """
    folder=Path("Y:\Models")

    a=scan_folder_disk(folder)

    #write a to db
    files_clean = [{'path': str(x)} for x in a]
    db[str(folder)].insert_all(files_clean)

    b=scan_folder_db(folder)


    len(a)
    len(b)
    
    """
