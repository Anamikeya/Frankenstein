from datetime import datetime

from PySide6 import QtCore, QtWidgets, QtGui
from pathlib import Path
import numpy as np
from PySide6.QtGui import QIcon, QPixmap

from blom import init_logger, timer
import sqlite_utils as sql
import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QTableWidget, QListWidgetItem, QLineEdit, \
    QFileDialog
from PySide6.QtCore import QFile, QIODevice, QSize, Qt, QCoreApplication, QRectF, Slot

from filepickertest import ImageViewer
from ui_loader import load_ui


l = init_logger('frankenstein')
db = sql.Database('database.db')

def infomsg(parent, msg: str):
    QMessageBox.information(parent, 'Title', msg, QMessageBox.Ok)

def errormsg(parent, msg: str = 'test'):
    QMessageBox.critical(parent, "Title", msg, QMessageBox.Ok)

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        loader = QUiLoader()
        #loader.load('ui.ui', self)
        load_ui('ui.ui', self)
        self._connectAll()
        self._populate_watchlist()

    def _connectAll(self):
        self.btn_add_folder.clicked.connect(self.add_folder)

    def _populate_watchlist(self):
        items=scan_folder_db('watchlist')
        self.watchlist.addItems(items)

    def showImage(self):
        image_path, _ = QFileDialog.getOpenFileName(self, self.tr("Load Image"), self.tr("~/Desktop/"), self.tr("Images (*.jpg)"))
        pixmap = QPixmap(image_path)
        self.labelimage.setPixmap(pixmap)

    def add_folder(self):
        path=QFileDialog.getExistingDirectory(self, self.tr("Load Folder"))

        if path:
            clock = timer()
            l.info(f'Adding {1} folder to watchlist')
            db['watchlist'].insert_all([{'path':str(path)}])
            l.info(f"Added {1} folder in {clock}")

        else:
            l.info('canceldd adding folder')

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

def watchlist_del():
    pass
def watchlist_add():
    pass

if __name__ == "__main__":
    watchlist = [Path("C:\Assets\Cykelklubben\Leaves"), Path("C:\Assets\Cykelklubben\License"),
                 Path("Y:\Models"), Path("Y:\Footage"), Path("Y:\Other"), Path("Y:\HDRI"), Path("Y:\previews"),
                 Path("Y:\Sound FX"), Path("Y:\Textures")]

    folder=Path('scan_folder_db("Y:\Models")')


    app = QApplication(sys.argv)

    window = MainWindow()

    #window.watchlist.addItems()
    #window = loadUi('ui.ui')
    window.show()

    sys.exit(app.exec_())

    # Temporary folder location
    """
    path=[Path('/Users/blom/Pictures')]

    scan_all(path)
    
    """

    # scan_all(watchlist)
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
