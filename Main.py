from PyQt5 import QtCore, QtGui, QtWidgets
from aqt import mw
from aqt.qt import *
import os
from os.path import dirname, join, realpath
from aqt.utils import tooltip, showInfo
from sqlite3 import connect
from .getdata import getdata
from .import_file import importfile
from .freq import frequency

db_path = join(dirname(realpath(__file__)), 'database.db')
conn = connect(db_path)
c = conn.cursor()
config = mw.addonManager.getConfig(__name__)

class Ui_Main(object):
	def setupUi(self, Main):

		out=mw.col.decks.all()
		decklist = []
		subdeckslist = []
		for l in out:
		   decklist.append(l['name'])
		for i in decklist:
			if "::" in i:
				subdeckslist.append(i)
		
		out=mw.col.models.all()
		notetypelist = []
		for l in out:
		   notetypelist.append(l['name'])


		Main.setObjectName("Main")
		Main.setWindowModality(QtCore.Qt.NonModal)
		Main.setEnabled(True)
		Main.resize(587, 572)
		Main.setFocusPolicy(QtCore.Qt.TabFocus)
		Main.setAcceptDrops(False)
		Main.setToolTip("")
		Main.setWhatsThis("")
		Main.setAutoFillBackground(False)
		Main.setSizeGripEnabled(False)
		Main.setWindowIcon(QtGui.QIcon(join(dirname(realpath(__file__)), 'icon.png')))
		Main.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)

		#####
		#CWF#
		#####

		self.Tab = QtWidgets.QTabWidget(Main)
		self.Tab.setGeometry(QtCore.QRect(10, 10, 571, 551))
		self.Tab.setObjectName("Tab")
		self.tab = QtWidgets.QWidget()
		self.tab.setObjectName("tab")
		self.layoutWidget = QtWidgets.QWidget(self.tab)
		self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 541, 501))
		self.layoutWidget.setObjectName("layoutWidget")
		self.gridLayout_5 = QtWidgets.QGridLayout(self.layoutWidget)
		self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
		self.gridLayout_5.setObjectName("gridLayout_5")
		self.CWF_Info = QtWidgets.QLabel(self.layoutWidget)
		font = QtGui.QFont()
		font.setPointSize(9)
		font.setBold(True)
		font.setWeight(75)

		self.CWF_Info.setFont(font)
		self.CWF_Info.setObjectName("CWF_Info")
		self.gridLayout_5.addWidget(self.CWF_Info, 0, 0, 1, 4)

		self.Notenumber = QtWidgets.QLabel(self.layoutWidget)
		font = QtGui.QFont()
		font.setPointSize(9)
		self.Notenumber.setFont(font)
		self.Notenumber.setObjectName("Notenumber")
		self.gridLayout_5.addWidget(self.Notenumber, 1, 0, 1, 3)

		self.Notenumber_Value = QtWidgets.QLabel(self.layoutWidget)
		font = QtGui.QFont()
		font.setPointSize(9)
		self.Notenumber_Value.setFont(font)
		self.Notenumber_Value.setObjectName("Notenumber_Value")
		self.gridLayout_5.addWidget(self.Notenumber_Value, 1, 3, 1, 1)

		self.Unique = QtWidgets.QLabel(self.layoutWidget)
		font = QtGui.QFont()
		font.setPointSize(9)
		self.Unique.setFont(font)
		self.Unique.setObjectName("Unique")
		self.gridLayout_5.addWidget(self.Unique, 2, 0, 1, 2)

		self.Found = QtWidgets.QLabel(self.layoutWidget)
		font = QtGui.QFont()
		font.setPointSize(9)
		self.Found.setFont(font)
		self.Found.setObjectName("Found")
		self.gridLayout_5.addWidget(self.Found, 3, 0, 1, 2)

		self.CWF_start = QtWidgets.QPushButton(self.layoutWidget)
		self.CWF_start.setObjectName("CWF_start")
		self.CWF_start.clicked.connect(self.CWF)
		self.gridLayout_5.addWidget(self.CWF_start, 4, 0, 1, 1)

		self.Results = QtWidgets.QListWidget(self.layoutWidget)
		font = QtGui.QFont()
		font.setFamily("SimHei")
		self.Results.setFont(font)
		self.Results.setObjectName("Results")
		self.gridLayout_5.addWidget(self.Results, 5, 0, 1, 4)

		self.Unique_Value = QtWidgets.QLabel(self.layoutWidget)
		font = QtGui.QFont()
		font.setPointSize(9)
		self.Unique_Value.setFont(font)
		self.Unique_Value.setObjectName("Unique_Value")
		self.gridLayout_5.addWidget(self.Unique_Value, 2, 3, 1, 1)

		self.Found_Value = QtWidgets.QLabel(self.layoutWidget)
		font = QtGui.QFont()
		font.setPointSize(9)
		self.Found_Value.setFont(font)
		self.Found_Value.setObjectName("Found_Value")
		self.gridLayout_5.addWidget(self.Found_Value, 3, 3, 1, 1)

		self.pbar = QtWidgets.QProgressBar(self.layoutWidget)
		self.pbar.setMaximum(117272)
		self.pbar.setProperty("value", 0)
		self.pbar.setObjectName("pbar")
		self.gridLayout_5.addWidget(self.pbar, 4, 1, 1, 3)
		self.Tab.addTab(self.tab, "")

		#####
		#HSK#
		#####

		self.tab_3 = QtWidgets.QWidget()
		self.tab_3.setObjectName("tab_3")
		self.layoutWidget1 = QtWidgets.QWidget(self.tab_3)
		self.layoutWidget1.setGeometry(QtCore.QRect(10, 10, 541, 501))
		self.layoutWidget1.setObjectName("layoutWidget1")
		self.gridLayout_4 = QtWidgets.QGridLayout(self.layoutWidget1)
		self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
		self.gridLayout_4.setObjectName("gridLayout_4")
		self.HSK_Info = QtWidgets.QLabel(self.layoutWidget1)
		font = QtGui.QFont()
		font.setPointSize(9)
		font.setBold(True)
		font.setWeight(75)

		self.HSK_Info.setFont(font)
		self.HSK_Info.setObjectName("HSK_Info")
		self.gridLayout_4.addWidget(self.HSK_Info, 0, 0, 1, 4)

		self.Notenumber_HSK = QtWidgets.QLabel(self.layoutWidget1)
		font = QtGui.QFont()
		font.setPointSize(9)
		self.Notenumber_HSK.setFont(font)
		self.Notenumber_HSK.setObjectName("Notenumber_HSK")
		self.gridLayout_4.addWidget(self.Notenumber_HSK, 1, 0, 1, 3)

		self.Notenumber_HSK_Value = QtWidgets.QLabel(self.layoutWidget1)
		font = QtGui.QFont()
		font.setPointSize(9)
		self.Notenumber_HSK_Value.setFont(font)
		self.Notenumber_HSK_Value.setObjectName("Notenumber_HSK_Value")
		self.gridLayout_4.addWidget(self.Notenumber_HSK_Value, 1, 3, 1, 1)

		self.Unique_HSK = QtWidgets.QLabel(self.layoutWidget1)
		font = QtGui.QFont()
		font.setPointSize(9)
		self.Unique_HSK.setFont(font)
		self.Unique_HSK.setObjectName("Unique_HSK")
		self.gridLayout_4.addWidget(self.Unique_HSK, 2, 0, 1, 2)

		self.Found_HSK = QtWidgets.QLabel(self.layoutWidget1)
		font = QtGui.QFont()
		font.setPointSize(9)
		self.Found_HSK.setFont(font)
		self.Found_HSK.setObjectName("Found_HSK")
		self.gridLayout_4.addWidget(self.Found_HSK, 3, 0, 1, 2)

		self.HSK_start = QtWidgets.QPushButton(self.layoutWidget1)
		self.HSK_start.setObjectName("HSK_start")
		self.HSK_start.clicked.connect(self.HSK)
		self.gridLayout_4.addWidget(self.HSK_start, 4, 0, 1, 1)

		self.Results_HSK = QtWidgets.QListWidget(self.layoutWidget1)
		font = QtGui.QFont()
		font.setFamily("SimHei")
		self.Results_HSK.setFont(font)
		self.Results_HSK.setObjectName("Results_HSK")
		self.gridLayout_4.addWidget(self.Results_HSK, 5, 0, 1, 4)

		self.Unique_HSK_Value = QtWidgets.QLabel(self.layoutWidget1)
		font = QtGui.QFont()
		font.setPointSize(9)
		self.Unique_HSK_Value.setFont(font)
		self.Unique_HSK_Value.setObjectName("Unique_HSK_Value")
		self.gridLayout_4.addWidget(self.Unique_HSK_Value, 2, 3, 1, 1)

		self.Found_HSK_Value = QtWidgets.QLabel(self.layoutWidget1)
		font = QtGui.QFont()
		font.setPointSize(9)
		self.Found_HSK_Value.setFont(font)
		self.Found_HSK_Value.setObjectName("Found_HSK_Value")
		self.gridLayout_4.addWidget(self.Found_HSK_Value, 3, 3, 1, 1)

		self.pbar_HSK = QtWidgets.QProgressBar(self.layoutWidget1)
		self.pbar_HSK.setProperty("value", 0)
		self.pbar_HSK.setObjectName("pbar_HSK")
		self.pbar.setMaximum(117272)
		self.gridLayout_4.addWidget(self.pbar_HSK, 4, 1, 1, 3)

		#####
		#FRQ#
		#####

		self.Tab.addTab(self.tab_3, "")
		self.tab_4 = QtWidgets.QWidget()
		self.tab_4.setObjectName("tab_4")
		self.layoutWidget2 = QtWidgets.QWidget(self.tab_4)
		self.layoutWidget2.setGeometry(QtCore.QRect(10, 10, 541, 501))
		self.layoutWidget2.setObjectName("layoutWidget2")
		self.gridLayout_3 = QtWidgets.QGridLayout(self.layoutWidget2)
		self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
		self.gridLayout_3.setObjectName("gridLayout_3")
		self.Unique_HSK_2 = QtWidgets.QLabel(self.layoutWidget2)
		font = QtGui.QFont()
		font.setPointSize(9)

		self.Unique_HSK_2.setFont(font)
		self.Unique_HSK_2.setObjectName("Unique_HSK_2")
		self.gridLayout_3.addWidget(self.Unique_HSK_2, 0, 0, 1, 1)

		self.Unique_HSK_Value_2 = QtWidgets.QLabel(self.layoutWidget2)
		font = QtGui.QFont()
		font.setPointSize(9)
		self.Unique_HSK_Value_2.setFont(font)
		self.Unique_HSK_Value_2.setObjectName("Unique_HSK_Value_2")
		self.gridLayout_3.addWidget(self.Unique_HSK_Value_2, 0, 1, 1, 1)

		self.Results_Freq = QtWidgets.QListWidget(self.layoutWidget2)
		font = QtGui.QFont()
		font.setFamily("SimHei")
		self.Results_Freq.setFont(font)
		self.Results_Freq.setObjectName("Results_Freq")
		self.gridLayout_3.addWidget(self.Results_Freq, 1, 0, 1, 2)
		self.start_freq()

		########
		#CONFIG#
		########

		self.Tab.addTab(self.tab_4, "")
		self.tab_2 = QtWidgets.QWidget()
		self.tab_2.setObjectName("tab_2")
		self.General_Box = QtWidgets.QGroupBox(self.tab_2)
		self.General_Box.setGeometry(QtCore.QRect(10, 10, 531, 261))
		self.General_Box.setObjectName("General_Box")
		self.widget = QtWidgets.QWidget(self.General_Box)
		self.widget.setGeometry(QtCore.QRect(11, 20, 513, 219))
		self.widget.setObjectName("widget")
		self.gridLayout_2 = QtWidgets.QGridLayout(self.widget)
		self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
		self.gridLayout_2.setObjectName("gridLayout_2")

		self.Deck_Label = QtWidgets.QLabel(self.widget)
		font = QtGui.QFont()
		font.setPointSize(9)
		self.Deck_Label.setFont(font)
		self.Deck_Label.setObjectName("Deck_Label")
		self.gridLayout_2.addWidget(self.Deck_Label, 0, 0, 1, 1)

		self.Filter_Label = QtWidgets.QLabel(self.widget)
		font = QtGui.QFont()
		font.setPointSize(9)
		self.Filter_Label.setFont(font)
		self.Filter_Label.setObjectName("Filter_Label")
		self.gridLayout_2.addWidget(self.Filter_Label, 0, 1, 1, 1)

		self.Decks = QtWidgets.QLineEdit(self.widget)
		self.Decks.setObjectName("Decks")
		self.gridLayout_2.addWidget(self.Decks, 1, 0, 1, 1)

		self.Filter = QtWidgets.QLineEdit(self.widget)
		self.Filter.setText("")
		self.Filter.setObjectName("Filter")
		self.gridLayout_2.addWidget(self.Filter, 1, 1, 1, 1)

		self.Subdecks_Label = QtWidgets.QLabel(self.widget)
		font = QtGui.QFont()
		font.setPointSize(9)
		self.Subdecks_Label.setFont(font)
		self.Subdecks_Label.setObjectName("Subdecks_Label")
		self.gridLayout_2.addWidget(self.Subdecks_Label, 2, 0, 1, 1)

		self.Field_Label = QtWidgets.QLabel(self.widget)
		font = QtGui.QFont()
		font.setPointSize(9)
		self.Field_Label.setFont(font)
		self.Field_Label.setObjectName("Field_Label")
		self.gridLayout_2.addWidget(self.Field_Label, 2, 1, 1, 1)

		self.Subdecks = QtWidgets.QLineEdit(self.widget)
		self.Subdecks.setObjectName("Subdecks")
		self.gridLayout_2.addWidget(self.Subdecks, 3, 0, 1, 1)

		self.Field_Number = QtWidgets.QSpinBox(self.widget)
		self.Field_Number.setObjectName("Field_Number")
		self.gridLayout_2.addWidget(self.Field_Number, 3, 1, 1, 1)

		self.TOS_Label = QtWidgets.QLabel(self.widget)
		font = QtGui.QFont()
		font.setPointSize(9)
		self.TOS_Label.setFont(font)
		self.TOS_Label.setObjectName("TOS_Label")
		self.gridLayout_2.addWidget(self.TOS_Label, 4, 0, 1, 1)

		self.Max_Label = QtWidgets.QLabel(self.widget)
		font = QtGui.QFont()
		font.setPointSize(9)
		self.Max_Label.setFont(font)
		self.Max_Label.setObjectName("Max_Label")
		self.gridLayout_2.addWidget(self.Max_Label, 4, 1, 1, 1)

		self.TOS = QtWidgets.QComboBox(self.widget)
		self.TOS.setObjectName("TOS")
		self.TOS.addItem("")
		self.TOS.addItem("")
		self.gridLayout_2.addWidget(self.TOS, 5, 0, 1, 1)

		self.Max = QtWidgets.QSpinBox(self.widget)
		self.Max.setObjectName("Max")
		self.gridLayout_2.addWidget(self.Max, 5, 1, 1, 1)

		self.HSK_Label = QtWidgets.QLabel(self.widget)
		font = QtGui.QFont()
		font.setPointSize(9)
		self.HSK_Label.setFont(font)
		self.HSK_Label.setObjectName("HSK_Label")
		self.gridLayout_2.addWidget(self.HSK_Label, 6, 0, 1, 1)

		self.Min_Label = QtWidgets.QLabel(self.widget)
		font = QtGui.QFont()
		font.setPointSize(9)
		self.Min_Label.setFont(font)
		self.Min_Label.setObjectName("Min_Label")
		self.gridLayout_2.addWidget(self.Min_Label, 6, 1, 1, 1)

		self.HSK = QtWidgets.QComboBox(self.widget)
		self.HSK.setObjectName("HSK")
		self.HSK.addItem("")
		self.HSK.addItem("")
		self.HSK.addItem("")
		self.HSK.addItem("")
		self.HSK.addItem("")
		self.HSK.addItem("")
		self.gridLayout_2.addWidget(self.HSK, 7, 0, 1, 1)

		self.Min = QtWidgets.QSpinBox(self.widget)
		self.Min.setObjectName("Min")
		self.gridLayout_2.addWidget(self.Min, 7, 1, 1, 1)

		self.Import_Box = QtWidgets.QGroupBox(self.tab_2)
		self.Import_Box.setGeometry(QtCore.QRect(10, 280, 531, 191))
		self.Import_Box.setObjectName("Import_Box")
		self.layoutWidget4 = QtWidgets.QWidget(self.Import_Box)
		self.layoutWidget4.setGeometry(QtCore.QRect(13, 28, 491, 141))
		self.layoutWidget4.setObjectName("layoutWidget4")
		self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget4)
		self.gridLayout.setContentsMargins(0, 0, 0, 0)
		self.gridLayout.setObjectName("gridLayout")

		self.Import_Notetype_Label = QtWidgets.QLabel(self.layoutWidget4)
		font = QtGui.QFont()
		font.setPointSize(9)
		self.Import_Notetype_Label.setFont(font)
		self.Import_Notetype_Label.setObjectName("Import_Notetype_Label")
		self.gridLayout.addWidget(self.Import_Notetype_Label, 1, 0, 1, 1)

		self.Import_Deck_Label = QtWidgets.QLabel(self.layoutWidget4)
		font = QtGui.QFont()
		font.setPointSize(9)
		self.Import_Deck_Label.setFont(font)
		self.Import_Deck_Label.setObjectName("Import_Deck_Label")
		self.gridLayout.addWidget(self.Import_Deck_Label, 1, 2, 1, 1)

		self.Field1_Label = QtWidgets.QLabel(self.layoutWidget4)
		self.Field1_Label.setObjectName("Field1_Label")
		self.gridLayout.addWidget(self.Field1_Label, 3, 0, 1, 1)

		self.Field2_Label = QtWidgets.QLabel(self.layoutWidget4)
		self.Field2_Label.setObjectName("Field2_Label")
		self.gridLayout.addWidget(self.Field2_Label, 3, 1, 1, 1)

		self.Field3_Label = QtWidgets.QLabel(self.layoutWidget4)
		self.Field3_Label.setObjectName("Field3_Label")
		self.gridLayout.addWidget(self.Field3_Label, 3, 2, 1, 1)

		self.Field4_Label = QtWidgets.QLabel(self.layoutWidget4)
		self.Field4_Label.setObjectName("Field4_Label")
		self.gridLayout.addWidget(self.Field4_Label, 3, 3, 1, 1)

		self.Field1 = QtWidgets.QComboBox(self.layoutWidget4)
		self.Field1.setEnabled(False)
		self.Field1.setObjectName("Field1")
		self.Field1.addItem("")
		self.Field1.addItem("")
		self.Field1.addItem("")
		self.Field1.addItem("")
		self.gridLayout.addWidget(self.Field1, 4, 0, 1, 1)

		self.Field2 = QtWidgets.QComboBox(self.layoutWidget4)
		self.Field2.setEnabled(False)
		self.Field2.setObjectName("Field2")
		self.Field2.addItem("")
		self.Field2.addItem("")
		self.Field2.addItem("")
		self.Field2.addItem("")
		self.gridLayout.addWidget(self.Field2, 4, 1, 1, 1)

		self.Field3 = QtWidgets.QComboBox(self.layoutWidget4)
		self.Field3.setEnabled(False)
		self.Field3.setObjectName("Field3")
		self.Field3.addItem("")
		self.Field3.addItem("")
		self.Field3.addItem("")
		self.Field3.addItem("")
		self.Field3.addItem("")
		self.gridLayout.addWidget(self.Field3, 4, 2, 1, 1)

		self.Field4 = QtWidgets.QComboBox(self.layoutWidget4)
		self.Field4.setEnabled(False)
		self.Field4.setObjectName("Field4")
		self.Field4.addItem("")
		self.Field4.addItem("")
		self.Field4.addItem("")
		self.Field4.addItem("")
		self.Field4.addItem("")
		self.gridLayout.addWidget(self.Field4, 4, 3, 1, 1)

		self.Import_Notetype = QtWidgets.QComboBox(self.layoutWidget4)
		self.Import_Notetype.setEnabled(False)
		for i in notetypelist:
			self.Import_Notetype.addItem(str(i))
		self.Import_Notetype.setObjectName("Import_Notetype")
		self.gridLayout.addWidget(self.Import_Notetype, 2, 0, 1, 2)

		self.Import_Deck = QtWidgets.QComboBox(self.layoutWidget4)
		self.Import_Deck.setEnabled(False)
		for i in decklist:
			self.Import_Deck.addItem(str(i))
		self.Import_Deck.setObjectName("Import_Deck")
		self.gridLayout.addWidget(self.Import_Deck, 2, 2, 1, 2)

		self.Check_Import = QtWidgets.QCheckBox(self.layoutWidget4)
		font = QtGui.QFont()
		font.setPointSize(9)
		self.Check_Import.setFont(font)
		self.Check_Import.setObjectName("Check_Import")
		self.Check_Import.stateChanged.connect(self.checked)
		self.gridLayout.addWidget(self.Check_Import, 0, 0, 1, 4)

		self.Save_Button = QtWidgets.QPushButton(self.tab_2)
		self.Save_Button.setGeometry(QtCore.QRect(10, 480, 261, 28))
		font = QtGui.QFont()
		font.setPointSize(9)
		font.setBold(False)
		font.setWeight(50)
		self.Save_Button.setFont(font)
		self.Save_Button.setObjectName("Save_Button")

		self.Default_Button = QtWidgets.QPushButton(self.tab_2)
		self.Default_Button.setGeometry(QtCore.QRect(280, 480, 261, 28))
		font = QtGui.QFont()
		font.setPointSize(9)
		font.setBold(False)
		font.setWeight(50)
		self.Default_Button.setFont(font)
		self.Default_Button.setObjectName("Default_Button")
		self.Tab.addTab(self.tab_2, "")

		self.Save_Button.clicked.connect(self.save_config)
		self.Default_Button.clicked.connect(self.default)

		self.retranslateUi(Main)
		self.Tab.setCurrentIndex(0)
		QtCore.QMetaObject.connectSlotsByName(Main)
		Main.setTabOrder(self.TOS, self.HSK)
		Main.setTabOrder(self.HSK, self.Filter)
		Main.setTabOrder(self.Filter, self.Field_Number)
		Main.setTabOrder(self.Field_Number, self.Max)
		Main.setTabOrder(self.Max, self.Min)

	def retranslateUi(self, Main):
		config = mw.addonManager.getConfig(__name__)
		all_data_list, notes_in_deck, number_of_characters, decknames, tos, filter_list, min_length, max_lenght, word_list, config, raw = getdata()
		_translate = QtCore.QCoreApplication.translate
		Main.setWindowTitle(_translate("Main", "Chinese Words Finder"))
		self.CWF_Info.setText(_translate("Main", "<html><head/><body><p>Find all Chinese words in the CC-CEDICT dictionary that only use <br/>the characters in the deck you choose sorted by frequency.</p></body></html>"))
		self.Notenumber.setText(_translate("Main", "Number of notes to be analyzed:"))
		self.Notenumber_Value.setText(_translate("Main", "0"))
		self.Unique.setText(_translate("Main", "Unique characters:"))
		self.Found.setText(_translate("Main", "Unique words found:"))
		self.CWF_start.setText(_translate("Main", "Find words"))
		self.Unique_Value.setText(_translate("Main", "0"))
		self.Found_Value.setText(_translate("Main", "0"))
		self.Tab.setTabText(self.Tab.indexOf(self.tab), _translate("Main", "Chinese Words Finder"))
		self.HSK_Info.setText(_translate("Main", "<html><head/><body><p>Find all missing HSK words.</p></body></html>"))
		self.Notenumber_HSK.setText(_translate("Main", "Number of notes to be analyzed:"))
		self.Notenumber_HSK_Value.setText(_translate("Main", "0"))
		self.Unique_HSK.setText(_translate("Main", "Unique characters:"))
		self.Found_HSK.setText(_translate("Main", "HSK words found:"))
		self.HSK_start.setText(_translate("Main", "Find HSK words"))
		self.Unique_HSK_Value.setText(_translate("Main", "0"))
		self.Found_HSK_Value.setText(_translate("Main", "0"))
		self.Tab.setTabText(self.Tab.indexOf(self.tab_3), _translate("Main", "Missing HSK Words"))
		self.Unique_HSK_2.setText(_translate("Main", "<b>Unique characters:</b>"))
		self.Unique_HSK_Value_2.setText(_translate("Main", "0"))
		self.Tab.setTabText(self.Tab.indexOf(self.tab_4), _translate("Main", "Character Frequency"))
		self.General_Box.setTitle(_translate("Main", "General"))
		self.TOS_Label.setText(_translate("Main", "Type of characters you are using:"))
		self.HSK_Label.setText(_translate("Main", "HSK level:"))
		
		self.HSK.setToolTip(_translate("Main", "Includes all previous levels."))
		self.Field_Number.setToolTip(_translate("Main", "0 = all fields"))
		self.Max.setToolTip(_translate("Main", "0 = no limit"))

		self.Notenumber_Value.setText(str(len(notes_in_deck)))
		self.Unique_Value.setText(str(number_of_characters))
		self.Notenumber_HSK_Value.setText(str(len(notes_in_deck)))
		self.Unique_HSK_Value.setText(str(number_of_characters))
		self.Unique_HSK_Value_2.setText(str(number_of_characters))

		self.Deck_Label.setText(_translate("Main", "Decks you want to analyse:"))
		self.Decks.setText(','.join(config["deckname"]))

		self.Filter_Label.setText(_translate("Main", "Filterwords that won't appear in the results:"))

		self.Subdecks_Label.setText(_translate("Main", "Subdecks you want to exclude:"))
		self.Subdecks.setText(','.join(config["exclude_subdeck"]))

		self.Field_Label.setText(_translate("Main", "Field you want to analyse:"))
		self.TOS.setItemText(0, _translate("Main", "Simplified"))
		self.TOS.setItemText(1, _translate("Main", "Traditional"))
		self.Max_Label.setText(_translate("Main", "Maximum length of output words:"))

		self.Filter.setText(','.join(config["filter"]))
		self.Field_Number.setValue(config["field_number"])
		self.Max.setValue(config["max_lenght"])
		self.Min.setValue(config["min_length"])
		self.Import_Notetype.setCurrentText(config["import_notetype"])
		self.Import_Deck.setCurrentText(config["import_deck"])

		if config["checked"] == "True":
			self.Check_Import.toggle()


		load_tos = config["tos"]
		if load_tos == 1:
			self.TOS.setItemText(0, _translate("Main", 'Simplified'))
			self.TOS.setItemText(1, _translate("Main", 'Traditional'))
		else:
			self.TOS.setItemText(0, _translate("Main", 'Traditional'))
			self.TOS.setItemText(1, _translate("Main", 'Simplified'))


		load_hsk = "HSK " + str(config["HSK"]) 
		self.HSK.setItemText(0, _translate("Main", "HSK 1"))
		self.HSK.setItemText(1, _translate("Main", "HSK 2"))
		self.HSK.setItemText(2, _translate("Main", "HSK 3"))
		self.HSK.setItemText(3, _translate("Main", "HSK 4"))
		self.HSK.setItemText(4, _translate("Main", "HSK 5"))
		self.HSK.setItemText(5, _translate("Main", "HSK 6"))
		self.HSK.setCurrentText(load_hsk)

		self.Min_Label.setText(_translate("Main", "Minimum length of output words:"))
		self.Import_Box.setTitle(_translate("Main", "Import"))
		self.Import_Notetype_Label.setText(_translate("Main", "Notetype:"))
		self.Import_Deck_Label.setText(_translate("Main", "Deck"))
		self.Field1_Label.setText(_translate("Main", "Field 1:"))
		self.Field2_Label.setText(_translate("Main", "Field 2:"))
		self.Field3_Label.setText(_translate("Main", "Field 3:"))
		self.Field4_Label.setText(_translate("Main", "Field 4:"))
		self.Field1.setItemText(0, _translate("Main", "Simplified"))
		self.Field1.setItemText(1, _translate("Main", "Traditional"))
		self.Field1.setItemText(2, _translate("Main", "Pinyin"))
		self.Field1.setItemText(3, _translate("Main", "English"))
		self.Field2.setItemText(0, _translate("Main", "Traditional"))
		self.Field2.setItemText(1, _translate("Main", "Simplified"))
		self.Field2.setItemText(2, _translate("Main", "Pinyin"))
		self.Field2.setItemText(3, _translate("Main", "English"))
		self.Field3.setItemText(0, _translate("Main", "Pinyin"))
		self.Field3.setItemText(1, _translate("Main", "Simplified"))
		self.Field3.setItemText(2, _translate("Main", "Traditional"))
		self.Field3.setItemText(3, _translate("Main", "English"))
		self.Field3.setItemText(4, _translate("Main", "Nothing"))
		self.Field4.setItemText(0, _translate("Main", "English"))
		self.Field4.setItemText(1, _translate("Main", "Simplified"))
		self.Field4.setItemText(2, _translate("Main", "Traditional"))
		self.Field4.setItemText(3, _translate("Main", "Pinyin"))
		self.Field4.setItemText(4, _translate("Main", "Nothing"))

		self.Field1.setCurrentText(config["field_1_config"])
		self.Field2.setCurrentText(config["field_2_config"])
		self.Field3.setCurrentText(config["field_3_config"])
		self.Field4.setCurrentText(config["field_4_config"])

		self.Check_Import.setText(_translate("Main", "Automatically import results into Anki"))
		self.Save_Button.setText(_translate("Main", "Save"))
		self.Default_Button.setText(_translate("Main", "Restore Defaults"))
		self.Tab.setTabText(self.Tab.indexOf(self.tab_2), _translate("Main", "Configurations"))

	def save_config(self):
		decks_config = self.Decks.text()
		decks_config = decks_config.replace(", ", ",")
		decks_config = decks_config.split(",")
		subdecks_config = self.Subdecks.text()
		subdecks_config = subdecks_config.replace(", ", ",")
		subdecks_config = subdecks_config.split(",")
		TOS_config = self.TOS.currentText()
		if TOS_config == 'Traditional':
			TOS_config = 0
		if TOS_config == 'Simplified':
			TOS_config = 1
		filter_config = self.Filter.text()
		filter_config = filter_config.replace(", ", ",")
		filter_config = filter_config.split(",")
		HSK_config = self.HSK.currentText()
		HSK_config = int(HSK_config.replace("HSK ",""))
		field_number_config = self.Field_Number.value()
		max_config = self.Max.value()
		min_config = self.Min.value()
		field_1_config = self.Field1.currentText()
		field_2_config = self.Field2.currentText()
		field_3_config = self.Field3.currentText()
		field_4_config = self.Field4.currentText()
		if self.Check_Import.isChecked():
			toggled = "True"
		else:
			toggled = "False"
		import_notetype_config = self.Import_Notetype.currentText()
		import_deck_config = self.Import_Deck.currentText()

		config = {"checked": toggled,"import_notetype": import_notetype_config, "import_deck": import_deck_config, "exclude_subdeck": subdecks_config,
		"tos": TOS_config, "deckname": decks_config,"filter": filter_config, 
		"min_length": min_config, "max_lenght": max_config, "field_number": field_number_config, "HSK": HSK_config,
		"field_1_config": field_1_config, "field_2_config": field_2_config, "field_3_config": field_3_config, "field_4_config": field_4_config}
		mw.addonManager.writeConfig(__name__, config)
		all_data_list, notes_in_deck, number_of_characters, decknames, tos, filter_list, min_length, max_lenght, word_list, config, raw = getdata()
		self.Notenumber_Value.setText(str(len(notes_in_deck)))
		self.Unique_Value.setText(str(number_of_characters))
		self.Notenumber_HSK_Value.setText(str(len(notes_in_deck)))
		self.Unique_HSK_Value.setText(str(number_of_characters))
		self.Unique_HSK_Value_2.setText(str(number_of_characters))
		self.Results.clear()
		self.Results_Freq.clear()
		self.Results_HSK.clear()
		self.pbar_HSK.setValue(0)
		self.pbar.setValue(0)
		self.start_freq()
		tooltip('Saved successfully.')
	
	def default(self):
		os.remove(join(dirname(realpath(__file__)), 'meta.json'))
	
	def checked(self):
		if self.Check_Import.isChecked():
			self.Import_Notetype.setEnabled(True)
			self.Import_Deck.setEnabled(True)
			self.Field1.setEnabled(True)
			self.Field2.setEnabled(True)
			self.Field3.setEnabled(True)
			self.Field4.setEnabled(True)
		else:
			self.Import_Notetype.setEnabled(False)
			self.Import_Deck.setEnabled(False)
			self.Field1.setEnabled(False)
			self.Field2.setEnabled(False)
			self.Field3.setEnabled(False)
			self.Field4.setEnabled(False)

	def CWF(self):
		self.Results.clear()
		found = 0
		counter = 0
		all_data_list, notes_in_deck, number_of_characters, decknames, tos, filter_list, min_length, max_lenght, word_list, config, raw = getdata()
		if filter_list == [""]:
			filter_list = []
		anki_file =  open(join(dirname(realpath(__file__)), 'WordsFound.txt'), "w", encoding="utf-8")


		c.execute('SELECT * FROM dictionary ORDER BY freq DESC')
	
		for row in c.fetchall():
			trad = row[tos]
			counter = counter + 1
			self.pbar.setValue(counter)
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

							if self.Field1.currentText() == "Simplified":
								Field1_content = simplified
							if self.Field1.currentText() == "Traditional":
								Field1_content = traditional
							if self.Field1.currentText() == "Pinyin":
								Field1_content = p
							if self.Field1.currentText() == "English":
								Field1_content = english

							if self.Field2.currentText() == "Simplified":
								Field2_content = simplified
							if self.Field2.currentText() == "Traditional":
								Field2_content = traditional
							if self.Field2.currentText() == "Pinyin":
								Field2_content = p
							if self.Field2.currentText() == "English":
								Field2_content = english

							if self.Field3.currentText() == "Simplified":
								Field3_content = simplified
							if self.Field3.currentText() == "Traditional":
								Field3_content = traditional
							if self.Field3.currentText() == "Pinyin":
								Field3_content = p
							if self.Field3.currentText() == "English":
								Field3_content = english
							if self.Field3.currentText() == "Nothing":
								Field3_content = ""

							if self.Field4.currentText() == "Simplified":
								Field4_content = simplified
							if self.Field4.currentText() == "Traditional":
								Field4_content = traditional
							if self.Field4.currentText() == "Pinyin":
								Field4_content = p
							if self.Field4.currentText() == "English":
								Field4_content = english
							if self.Field4.currentText() == "Nothing":
								Field4_content = ""

							Card = str(Field1_content + "\t" + Field2_content + "\t" + Field3_content + "\t" + Field4_content)
							anki_file.write(Card)
							self.Results.addItem(Card)
							self.Found_Value.setText(str(found))
						else:
							continue
		anki_file.close()
		if config["checked"] == "True":
			importfile("WordsFound.txt", config["import_deck"], config["import_notetype"])

	def HSK(self):
		self.Results_HSK.clear()
		all_data_list, notes_in_deck, number_of_characters, decknames, tos, filter_list, min_length, max_lenght, word_list, config, raw = getdata()
		HSK = config['HSK']
		hsk_list = []
		if tos == 0:
			tos = 1
		else:
			tos = 0
		for i in range(HSK + 1):
			hsk_list.append("HSK "+str(i))
		anki_file =  open(join(dirname(realpath(__file__)), 'MissingHSK.txt'), "w", encoding="utf-8")
		counter = 0
		found = 0
		c.execute('SELECT * FROM HSK ORDER BY HSK ASC')
	 
		hsk_word_list = []
		for row in c.fetchall():
				counter = counter + 1
				self.pbar_HSK.setValue(counter)
				hanzi = row[tos]
				hsk_word_list.append(hanzi)
				hsk_lvl = row[4]
				if hanzi not in word_list and hsk_lvl in hsk_list:
					traditional = row[1]
					simplified = row[0]
					p = row[2]
					english = row[3]
					english = english.replace("\n", "")
					found = found + 1

					if self.Field1.currentText() == "Simplified":
						Field1_content = simplified
					if self.Field1.currentText() == "Traditional":
						Field1_content = traditional
					if self.Field1.currentText() == "Pinyin":
						Field1_content = p
					if self.Field1.currentText() == "English":
						Field1_content = english

					if self.Field2.currentText() == "Simplified":
						Field2_content = simplified
					if self.Field2.currentText() == "Traditional":
						Field2_content = traditional
					if self.Field2.currentText() == "Pinyin":
						Field2_content = p
					if self.Field2.currentText() == "English":
						Field2_content = english

					if self.Field3.currentText() == "Simplified":
						Field3_content = simplified
					if self.Field3.currentText() == "Traditional":
						Field3_content = traditional
					if self.Field3.currentText() == "Pinyin":
						Field3_content = p
					if self.Field3.currentText() == "English":
						Field3_content = english
					if self.Field3.currentText() == "Nothing":
						Field3_content = ""

					if self.Field4.currentText() == "Simplified":
						Field4_content = simplified
					if self.Field4.currentText() == "Traditional":
						Field4_content = traditional
					if self.Field4.currentText() == "Pinyin":
						Field4_content = p
					if self.Field4.currentText() == "English":
						Field4_content = english
					if self.Field4.currentText() == "Nothing":
						Field4_content = ""
					Card = str(Field1_content + "\t" + Field2_content + "\t" + Field3_content + "\t" + Field4_content)
					anki_file.write(Card)
					self.Results_HSK.addItem(Card)
					self.Found_HSK_Value.setText(str(found))
		anki_file.close()
		if config["checked"] == "True":
			importfile("MissingHSK.txt", config["import_deck"], config["import_notetype"])

	def start_freq(self):
		freq_list = frequency()
		for i in freq_list:
			self.Results_Freq.addItem(i)
		


class start_main(QDialog):
	def __init__(self, parent=None):
		self.parent = parent
		QDialog.__init__(self, parent, Qt.Window)
		self.dialog = Ui_Main()
		self.dialog.setupUi(self)