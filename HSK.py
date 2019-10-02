from .getdata import getdata
from aqt import mw
from aqt.utils import showInfo, askUser, showWarning, tooltip
from PyQt5.QtWidgets import QAction, QActionGroup, QMenu
from aqt.qt import *
import sqlite3
from sqlite3 import connect
from os.path import dirname, join, realpath
import re
import getpass
import requests
from bs4 import BeautifulSoup
import webbrowser
from aqt.addons import ConfigEditor, AddonsDialog

db_path = join(dirname(realpath(__file__)), 'database.db')
conn = connect(db_path)
c = conn.cursor()
all_data = ""
this_version = "V1.5"
config = mw.addonManager.getConfig(__name__)
language = config['language']


def hskFinder():
	all_data_list, notes_in_deck, number_of_characters, decknames, tos, filter_list, min_length, max_lenght, word_list, config, raw = getdata()
	username = getpass.getuser()
	if tos == 0:
		tos = 1
	else:
		tos = 0

	config = mw.addonManager.getConfig(__name__)
	HSK = config['HSK']
	hsk_list = []
	for i in range(HSK + 1):
		hsk_list.append("HSK "+str(i))

	textfile_info = ''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Output-file info' ").fetchone())  % {'config':config} % {'config':config}
	try:
		anki_file =  open("C:/Users/"+username+"/Desktop/MissingHSK.txt", "w", encoding="utf-8")
		anki_file.write(textfile_info)
		d = ''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'File location desktop' ").fetchone())
	except:
		anki_file =  open("MissingHSK.txt", "w", encoding="utf-8")
		anki_file.write(textfile_info)
		d = ''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'File location media folder' ").fetchone())
	info = ''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'HSK info' ").fetchone()) % {'hsk': HSK, 'deckname':decknames, 'note_number': len(notes_in_deck), "d": d}
	if not askUser(info, title=''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Title 2' ").fetchone())):
		return

	counter = 0
	found = 0

	mw.progress.start(immediate=True, min=0, max=5000)
		
	c.execute('SELECT * FROM HSK')
	 
	hsk_word_list = []
	extra = 0 
	extra_list = []

	for row in c.fetchall():
		counter = counter + 1
		hanzi = row[tos]
		hsk_word_list.append(hanzi)
		hsk_lvl = row[4]
		if hanzi not in word_list and hsk_lvl in hsk_list:
			traditional = row[0]
			simplified = row[1]
			p = row[2]
			english = row[3]
			english = english.replace("\n", "")
			found = found + 1
			line = str(traditional + "\t" + simplified + "\t" + p + "\t" + english + "\t" + hsk_lvl + "\n")
			anki_file.write(line)

		msg = ''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'HSK progress' ").fetchone()) % {'hanzi': hanzi, 'counter': counter, 'total': 5000, 'found': found,}
		mw.progress.update(label=msg, value=counter)
	for i in word_list:
		if i not in hsk_word_list:
			extra = extra + 1
			extra_list.append(i)
	anki_file.write(str(extra_list))
	anki_file.close()
	mw.progress.finish()
	showInfo(''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'HSK found' ").fetchone()) % (found, extra), title=''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Title 2' ").fetchone()))
