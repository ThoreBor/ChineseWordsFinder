from aqt import mw
from aqt.utils import showWarning
import re

def extractChinese(output):
	extract = re.compile(u'[^\u4E00-\u9FA5]')
	output = extract.sub(r'', output) 
	return output

def getdata():
	all_data = ""
	notes_in_deck = []
	notes_in_sub_deck = []
	word_list = []
	config = mw.addonManager.getConfig(__name__)
	deckname = config['deckname']
	tos = config['tos']
	filter_list = config['filter']
	min_length = config['min_length']
	max_lenght = config['max_lenght']
	exclude_subdeck = config['exclude_subdeck']
	word_list = []
	
	if max_lenght == 0:
		max_lenght = 25
	
	for i in deckname:
		find_ids = mw.col.findNotes("deck:" + i)
		if len(find_ids) == 0 and i != "Default":
			showWarning("Couldn't find any cards in " + str(i))
		for i in find_ids:
			notes_in_deck.append(i)

	
	if "parentdeck::subdeck" not in exclude_subdeck:
		for i in exclude_subdeck:
			find_ids = mw.col.findNotes("deck:" + i)
			if len(find_ids) == 0:
				showWarning("Couldn't find any cards in " + str(i))
			for i in find_ids:
				notes_in_sub_deck.append(i)
		for i in notes_in_sub_deck:
			notes_in_deck.remove(i)

	for i in notes_in_deck:
		field_number = config['field_number']
		if field_number == 0:
			all_data = all_data + str(mw.col.db.scalar("SELECT flds FROM notes WHERE id=?" ,i, ))
		else:
			try:
				field_number = field_number-1
				all_fields = mw.col.db.scalar("SELECT flds FROM notes WHERE id=?" ,i, )
				field = all_fields.split("")
				field = field[field_number]
				word_list.append(field)
				all_data = all_data + str(field)
			except:
				continue

	all_data = extractChinese(all_data)
	raw = all_data
	all_data = ''.join(set(all_data))
	all_data_list = list(all_data)
	number_of_characters = len(all_data_list)
	
	return all_data_list, notes_in_deck, number_of_characters, tos, filter_list, min_length, max_lenght, word_list, config, raw

