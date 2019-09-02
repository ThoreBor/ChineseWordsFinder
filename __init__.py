# Chinese Words Finder V1.4 Copyright 2019 Thore Tyborski

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Dictionary used:
# CC-CEDICT
# Community maintained free Chinese-English dictionary.

# Published by MDBG

# License:
# Creative Commons Attribution-ShareAlike 4.0 International License
# https://creativecommons.org/licenses/by-sa/4.0/

# Referenced works:
# CEDICT - Copyright (C) 1997, 1998 Paul Andrew Denisowski

# CC-CEDICT can be downloaded from:
# https://www.mdbg.net/chinese/dictionary?page=cc-cedict

# Additions and corrections can be sent through:
# https://cc-cedict.org/editor/editor.php

# For more information about CC-CEDICT see:
# https://cc-cedict.org/wiki/
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

all_data = ""
this_version = "V1.4"

def extractChinese(output):
	extract = re.compile(u'[^\u4E00-\u9FA5]')
	output = extract.sub(r'', output) 
	return output

def getdata():
	all_data = ""
	notes_in_deck = []
	decknames = ""
	word_list = []
	config = mw.addonManager.getConfig(__name__)
	deckname = config['deckname']
	tos = config['tos']
	filter_active = config['filter_active']
	filter_list = config['filter']
	min_length = config['min_length']
	max_lenght = config['max_lenght']
	word_list = []
	if max_lenght == 0:
		max_lenght = 25
	for i in deckname:
		decknames = decknames + i + " and "
		searchterm = "deck:'" + i + "'"
		notes_in_deck = notes_in_deck + mw.col.findNotes(searchterm)

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

	decknames = decknames[:-5]
	all_data = extractChinese(all_data)
	raw = all_data
	all_data = ''.join(set(all_data))
	all_data_list = list(all_data)
	number_of_characters = len(all_data_list)
	
	return all_data_list, notes_in_deck, number_of_characters, decknames, tos, filter_active, filter_list, min_length, max_lenght, word_list, config, raw

def WordFinder():
	all_data_list, notes_in_deck, number_of_characters, decknames, tos, filter_active, filter_list, min_length, max_lenght, word_list, config, raw = getdata()
	username = getpass.getuser()
	textfile_info = '''This data comes from:
CC-CEDICT
Community maintained free Chinese-English dictionary.
 
Published by MDBG
 
License:
Creative Commons Attribution-ShareAlike 4.0 International License
https://creativecommons.org/licenses/by-sa/4.0/
 
Referenced works:
CEDICT - Copyright (C) 1997, 1998 Paul Andrew Denisowski
 
CC-CEDICT can be downloaded from:
https://www.mdbg.net/chinese/dictionary?page=cc-cedict
 
Additions and corrections can be sent through:
https://cc-cedict.org/editor/editor.php
 
For more information about CC-CEDICT see:
https://cc-cedict.org/wiki/

Configurations: %(config)s

If you delete the info text (everything above, including this line), this text file can be imported into Anki. You need a note type with four fields: traditional, simplified, pinyin, english.

''' % {'config':config}
	try:
		anki_file =  open("C:/Users/"+username+"/Desktop/WordsFound.txt", "w", encoding="utf-8")
		anki_file.write(textfile_info)
		d = "You'll find the text file on your desktop."
	except:
		anki_file =  open("WordsFound.txt", "w", encoding="utf-8")
		anki_file.write(textfile_info)
		d = "You'll find the text file in the Anki collection.media folder."
	info = '''
	<b>Unique characters in %(deckname)s (%(note_number)s notes): %(number_of_characters)s</b><br>
	This add-on finds all Chinese words in the CC-CEDICT dictionary that only use the characters
	in the decks you selected and creates a text file with the words, pinyin and English translation
	that can be imported into Anki. %(d)s This should only take a few seconds. 
	<br><br><b>Go to CWF>Configurations (Ctrl+C) and follow the instructions to change the deck(s) you want to analyse and to customize other options.</b>
	<br><br>Licensed under the MIT License.<br>
	<div>
	<b>Do you want to continue?<b>
	''' % {'number_of_characters':number_of_characters, 'deckname':decknames, 'note_number': len(notes_in_deck), 'd': d
				}
	if not askUser(info, title="Chinese Words Finder"):
		return

	counter = 0
	found = 0
	db_path = join(dirname(realpath(__file__)), 'database.db')
	conn = connect(db_path)
	c = conn.cursor()

	mw.progress.start(immediate=True, min=0, max=117272)
		
	c.execute('SELECT * FROM dictionary')
	
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
				if filter_active == "True":
					if any(x in english.lower() for x in filter_list):
						continue

					else:
						if trad not in word_list:
							found = found + 1
							line = str(traditional + "	" + simplified + "	" + p + "	" + english + "\n")
							anki_file.write(line)
						else:
							continue
				else:
					if trad not in word_list:
						found = found + 1
						line = str(traditional + "	" + simplified + "	" + p + "	" + english + "\n")
						anki_file.write(line)
					else:
						continue

		msg = '''
		<b>%(counter)d / %(total)d <br>
		<b>Searching:</b> %(hanzi)s<br>
		<b>Words found:</b> %(found)d<br>
		''' % {
			'hanzi': trad,
			'counter': counter,
			'total': 117272,
			'found': found,
		}
		mw.progress.update(label=msg, value=counter)
	anki_file.close()
	mw.progress.finish()
	showInfo("%s words found." % (found), title="Chinese Words Finder")

def hskFinder():
	all_data_list, notes_in_deck, number_of_characters, decknames, tos, filter_active, filter_list, min_length, max_lenght, word_list, config, raw = getdata()
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

	textfile_info = '''This data comes from:
CC-CEDICT
Community maintained free Chinese-English dictionary.
 
Published by MDBG
 
License:
Creative Commons Attribution-ShareAlike 4.0 International License
https://creativecommons.org/licenses/by-sa/4.0/
 
Referenced works:
CEDICT - Copyright (C) 1997, 1998 Paul Andrew Denisowski
 
CC-CEDICT can be downloaded from:
https://www.mdbg.net/chinese/dictionary?page=cc-cedict
 
Additions and corrections can be sent through:
https://cc-cedict.org/editor/editor.php
 
For more information about CC-CEDICT see:
https://cc-cedict.org/wiki/

HSK levels are from: http://www.chinesetest.cn/godownload.do

Configurations: %(config)s

If you delete the info text (everything above, including this line), this text file can be imported into Anki. You need a note type with four fields: simplified, traditional, pinyin, english and HSK level.

''' % {'config':config}
	try:
		anki_file =  open("C:/Users/"+username+"/Desktop/MissingHSK.txt", "w", encoding="utf-8")
		anki_file.write(textfile_info)
		d = "You'll find the results in a file on your desktop."
	except:
		anki_file =  open("MissingHSK.txt", "w", encoding="utf-8")
		anki_file.write(textfile_info)
		d = "You'll find the results in a file in the Anki collection.media folder."
	info = '''
	<div>This tool finds all HSK %(hsk)s words that are missing in %(deckname)s (%(note_number)s notes).</div>
	<br><br><b>Go to CWF>Configurations (Ctrl+C) and follow the instructions to change the deck(s) you want to analyse and HSK level.</b><br>%(d)s
	<br><br>Licensed under the MIT License.<br>
	<div>
	<b>Do you want to continue?<b>
	''' % {'hsk': HSK, 'deckname':decknames, 'note_number': len(notes_in_deck), "d": d
				}
	if not askUser(info, title="Missing HSK words"):
		return

	counter = 0
	found = 0
	db_path = join(dirname(realpath(__file__)), 'database.db')
	conn = connect(db_path)
	c = conn.cursor()

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
			found = found + 1
			line = str(traditional + "	" + simplified + "	" + p + "	" + english + "	" + hsk_lvl + "\n")
			anki_file.write(line)

		msg = '''
			<b>%(counter)d / %(total)d <br>
			<b>Searching:</b> %(hanzi)s<br>
			<b>Words found:</b> %(found)d<br>
			''' % {
				'hanzi': hanzi,
				'counter': counter,
				'total': 5000,
				'found': found,
			}
		mw.progress.update(label=msg, value=counter)
	for i in word_list:
		if i not in hsk_word_list:
			extra = extra + 1
			extra_list.append(i)
	anki_file.write(str(extra_list))
	anki_file.close()
	mw.progress.finish()
	showInfo("%s words found. There were %s words, that aren't in the HSK list. They are listed at the end of the text file." % (found, extra), title="Missing HSK words")

def frequency():
	try:
		all_data_list, notes_in_deck, number_of_characters, decknames, tos, filter_active, filter_list, min_length, max_lenght, word_list, config, raw = getdata()
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
			f_file = f_file + "\n"+ str(counter+1) + ": " + i + ": " + str(value[counter])
			counter = counter + 1

		unique2 = unique[:10]
		value2 = value[:10]
		f_info = "<b>Top 10 characters in " + decknames + "(" + str(len(notes_in_deck)) + " notes) " + ":</b><br>"
		counter = 0
		for i in unique2:
			f_info = f_info + "<br>"+ str(counter+1) + ": " + i + ": " + str(value2[counter])
			counter = counter + 1
		f_info = f_info + "<br><br><b>Go to CWF>Configurations (Ctrl+C) and follow the instructions to change the deck(s) you want to analyse.<br><br>Do you want to see the complete results?"
		if not askUser(f_info, title="Character frequency"):
				return
		else:
			try:
				anki_file =  open("C:/Users/"+username+"/Desktop/CharacterFrequency.txt", "w", encoding="utf-8")
				anki_file.write(f_file)
				tooltip("The file is on your desktop.")
			except:
				anki_file =  open("CharacterFrequency.txt", "w", encoding="utf-8")
				anki_file.write(f_file)
				tooltip("The file is in the collection.media folder.")
	except:
		showWarning("Go to CWF>Configurations (Ctrl+C) and select the deck you want to analyse.")

###MENU###
def About():
	showInfo("<b>%s</b><br> The code for this add-on is available on <a href='https://github.com/ThoreBor/ChineseWordsFinder'>Git Hub.</a><br>Licensed under the <a href='https://github.com/ThoreBor/ChineseWordsFinder/blob/master/License.txt'>MIT License.</a><br><a href='https://ko-fi.com/U7U0XUA5'>Support Me</a>" % this_version, title="Chinese Words Finder")

def github():
	webbrowser.open('https://github.com/ThoreBor/ChineseWordsFinder/issues')

def config():
	addon = "2048169015"
	mw.mgr = mw.addonManager
	conf = mw.addonManager.getConfig(addon)
	ConfigEditor(mw, addon, conf)

def Update():
	try:
		url = 'https://chinesewordsfinderupdates.netlify.com'
		headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36 OPR/62.0.3331.116'}
		page = requests.get(url, headers=headers)
		soup = BeautifulSoup(page.content, 'html.parser')
		version = soup.find(id='newest_verion').get_text()
		log = soup.find(id='changelog').get_text()
		log_list = log.split(',')
		log = ""
		for i in log_list:
			log = log + "- " + i + "<br>"
	except:
		showWarning("Please check your internet connection.", title="Chinese Words Finder ")
		return
	if version != this_version:
		info = '''You can update Chinese Words Finder to Version %(version)s. You are currently using version %(this_version)s.<br><br><b>Changes:</b><br>%(log)s <br><br><b>Do you want to update now?</b>''' % {'version':version, 'this_version': this_version, 'log':log}

		if not askUser(info, title="Chinese Words Finder - UPDATE!"):
			return
		else:
			download()
	else:
		showInfo("You are using the newest version (%s)." % this_version, title="Chinese Words Finder")

def download():
	try:
		mw.mgr = mw.addonManager
		updated = ['2048169015']
		mw.mgr.downloadIds(updated)
		tooltip(_("Chinese Words Finder was updated successfully."))
	except:
		tooltip(_("Update failed..."))
	
def add_menu(Name, Button, exe, *sc):
	action = QAction(Button, mw)
	action.triggered.connect(exe)
	if not hasattr(mw, 'menu'):
		mw.menu = {}
	if Name not in mw.menu:
		add = QMenu(Name, mw)
		mw.menu[Name] = add
		mw.form.menubar.insertMenu(mw.form.menuTools.menuAction(), add)
	mw.menu[Name].addAction(action)
	for i in sc:
		action.setShortcut(QKeySequence(i))

add_menu('CWF','Chinese Words Finder', WordFinder, 'Ctrl+W')
add_menu('CWF','Find Missing HSK words', hskFinder, 'Ctrl+H')
add_menu('CWF', 'Character frequency', frequency, 'Ctrl+F')
add_menu('CWF','Configurations', config, 'Ctrl+C')
add_menu('CWF','Check for Updates', Update, 'Ctrl+U')
add_menu('CWF','Make a feature request or report a bug', github)
add_menu('CWF','About', About)
###MENU###


