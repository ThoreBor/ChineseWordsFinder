from sqlite3 import connect
from .getdata import getdata
from .import_file import importfile
from os.path import dirname, join, realpath
from PyQt5 import QtCore, QtGui, QtWidgets

db_path = join(dirname(realpath(__file__)), 'database.db')
conn = connect(db_path)
c = conn.cursor()

def CWF(self):
	self.dialog.Results.setRowCount(0)
	found = 0
	counter = 0
	all_data_list, notes_in_deck, number_of_characters, tos, filter_list, min_length, max_lenght, word_list, config, raw = getdata()
	if filter_list == [""]:
		filter_list = []
	anki_file =  open(join(dirname(realpath(__file__)), 'WordsFound.txt'), "w", encoding="utf-8")


	c.execute('SELECT * FROM dictionary ORDER BY freq DESC')

	for row in c.fetchall():
		trad = row[tos]
		counter = counter + 1
		self.dialog.pbar.setValue(counter)
		l = len(trad)
		lc = 0
		for i in trad:
			if i in all_data_list:
				lc = lc + 1
				
		if lc == l:
			traditional = row[0]
			simplified = row[1]
			p = row[2]
			english = row[3]
			english = english[:-3]

			if len(traditional) >= min_length and len(traditional) <= max_lenght:  
				if any(x in english.lower() for x in filter_list):
					continue

				else:
					if trad not in word_list:
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
						self.dialog.Found_Value.setText(str(found))

						rowPosition = self.dialog.Results.rowCount()
						self.dialog.Results.setColumnCount(4)
						self.dialog.Results.insertRow(rowPosition)

						self.dialog.Results.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(traditional))
						self.dialog.Results.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(simplified))
						self.dialog.Results.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(p))
						self.dialog.Results.setItem(rowPosition, 3, QtWidgets.QTableWidgetItem(english))
						
					else:
						continue
	self.dialog.Results.resizeColumnsToContents()
	anki_file.close()
	if config["checked"] == "True":
		importfile("WordsFound.txt", config["import_deck"], config["import_notetype"])