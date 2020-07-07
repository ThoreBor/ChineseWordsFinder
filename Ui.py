from aqt import mw
from aqt.qt import *
from aqt.utils import tooltip

import os
from os.path import dirname, join, realpath
from sqlite3 import connect

from .getdata import getdata
from .freq import frequency
from .forms import wordfinder
from .WordFinder import CWF
from .HSK import HSK
from .config import save_config

db_path = join(dirname(realpath(__file__)), 'database.db')
conn = connect(db_path)
c = conn.cursor()

class start_main(QDialog):
	def __init__(self, parent=None):
		self.parent = parent
		QDialog.__init__(self, parent, Qt.Window)
		self.dialog = wordfinder.Ui_Main()
		self.dialog.setupUi(self)
		self.setupUI()

	def setupUI(self):
		all_data_list, notes_in_deck, number_of_characters, tos, filter_list, min_length, max_lenght, word_list, config, raw = getdata()

		self.dialog.pbar.setMaximum(118398)

		out = mw.col.decks.all()
		decklist = []
		subdeckslist = []
		for l in out:
		   decklist.append(l['name'])
		for i in decklist:
			if "::" in i:
				subdeckslist.append(i)
		
		out = mw.col.models.all()
		notetypelist = []
		for l in out:
		   notetypelist.append(l['name'])

		for i in notetypelist:
			self.dialog.Import_Notetype.addItem(str(i))
		
		for i in decklist:
			self.dialog.Import_Deck.addItem(str(i))

		self.dialog.HSK.setToolTip("Includes all previous levels.")
		self.dialog.Field_Number.setToolTip("0 = all fields")
		self.dialog.Max.setToolTip("0 = no limit")

		self.dialog.Notenumber_Value.setText(str(len(notes_in_deck)))
		self.dialog.Unique_Value.setText(str(number_of_characters))
		self.dialog.Notenumber_HSK_Value.setText(str(len(notes_in_deck)))
		self.dialog.Unique_HSK_Value.setText(str(number_of_characters))
		self.dialog.Unique_HSK_Value_2.setText(str(number_of_characters))
		self.dialog.Decks.setText(','.join(config["deckname"]))
		self.dialog.Subdecks.setText(','.join(config["exclude_subdeck"]))
		self.dialog.Filter.setText(','.join(config["filter"]))
		self.dialog.Field_Number.setValue(config["field_number"])
		self.dialog.Max.setValue(config["max_lenght"])
		self.dialog.Min.setValue(config["min_length"])
		self.dialog.Import_Notetype.setCurrentText(config["import_notetype"])
		self.dialog.Import_Deck.setCurrentText(config["import_deck"])

		if config["checked"] == "True":
			self.dialog.Check_Import.toggle()

		if config["tos"] == 1:
			self.dialog.TOS.setItemText(0, 'Simplified')
			self.dialog.TOS.setItemText(1, 'Traditional')
		else:
			self.dialog.TOS.setItemText(0, 'Traditional')
			self.dialog.TOS.setItemText(1, 'Simplified')


		load_hsk = "HSK " + str(config["HSK"]) 
		self.dialog.HSK.setCurrentText(load_hsk)
		self.dialog.Field1.setCurrentText(config["field_1_config"])
		self.dialog.Field2.setCurrentText(config["field_2_config"])
		self.dialog.Field3.setCurrentText(config["field_3_config"])
		self.dialog.Field4.setCurrentText(config["field_4_config"])

		self.dialog.Save_Button.clicked.connect(self.start_config)
		self.dialog.Default_Button.clicked.connect(self.default)
		self.dialog.CWF_start.clicked.connect(self.start_CWF)
		self.dialog.HSK_start.clicked.connect(self.start_HSK)
		self.dialog.Check_Import.stateChanged.connect(self.checked)

		self.start_freq()

	def start_CWF(self):
		CWF(self)

	def start_HSK(self):
		HSK(self)

	def start_freq(self):
		freq_list = frequency()
		for i in freq_list:
			self.dialog.Results_Freq.addItem(i)

	def start_config(self):
		save_config(self)

	def default(self):
		try:
			os.remove(join(dirname(realpath(__file__)), 'meta.json'))
			tooltip("Please restart the add-on.")
		except:
			tooltip("Please restart the add-on.")
	
	def checked(self):
		if self.dialog.Check_Import.isChecked():
			self.dialog.Import_Notetype.setEnabled(True)
			self.dialog.Import_Deck.setEnabled(True)
			self.dialog.Field1.setEnabled(True)
			self.dialog.Field2.setEnabled(True)
			self.dialog.Field3.setEnabled(True)
			self.dialog.Field4.setEnabled(True)
		else:
			self.dialog.Import_Notetype.setEnabled(False)
			self.dialog.Import_Deck.setEnabled(False)
			self.dialog.Field1.setEnabled(False)
			self.dialog.Field2.setEnabled(False)
			self.dialog.Field3.setEnabled(False)
			self.dialog.Field4.setEnabled(False)