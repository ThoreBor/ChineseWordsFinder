from aqt import mw
from .getdata import getdata
from aqt.utils import tooltip

def save_config(self):
	decks_config = self.dialog.Decks.text()
	decks_config = decks_config.replace(", ", ",")
	decks_config = decks_config.split(",")
	subdecks_config = self.dialog.Subdecks.text()
	subdecks_config = subdecks_config.replace(", ", ",")
	subdecks_config = subdecks_config.split(",")
	TOS_config = self.dialog.TOS.currentText()
	if TOS_config == 'Traditional':
		TOS_config = 0
	if TOS_config == 'Simplified':
		TOS_config = 1
	filter_config = self.dialog.Filter.text()
	filter_config = filter_config.replace(", ", ",")
	filter_config = filter_config.split(",")
	HSK_config = self.dialog.HSK.currentText()
	HSK_config = int(HSK_config.replace("HSK ",""))
	field_number_config = self.dialog.Field_Number.value()
	max_config = self.dialog.Max.value()
	min_config = self.dialog.Min.value()
	field_1_config = self.dialog.Field1.currentText()
	field_2_config = self.dialog.Field2.currentText()
	field_3_config = self.dialog.Field3.currentText()
	field_4_config = self.dialog.Field4.currentText()
	if self.dialog.Check_Import.isChecked():
		toggled = "True"
	else:
		toggled = "False"
	import_notetype_config = self.dialog.Import_Notetype.currentText()
	import_deck_config = self.dialog.Import_Deck.currentText()

	config = {"checked": toggled,"import_notetype": import_notetype_config, "import_deck": import_deck_config, "exclude_subdeck": subdecks_config,
	"tos": TOS_config, "deckname": decks_config,"filter": filter_config, 
	"min_length": min_config, "max_lenght": max_config, "field_number": field_number_config, "HSK": HSK_config,
	"field_1_config": field_1_config, "field_2_config": field_2_config, "field_3_config": field_3_config, "field_4_config": field_4_config}
	mw.addonManager.writeConfig(__name__, config)
	all_data_list, notes_in_deck, number_of_characters, tos, filter_list, min_length, max_lenght, word_list, config, raw = getdata()
	self.dialog.Notenumber_Value.setText(str(len(notes_in_deck)))
	self.dialog.Unique_Value.setText(str(number_of_characters))
	self.dialog.Notenumber_HSK_Value.setText(str(len(notes_in_deck)))
	self.dialog.Unique_HSK_Value.setText(str(number_of_characters))
	self.dialog.Unique_HSK_Value_2.setText(str(number_of_characters))
	self.dialog.Results.setRowCount(0)
	self.dialog.Results_Freq.clear()
	self.dialog.Results_HSK.setRowCount(0)
	self.dialog.pbar.setValue(0)
	self.dialog.Found_HSK_Value.setText("0")
	self.dialog.Found_Value.setText("0")
	self.start_freq()
	tooltip('Saved successfully.')