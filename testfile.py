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

