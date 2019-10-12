from PyQt5 import QtCore, QtGui, QtWidgets
from aqt import mw
from aqt.qt import *
import os
from os.path import dirname, join, realpath
from aqt.utils import tooltip, showInfo
from sqlite3 import connect

db_path = join(dirname(realpath(__file__)), 'database.db')
conn = connect(db_path)
c = conn.cursor()
config = mw.addonManager.getConfig(__name__)
language = config['language']

class Ui_Add_from_dictionary(object):
	def setupUi(self, Add_from_dictionary):
		Add_from_dictionary.setObjectName("Add_from_dictionary")
		Add_from_dictionary.resize(365, 157)
		self.gridLayout = QtWidgets.QGridLayout(Add_from_dictionary)
		self.gridLayout.setObjectName("gridLayout")
		self.verticalLayout = QtWidgets.QVBoxLayout()
		self.verticalLayout.setObjectName("verticalLayout")

		self.Info_Label = QtWidgets.QLabel(Add_from_dictionary)
		self.Info_Label.setObjectName("Info_Label")
		self.verticalLayout.addWidget(self.Info_Label)

		self.Input_Form = QtWidgets.QComboBox(Add_from_dictionary)
		font = QtGui.QFont()
		font.setPointSize(8)
		self.Input_Form.setFont(font)
		self.Input_Form.setObjectName("Input_Form")
		self.Input_Form.addItem("")
		self.Input_Form.addItem("")
		self.Input_Form.addItem("")
		self.verticalLayout.addWidget(self.Input_Form)

		self.Input = QtWidgets.QLineEdit(Add_from_dictionary)
		self.Input.setObjectName("Input")
		self.verticalLayout.addWidget(self.Input)

		self.Search = QtWidgets.QPushButton(Add_from_dictionary)
		self.Search.setObjectName("Search")
		self.verticalLayout.addWidget(self.Search)
		self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
		self.Search.clicked.connect(self.search)

		self.retranslateUi(Add_from_dictionary)
		QtCore.QMetaObject.connectSlotsByName(Add_from_dictionary)

	def retranslateUi(self, Add_from_dictionary):
		_translate = QtCore.QCoreApplication.translate
		Add_from_dictionary.setWindowTitle(_translate("Add_from_dictionary", "Add cards from dictionary"))
		self.Info_Label.setText(_translate("Add_from_dictionary", "Search the CC-CEDICT dictionary and add cards to Anki"))
		self.Input_Form.setItemText(0, _translate("Add_from_dictionary", "Simplified"))
		self.Input_Form.setItemText(1, _translate("Add_from_dictionary", "Traditional"))
		self.Input_Form.setItemText(2, _translate("Add_from_dictionary", "English"))
		self.Search.setText(_translate("Add_from_dictionary", "Search"))
	
	def search(self):
		pass

class start_search_dialog(QDialog):
	def __init__(self, parent=None):
		self.parent = parent
		QDialog.__init__(self, parent, Qt.Window)
		self.ui = Ui_Add_from_dictionary()
		self.ui.setupUi(self)