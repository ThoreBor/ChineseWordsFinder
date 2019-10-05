from PyQt5 import QtCore, QtGui, QtWidgets
from aqt import mw
from aqt.qt import *
import os
from os.path import dirname, join, realpath
from aqt.utils import tooltip
from sqlite3 import connect

db_path = join(dirname(realpath(__file__)), 'database.db')
conn = connect(db_path)
c = conn.cursor()
config = mw.addonManager.getConfig(__name__)
language = config['language']

class Ui_Config(object):
    def setupUi(self, Config):
        Config.setObjectName("Config")
        Config.setWindowIcon(QtGui.QIcon(join(dirname(realpath(__file__)), 'config_icon.png')))
        Config.setWindowModality(QtCore.Qt.NonModal)
        Config.setEnabled(True)
        Config.resize(398, 470)
        Config.setFocusPolicy(QtCore.Qt.TabFocus)
        Config.setAcceptDrops(False)
        Config.setAutoFillBackground(False)
        Config.setSizeGripEnabled(False)

        self.gridLayout = QtWidgets.QGridLayout(Config)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        self.Deck_Label = QtWidgets.QLabel(Config)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.Deck_Label.setFont(font)
        self.Deck_Label.setObjectName("Deck_Label")
        self.verticalLayout.addWidget(self.Deck_Label)

        self.Decks = QtWidgets.QLineEdit(Config)
        self.Decks.setObjectName("Decks")
        self.verticalLayout.addWidget(self.Decks)

        self.Subdecks_Label = QtWidgets.QLabel(Config)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.Subdecks_Label.setFont(font)
        self.Subdecks_Label.setObjectName("Subdecks_Label")
        self.verticalLayout.addWidget(self.Subdecks_Label)

        self.Subdecks = QtWidgets.QLineEdit(Config)
        self.Subdecks.setObjectName("Subdecks")
        self.verticalLayout.addWidget(self.Subdecks)

        self.TOS = QtWidgets.QComboBox(Config)
        self.TOS.setObjectName("TOS")
        self.TOS.addItem("")
        self.TOS.addItem("")
        self.verticalLayout.addWidget(self.TOS)

        self.HSK = QtWidgets.QComboBox(Config)
        self.HSK.setObjectName("HSK")
        self.HSK.addItem("")
        self.HSK.addItem("")
        self.HSK.addItem("")
        self.HSK.addItem("")
        self.HSK.addItem("")
        self.HSK.addItem("")
        self.verticalLayout.addWidget(self.HSK)

        self.Filter_Label = QtWidgets.QLabel(Config)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.Filter_Label.setFont(font)
        self.Filter_Label.setObjectName("Filter_Label")
        self.verticalLayout.addWidget(self.Filter_Label)

        self.Filter = QtWidgets.QLineEdit(Config)
        self.Filter.setText("")
        self.Filter.setObjectName("Filter")
        self.verticalLayout.addWidget(self.Filter)

        self.Field_Label = QtWidgets.QLabel(Config)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.Field_Label.setFont(font)
        self.Field_Label.setObjectName("Field_Label")
        self.verticalLayout.addWidget(self.Field_Label)

        self.Field_Number = QtWidgets.QSpinBox(Config)
        self.Field_Number.setObjectName("Field_Number")
        self.verticalLayout.addWidget(self.Field_Number)

        self.Max_Label = QtWidgets.QLabel(Config)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.Max_Label.setFont(font)
        self.Max_Label.setObjectName("Max_Label")
        self.verticalLayout.addWidget(self.Max_Label)

        self.Max = QtWidgets.QSpinBox(Config)
        self.Max.setObjectName("Max")
        self.verticalLayout.addWidget(self.Max)

        self.Min_Label = QtWidgets.QLabel(Config)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.Min_Label.setFont(font)
        self.Min_Label.setObjectName("Min_Label")
        self.verticalLayout.addWidget(self.Min_Label)

        self.Min = QtWidgets.QSpinBox(Config)
        self.Min.setObjectName("Min")
        self.verticalLayout.addWidget(self.Min)

        self.Language = QtWidgets.QComboBox(Config)
        self.Language.setObjectName("Language")
        self.Language.addItem("")
        self.Language.addItem("")
        self.verticalLayout.addWidget(self.Language)

        self.Default_Button = QtWidgets.QPushButton(Config)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.Default_Button.setFont(font)
        self.Default_Button.setObjectName("Default_Button")
        self.verticalLayout.addWidget(self.Default_Button)

        self.Save_Button = QtWidgets.QPushButton(Config)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.Save_Button.setFont(font)
        self.Save_Button.setObjectName("Save_Button")
        self.verticalLayout.addWidget(self.Save_Button)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        

        self.Save_Button.clicked.connect(self.save_config)
        self.Default_Button.clicked.connect(self.default)

        self.retranslateUi(Config)
        QtCore.QMetaObject.connectSlotsByName(Config)
        Config.setTabOrder(self.Decks, self.Subdecks)
        Config.setTabOrder(self.Subdecks, self.TOS)
        Config.setTabOrder(self.TOS, self.HSK)
        Config.setTabOrder(self.HSK, self.Filter)
        Config.setTabOrder(self.Filter, self.Field_Number)
        Config.setTabOrder(self.Field_Number, self.Max)
        Config.setTabOrder(self.Max, self.Min)
        Config.setTabOrder(self.Min, self.Language)
        Config.setTabOrder(self.Language, self.Save_Button)

    def retranslateUi(self, Config):
        config = mw.addonManager.getConfig(__name__)
        _translate = QtCore.QCoreApplication.translate
        Config.setWindowTitle(_translate("Config", ''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Config Title' ").fetchone())))

        self.Deck_Label.setText(_translate("Config", ''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Deck Label' ").fetchone())))
        self.Decks.setText(','.join(config["deckname"]))
        self.Decks.setToolTip(''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Decks Tip' ").fetchone()))

        self.Subdecks_Label.setText(_translate("Config", ''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Subdecks Label' ").fetchone())))
        self.Subdecks.setText(','.join(config["exclude_subdeck"]))
        self.Subdecks.setToolTip(''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Subdecks Tip' ").fetchone()))
        
        load_tos = config["tos"]
        if load_tos == 1:
            self.TOS.setItemText(0, _translate("Config", ''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'TOS Simp' ").fetchone())))
            self.TOS.setItemText(1, _translate("Config", ''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'TOS Trad' ").fetchone())))
        else:
            self.TOS.setItemText(0, _translate("Config", ''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'TOS Trad' ").fetchone())))
            self.TOS.setItemText(1, _translate("Config", ''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'TOS Simp' ").fetchone())))
        self.TOS.setToolTip(''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'TOS Tip' ").fetchone()))

        load_hsk = config["HSK"]
        hsk_list = []
        hsk_list.append('HSK '+str(load_hsk))
        for i in range(1, load_hsk):
            hsk_list.append('HSK '+str(i))
        for i in range(load_hsk, 7):
            hsk_list.append('HSK '+str(i))
        hsk_list = list(dict.fromkeys(hsk_list))        
        self.HSK.setItemText(0, _translate("Config", str(hsk_list[0])))
        self.HSK.setItemText(1, _translate("Config", str(hsk_list[1])))
        self.HSK.setItemText(2, _translate("Config", str(hsk_list[2])))
        self.HSK.setItemText(3, _translate("Config", str(hsk_list[3])))
        self.HSK.setItemText(4, _translate("Config", str(hsk_list[4])))
        self.HSK.setItemText(5, _translate("Config", str(hsk_list[5])))
        self.HSK.setToolTip(''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'HSK Tip' ").fetchone()))

        self.Filter_Label.setText(_translate("Config", ''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Filter Label' ").fetchone())))
        self.Filter.setText(','.join(config["filter"]))
        self.Filter.setToolTip(''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Filter Tip' ").fetchone()))

        self.Field_Label.setText(_translate("Config", ''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Field Label' ").fetchone())))
        self.Field_Number.setValue(config["field_number"])
        self.Field_Number.setToolTip(''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Field Tip' ").fetchone()))

        self.Max_Label.setText(_translate("Config", ''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Max Label' ").fetchone())))
        self.Max.setValue(config["max_lenght"])
        self.Max.setToolTip(''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Max Tip' ").fetchone()))

        self.Min_Label.setText(_translate("Config", ''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Min Label' ").fetchone())))
        self.Min.setValue(config["min_length"])
        self.Min.setToolTip(''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Min Tip' ").fetchone()))


        load_language = config["language"]
        if load_language == "English":
            self.Language.setItemText(0, _translate("Config", "English"))
            self.Language.setItemText(1, _translate("Config", "German"))
        else: 
            self.Language.setItemText(0, _translate("Config", "German"))
            self.Language.setItemText(1, _translate("Config", "English"))
        self.Language.setToolTip(''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Language Tip' ").fetchone()))

        self.Default_Button.setText(_translate("Config", ''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Restore Label' ").fetchone())))
        self.Default_Button.setToolTip(''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Restore Tip' ").fetchone()))
        self.Save_Button.setText(_translate("Config", ''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Save Label' ").fetchone())))
        

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
        language_config = self.Language.currentText()

        config = {"language": language_config, "exclude_subdeck": subdecks_config,
        "tos": TOS_config, "deckname": decks_config,"filter": filter_config, 
        "min_length": min_config, "max_lenght": max_config, "field_number": field_number_config, "HSK": HSK_config}
        mw.addonManager.writeConfig(__name__, config)
        tooltip("Saved successfully.")

    def default(self):
        os.remove(join(dirname(realpath(__file__)), 'meta.json'))

class start_config(QDialog):
    def __init__(self, parent=None):
        self.parent = parent
        QDialog.__init__(self, parent, Qt.Window)
        self.dialog = Ui_Config()
        self.dialog.setupUi(self)