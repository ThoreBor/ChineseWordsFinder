from .getdata import getdata
from aqt import mw
from aqt.utils import askUser, showWarning, tooltip
from aqt.qt import *
from sqlite3 import connect
from os.path import dirname, join, realpath
import getpass

db_path = join(dirname(realpath(__file__)), 'database.db')
conn = connect(db_path)
c = conn.cursor()
all_data = ""
this_version = "V1.5"
config = mw.addonManager.getConfig(__name__)
language = config['language']

def frequency():
	try:
		all_data_list, notes_in_deck, number_of_characters, decknames, tos, filter_list, min_length, max_lenght, word_list, config, raw = getdata()
		unique = []
		value = []
		f_file = ""
		counter = 0
		username = getpass.getuser()
		for i in all_data_list:
			unique.append(i)
			value.append(raw.count(i))
		value, unique = zip(*sorted(zip(value, unique)))
		value, unique = (list(t) for t in zip(*sorted(zip(value, unique))))
		unique = unique[::-1]
		value = value[::-1]

		for i in unique:
			f_file = f_file + "\n"+ str(counter+1) + ": " + i + "(" + str(value[counter]) + ")"
			counter = counter + 1

		unique2 = unique[:10]
		value2 = value[:10]
		f_info = ''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Frequency info' ").fetchone()) % {'decknames': decknames, 'notes': len(notes_in_deck)}
		counter = 0
		for i in unique2:
			f_info = f_info + "<br>"+ str(counter+1) + ": " + i + "(" + str(value2[counter]) + ")"
			counter = counter + 1
		f_info = f_info + ''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Frequency info 2' ").fetchone())
		if not askUser(f_info, title=''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Title 3' ").fetchone())):
				return
		else:
			try:
				anki_file =  open("C:/Users/"+username+"/Desktop/CharacterFrequency.txt", "w", encoding="utf-8")
				anki_file.write(f_file)
				tooltip(''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'File location desktop' ").fetchone()))
			except:
				anki_file =  open("CharacterFrequency.txt", "w", encoding="utf-8")
				anki_file.write(f_file)
				tooltip(''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'File location media folder' ").fetchone()))
	except:
		showWarning(''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Frequency warning' ").fetchone()))