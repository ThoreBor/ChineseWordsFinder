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

class Ui_Config(object):
    def setupUi(self, Config):

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

        self.Hover = QtWidgets.QLabel(Config)
        font = QtGui.QFont()
        font.setItalic(True)
        font.setKerning(True)
        self.Hover.setFont(font)
        self.Hover.setObjectName("Hover")
        self.verticalLayout.addWidget(self.Hover)

        self.Deck_Label = QtWidgets.QLabel(Config)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.Deck_Label.setFont(font)
        self.Deck_Label.setObjectName("Deck_Label")
        self.verticalLayout.addWidget(self.Deck_Label)

        self.Decks = QtWidgets.QLineEdit(Config)
        self.Decks.setObjectName("Decks")
        # for i in decklist:
        #     self.Decks.addItem(str(i))
        self.verticalLayout.addWidget(self.Decks)

        self.Subdecks_Label = QtWidgets.QLabel(Config)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.Subdecks_Label.setFont(font)
        self.Subdecks_Label.setObjectName("Subdecks_Label")
        self.verticalLayout.addWidget(self.Subdecks_Label)

        self.Subdecks = QtWidgets.QLineEdit(Config)
        self.Subdecks.setObjectName("Subdecks")
        # for i in subdeckslist:
        #     self.Subdecks.addItem(str(i))
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

        self.Check_Import = QtWidgets.QCheckBox(Config)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.Check_Import.setFont(font)
        self.Check_Import.setObjectName("Check_Import")
        self.verticalLayout.addWidget(self.Check_Import)
        self.Check_Import.stateChanged.connect(self.checked)

        self.Import_Notetype_Label = QtWidgets.QLabel(Config)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.Import_Notetype_Label.setFont(font)
        self.Import_Notetype_Label.setObjectName("Import_Notetype_Label")
        self.verticalLayout.addWidget(self.Import_Notetype_Label)

        self.Import_Notetype = QtWidgets.QComboBox(Config)
        self.Import_Notetype.setEnabled(False)
        self.Import_Notetype.setObjectName("Import_Notetype")
        for i in notetypelist:
            self.Import_Notetype.addItem(str(i))
        self.verticalLayout.addWidget(self.Import_Notetype)

        self.Import_Deck_Label = QtWidgets.QLabel(Config)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.Import_Deck_Label.setFont(font)
        self.Import_Deck_Label.setObjectName("Import_Deck_Label")
        self.verticalLayout.addWidget(self.Import_Deck_Label)

        self.Import_Deck = QtWidgets.QComboBox(Config)
        self.Import_Deck.setEnabled(False)
        self.Import_Deck.setObjectName("Import_Deck")
        for i in decklist:
            self.Import_Deck.addItem(str(i))
        self.verticalLayout.addWidget(self.Import_Deck)

        self.Language_Label = QtWidgets.QLabel(Config)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.Language_Label.setFont(font)
        self.Language_Label.setObjectName("Language_Label")
        self.verticalLayout.addWidget(self.Language_Label)

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

        self.Hover.setText(_translate("Config", ''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Hover info' ").fetchone())))

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

        load_hsk = "HSK " + str(config["HSK"])        
        self.HSK.setItemText(0, _translate("Config", "HSK 1"))
        self.HSK.setItemText(1, _translate("Config", "HSK 2"))
        self.HSK.setItemText(2, _translate("Config", "HSK 3"))
        self.HSK.setItemText(3, _translate("Config", "HSK 4"))
        self.HSK.setItemText(4, _translate("Config", "HSK 5"))
        self.HSK.setItemText(5, _translate("Config", "HSK 6"))
        self.HSK.setCurrentText(load_hsk)
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

        self.Check_Import.setText(_translate("Config", ''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Checkbox info' ").fetchone())))
        if config["checked"] == "True":
            self.Check_Import.toggle()

        self.Import_Notetype_Label.setText(_translate("Config", ''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Notetype Label' ").fetchone())))
        self.Import_Notetype.setCurrentText(config["import_notetype"])
        self.Import_Deck_Label.setText(_translate("Config", ''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Deck Import Label' ").fetchone())))
        self.Import_Deck.setCurrentText(config["import_deck"])

        self.Language_Label.setText(''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Language Label' ").fetchone()))

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
        if self.Check_Import.isChecked():
            toggled = "True"
            showInfo(''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Checked info' ").fetchone()))
        else:
            toggled = "False"
        import_notetype_config = self.Import_Notetype.currentText()
        import_deck_config = self.Import_Deck.currentText()
        language_config = self.Language.currentText()

        config = {"checked": toggled,"import_notetype": import_notetype_config, "import_deck": import_deck_config, "language": language_config, "exclude_subdeck": subdecks_config,
        "tos": TOS_config, "deckname": decks_config,"filter": filter_config, 
        "min_length": min_config, "max_lenght": max_config, "field_number": field_number_config, "HSK": HSK_config}
        mw.addonManager.writeConfig(__name__, config)
        tooltip(''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Saved' ").fetchone()))
    def default(self):
        os.remove(join(dirname(realpath(__file__)), 'meta.json'))
    
    def checked(self):
        if self.Check_Import.isChecked():
            self.Import_Notetype.setEnabled(True)
            self.Import_Deck.setEnabled(True)
        else:
            self.Import_Notetype.setEnabled(False)
            self.Import_Deck.setEnabled(False)

class start_config(QDialog):
    def __init__(self, parent=None):
        self.parent = parent
        QDialog.__init__(self, parent, Qt.Window)
        self.dialog = Ui_Config()
        self.dialog.setupUi(self)