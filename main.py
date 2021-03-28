import PySide2

from database import *
from pathlib import Path
from glob import glob

#Temporary folder location
watchlist=[Path("C:\Assets\Cykelklubben\Leaves")]

folder=watchlist[0]

for folder in watchlist:
    files=folder.glob("*")
    print(files)



if __name__=="__main__":

    db_conn()


