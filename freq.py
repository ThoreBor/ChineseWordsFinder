from .getdata import getdata
from aqt import mw
from aqt.qt import *
from sqlite3 import connect
from os.path import dirname, join, realpath

db_path = join(dirname(realpath(__file__)), 'database.db')
conn = connect(db_path)
c = conn.cursor()

def frequency():
	freq_list = []
	try:
		all_data_list, notes_in_deck, number_of_characters, decknames, tos, filter_list, min_length, max_lenght, word_list, config, raw = getdata()
		unique = []
		value = []
		counter = 0
		for i in all_data_list:
			unique.append(i)
			value.append(raw.count(i))
		value, unique = zip(*sorted(zip(value, unique)))
		value, unique = (list(t) for t in zip(*sorted(zip(value, unique))))
		unique = unique[::-1]
		value = value[::-1]
		for i in unique:
			freq_results = (str(counter+1) + ": " + i + "(" + str(value[counter]) + ")"+ "\n")
			counter = counter + 1
			freq_list.append(freq_results)
	except:
		pass
	return freq_list
