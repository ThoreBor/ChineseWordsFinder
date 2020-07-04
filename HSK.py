from sqlite3 import connect
from .getdata import getdata
from .import_file import importfile
from os.path import dirname, join, realpath
from PyQt5 import QtCore, QtGui, QtWidgets

db_path = join(dirname(realpath(__file__)), 'database.db')
conn = connect(db_path)
c = conn.cursor()

def HSK(self):
	self.dialog.Results_HSK.clear()
	all_data_list, notes_in_deck, number_of_characters, tos, filter_list, min_length, max_lenght, word_list, config, raw = getdata()
	HSK = config['HSK']
	hsk_list = []
	for i in range(HSK + 1):
		hsk_list.append("HSK "+str(i))
	anki_file =  open(join(dirname(realpath(__file__)), 'MissingHSK.txt'), "w", encoding="utf-8")
	counter = 0
	found = 0
	c.execute('SELECT * FROM HSK ORDER BY HSK ASC')

	hsk_word_list = []
	for row in c.fetchall():
			counter = counter + 1
			hanzi = row[tos]
			hsk_word_list.append(hanzi)
			hsk_lvl = row[4]
			if hanzi not in word_list and hsk_lvl in hsk_list:
				traditional = row[0]
				simplified = row[1]
				p = row[2]
				english = row[3]
				english = english.replace("\n", "")
				lvl = row[4]
				found = found + 1

				if self.dialog.Field1.currentText() == "Simplified":
					Field1_content = simplified
				if self.dialog.Field1.currentText() == "Traditional":
					Field1_content = traditional
				if self.dialog.Field1.currentText() == "Pinyin":
					Field1_content = p
				if self.dialog.Field1.currentText() == "English":
					Field1_content = english

				if self.dialog.Field2.currentText() == "Simplified":
					Field2_content = simplified
				if self.dialog.Field2.currentText() == "Traditional":
					Field2_content = traditional
				if self.dialog.Field2.currentText() == "Pinyin":
					Field2_content = p
				if self.dialog.Field2.currentText() == "English":
					Field2_content = english

				if self.dialog.Field3.currentText() == "Simplified":
					Field3_content = simplified
				if self.dialog.Field3.currentText() == "Traditional":
					Field3_content = traditional
				if self.dialog.Field3.currentText() == "Pinyin":
					Field3_content = p
				if self.dialog.Field3.currentText() == "English":
					Field3_content = english
				if self.dialog.Field3.currentText() == "Nothing":
					Field3_content = ""

				if self.dialog.Field4.currentText() == "Simplified":
					Field4_content = simplified
				if self.dialog.Field4.currentText() == "Traditional":
					Field4_content = traditional
				if self.dialog.Field4.currentText() == "Pinyin":
					Field4_content = p
				if self.dialog.Field4.currentText() == "English":
					Field4_content = english
				if self.dialog.Field4.currentText() == "Nothing":
					Field4_content = ""
				Card = str(Field1_content + "\t" + Field2_content + "\t" + Field3_content + "\t" + Field4_content + "\n")
				anki_file.write(Card)
				self.dialog.Found_HSK_Value.setText(str(found))

				rowPosition = self.dialog.Results_HSK.rowCount()
				self.dialog.Results_HSK.setColumnCount(5)
				self.dialog.Results_HSK.insertRow(rowPosition)

				self.dialog.Results_HSK.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(lvl))
				self.dialog.Results_HSK.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(traditional))
				self.dialog.Results_HSK.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(simplified))
				self.dialog.Results_HSK.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(p))
				self.dialog.Results_HSK.setItem(rowPosition, 4, QtWidgets.QTableWidgetItem(english))
	
	self.dialog.Results_HSK.resizeColumnsToContents()
	anki_file.close()
	if config["checked"] == "True":
		importfile("MissingHSK.txt", config["import_deck"], config["import_notetype"])