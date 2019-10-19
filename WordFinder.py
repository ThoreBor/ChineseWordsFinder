from .getdata import getdata
from .import_file import importfile
from aqt import mw
from aqt.utils import showInfo, askUser
from sqlite3 import connect
from os.path import dirname, join, realpath
import getpass

db_path = join(dirname(realpath(__file__)), 'database.db')
conn = connect(db_path)
c = conn.cursor()
config = mw.addonManager.getConfig(__name__)
language = config['language']

def WordFinder():
	all_data_list, notes_in_deck, number_of_characters, decknames, tos, filter_list, min_length, max_lenght, word_list, config, raw = getdata()
	if filter_list == [""]:
		filter_list = []
	username = getpass.getuser()
	textfile_info = ''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Output-file info' ").fetchone())  % {'config':config}
	try:
		anki_file =  open("C:/Users/"+username+"/Desktop/WordsFound.txt", "w", encoding="utf-8")
		anki_file.write(textfile_info)
		d = ''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'File location desktop' ").fetchone())
	except:
		anki_file =  open(join(dirname(realpath(__file__)), 'WordsFound.txt'), "w", encoding="utf-8")
		anki_file.write(textfile_info)
		d = ''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'File location media folder' ").fetchone())
	info = ''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Word Finder info' ").fetchone()) % {'number_of_characters':number_of_characters, 'deckname':decknames, 'note_number': len(notes_in_deck), 'd': d}
	
	raw =  open(join(dirname(realpath(__file__)), 'WordsFound_raw.txt'), "w", encoding="utf-8")
	if not askUser(info, title=''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Title 1' ").fetchone())):
		return

	counter = 0
	found = 0

	mw.progress.start(immediate=True, min=0, max=117272)
		
	c.execute('SELECT * FROM dictionary ORDER BY freq DESC')
	
	for row in c.fetchall():
		trad = row[tos]
		counter = counter + 1
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
						line = str(simplified + "\t" + traditional + "\t" +  p + "\t" + english + "\n")
						anki_file.write(line)
						raw.write(line)
					else:
						continue

		msg = d = ''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Word Finder progress' ").fetchone()) % {'hanzi': trad, 'counter': counter, 'total': 117272, 'found': found,}
		mw.progress.update(label=msg, value=counter)
	anki_file.close()
	raw.close()
	mw.progress.finish()
	if config["checked"] == "True":
		importfile("WordsFound_raw.txt", config["import_deck"], config["import_notetype"])
	showInfo(''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Words found' ").fetchone()) % (found), title=''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Title 1' ").fetchone()))