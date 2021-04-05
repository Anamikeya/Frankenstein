from datetime import datetime

from PySide6 import QtCore, QtWidgets, QtGui
from pathlib import Path
import numpy as np
from PySide6.QtGui import QIcon

from blom import init_logger, timer
import sqlite_utils as sql
import os
import sys

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


import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QTableWidget, QListWidgetItem, QLineEdit
from PySide6.QtCore import QFile, QIODevice, QSize, Qt, QCoreApplication


def infomsg(parent, msg: str):
    QMessageBox.information(parent, 'Title', msg, QMessageBox.Ok)


def errormsg(parent, msg: str = 'test'):
    QMessageBox.critical(parent, "Title", msg, QMessageBox.Ok)


def loadUi(filename):
    ui_file = QFile(filename)
    if not ui_file.open(QIODevice.ReadOnly):
        print(f"Cannot open {filename}: {ui_file.errorString()}")
        sys.exit(-1)
    loader = QUiLoader()
    window = loader.load(ui_file)
    ui_file.close()
    if not window:
        print(loader.errorString())
        sys.exit(-1)
    else:
        return window


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        loader = QUiLoader()
        loader.load('ui.ui', self)
        # load_ui('ui.ui', self)


class MainWindow_old(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        # load_ui('ui.ui', self)

        # self.l = get_logger('totalrekoll')
        self.pathWindowFeedback = 'GUI_Files/feedback.ui'

        self.icons = {
            'btnRefreshSongs': {"path": 'GUI_Files/icons/Refresh_icon.svg.png',
                                'size': (20, 20)}
        }

        # QKeySequence.Close()

        # self.errormsg('nytt error')

        self._setIcons()

        self.dialogs = list()

        # self.connector = gui_connector.UiFuncConnector(self)
        self.connectStuff()

        # Columns for the songlist
        self.columns = ["Title", "Songwriters", "Producers", "Artists", "ID"]
        self.uiPopulateSongsInit()

    def infomsg(self, msg: str):
        QMessageBox.information(self, 'Title', msg, QMessageBox.Ok)

    def errormsg(self, msg: str = 'test'):
        QMessageBox.critical(self, "Title", msg, QMessageBox.Ok)

    def _setIcons(self):
        try:
            for key, value in self.icons.items():
                path = value['path']
                size = value['size']
                self.l.info(f'setting {key} to {path} size {size}')
                iconsize = QSize(*size)
                newicon = QIcon()
                newicon.addFile(path, size=iconsize)
                self.__getattribute__(key).setIcon(newicon)
            self.l.info('all icons set')
        except Exception as e:
            self.l.error(f'Couldnt set icons\n{e}')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            print("Killing")
            self.deleteLater()
        elif event.key() == Qt.Key_Enter:
            self.proceed()
        event.accept()

    def proceed(self):
        print("Call Enter Key")

    def close(self):
        sys.exit(self.app.exec_())

    def connectStuff(self):
        # noinspection PyTypeChecker
        self.tableSongs: QTableWidget = self.findChild(QTableWidget, "tableSongs")

        # self.connector.connectBtn("btnBackup", db.savePerson) #TODO
        self.connector.connectBtn("btnRefreshSongs", self.uiPopulateSongsUpdate)
        self.connector.connectBtn("btnContacts", self.openWindowContacts)
        self.connector.connectTableDoubleClick("tableSongs", self.openWindowSong)

        # findChild(QListWidget, "listWidget").clicked.connect(printSelectedItem)

    def openWindowSong(self):
        self.l.debug('opening song')
        # self.dialogs.append(WindowSong(self.getSongFromTable(), parent=self))
        self.dialogs[-1].show()
        self.l.debug('song should be open')

    def openWindowContacts(self):
        self.l.debug('opening Contacts')
        self.dialogs.append(WindowContacts(parent=self))
        self.dialogs[-1].show()
        self.l.debug('Contacts should be open')

    def getSongFromTable(self):
        """Returns the selected song from table by looking up the id in the table and matching it in the database."""
        itemN = 0  # In case of selecting multiple items

        itemColumn = self.tableSongs.selectedItems()[itemN].column()
        itemRow = self.tableSongs.selectedItems()[itemN].row()
        itemText = self.tableSongs.selectedItems()[itemN].text()

        id = self.tableSongs.item(itemRow, 4).text()

        # QTableWidgetItem.

        self.l.debug(f'itemcolumn: {itemColumn}')
        self.l.debug(f'itemrow   : {itemRow}')
        self.l.debug(f'itemtext  : {itemText}')
        self.l.debug(f'id  : {id}')

        try:
            id = int(id)
        except:
            msg = f'couldnt convert id to int from str. Is not type: {type(id)}'
            self.l.error(msg)
            raise ValueError(msg)
        if isinstance(id, int):
            # song = sqldb.get_song(id=id)
            song = None
        else:
            msg = f'couldnt convert id to int from str. Is not type: {type(id)}'
            self.l.error(msg)
            raise ValueError(msg)

        # self.p(f"Row: {itemRow} Column: {itemColumn} Text: {itemText}")
        self.l.debug(f"{song.get('title')}")
        self.l.debug(f"song: {song}")
        return song

    def uiPopulateSongsInit(self):
        # TableWidgetFuncs.initTable(self.tableSongs, self.columns)
        self.uiPopulateSongsAdd()

    def uiPopulateSongsAdd(self):
        self.l.debug('Adding songs to songs view')
        items = ['title', 'songwriters', 'producers', 'artists', 'id']
        # TableWidgetFuncs.updateTable(self.tableSongs, items=items)

    def uiPopulateSongsUpdate(self):
        self.l.debug('Updateing songs view')

        # self.table.clear()

        self.l.debug(f'Row count: {self.tableSongs.rowCount()}')
        # Remove all columns

        for i in range(self.tableSongs.rowCount()):
            self.l.debug(f'removing row {0} this many times: {i}')
            self.tableSongs.removeRow(0)

        self.uiPopulateSongsAdd()


class WindowContacts(QDialog):
    class QListPerson(QListWidgetItem):
        """A person object but that fit inside a QListWidget"""

        def __init__(self, dicten):
            firstname = dicten.get("firstname")
            lastname = dicten.get("lastname")

            niceName = f'{firstname.capitalize()}'

            if lastname:
                niceName += f' {lastname.capitalize()}'

            padding = 30

            id_string = f'({str(dicten.get("id"))})'
            spaces = " " * (padding - len(niceName))
            niceName += spaces + id_string

            print(niceName)

            super().__init__(niceName)

            self.contact = dicten


class WindowAddPeople(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        # load_ui("GUI_Files/Add Person.ui", self)

        # self.l = get_logger('totalrekoll')

        self.l.debug('adding new person')
        # self.person = Person()
        # self.l.debug(f'id for person: {self.person._id}')

        self._updatePersonsList()

        self.buttonBox.accepted.connect(self.ok)
        self.buttonBox.rejected.connect(self.cancel)
        self.btnNewPerson.clicked.connect(self.NewPerson)
        self.listPeople.itemDoubleClicked.connect(self.loadPersonFromList)
        self.btnRemovePerson.clicked.connect(self.removePerson)
        self.btnSavePerson.clicked.connect(self.savePerson)
        # self.btnFindMatch.clicked.connect(self._setPersonToFormData)

    def NewPerson(self):
        self.clearFields()

    def clearFields(self):
        self.l.debug(f'Clearing all fields')

        textfields = [self.firstname,
                      self.lastname,
                      self.emails,
                      self.phones,
                      self.instagram,
                      self.tiktok,
                      self.snapchat,
                      self.facebook,
                      self.youtube,
                      self.works]

        checkboxes = [
            self.checkSongwriter,
            self.checkProducer,
            self.checkArtist,
            self.checkAnR,
            self.checkManager,
            self.checkOther,
            self.checkBirthday

        ]
        a = QLineEdit()

        for x in textfields:
            # x.setText('')
            x.clear()
            # x.update()
            # x.selectAll()
            # x.deselect()

        for x in checkboxes:
            x.setChecked(False)

        self.birthday.setDate(datetime.now())

        QCoreApplication.processEvents()
        self.update()

    def _setPersonToFormData(self):

        self.l.info(f'setting person to form data')
        person = {}
        self.l.debug(person)
        for key, val in self.mapping.items():
            if val:
                person[key] = val

        if self.checkBirthday.isChecked():
            person['birthday'] = self.birthday.date().toPython()

        return person

    def _loadPerson(self, selected):
        """setting all fields to person loaded"""

        self.l.debug(f'Loading person with id {selected.get("id")}')

        self.firstname.setText(selected.get('firstname'))
        self.lastname.setText(selected.get('lastname'))
        # self.emails.setText(_loadListToCommaString(selected.get('email_adresses')))
        # self.phones.setText(_loadListToCommaString(selected.get('phone_numbers')))
        self.instagram.setText(selected.get('instagram'))
        self.tiktok.setText(selected.get('tiktok'))
        self.snapchat.setText(selected.get('snapchat'))
        self.facebook.setText(selected.get('facebook'))
        self.youtube.setText(selected.get('youtube'))
        # self.works.setText(_loadListToCommaString(selected.get('works')))

        self.checkSongwriter.setChecked(selected.get('is_songwriter'))
        self.checkProducer.setChecked(selected.get('is_producer'))
        self.checkArtist.setChecked(selected.get('is_artist'))
        self.checkAnR.setChecked(selected.get('is_anr'))
        self.checkManager.setChecked(selected.get('is_manager'))
        self.checkOther.setChecked(selected.get('is_other'))

        if selected.get('birthday'):
            self.checkBirthday.setChecked(1)
            date = datetime.strptime(selected.get('birthday'), '%Y-%m-%d')
            self.birthday.setDate(date)

    def _updatePersonsList(self):
        self.listPeople.clear()

        # for x in sqldb.get_all_contacts():
        #    self.listPeople.addItem(self.QListPerson(x))

    def getSelectedPerson(self):
        """Returns selected person and sets self.id to selected person"""
        selected = self.listPeople.selectedItems()
        if len(selected) > 1:
            self.l.warning('selected more than one item, setting selected to first item')
        selected = selected[0]
        self.id = selected.contact['id']
        return selected

    def loadPersonFromList(self):

        selected = self.getSelectedPerson()
        self.l.info(f'Loading Person {selected}')
        self._loadPerson(selected.contact)

    def savePerson(self):
        person = self._setPersonToFormData()
        self.l.info(f'Save person {person}')

        try:
            person['id']
            del person['id']
        except KeyError:
            pass

        # sqldb.add_contact(**person)

        self._updatePersonsList()

    def removePerson(self):
        selected = self.getSelectedPerson()

        try:
            self.l.info(f'Removing Person {selected}')
            # sqldb.del_contact(id=selected.contact['id'])
            self._updatePersonsList()
        except KeyError:
            raise TypeError('Selected has no ID')

    def ok(self):
        l.debug('closing windowaddpeople')
        pass

    def cancel(self):
        self.l.info('cancelling')


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = loadUi('ui.ui')
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
