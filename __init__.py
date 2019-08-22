# Chinese Words Finder V1.2 Copyright 2019 Thore Tyborski

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
from aqt.utils import showInfo, askUser
from aqt.qt import *
import itertools
import sqlite3
from sqlite3 import connect
from os.path import dirname, join, realpath
import re
import getpass
import random
import time
import math
import requests
from bs4 import BeautifulSoup
import webbrowser

all_data = ""
possible_combi = 117272

def Update():
	url = 'https://ankiweb.net/shared/info/2048169015'
	headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36 OPR/62.0.3331.116'}
	page = requests.get(url, headers=headers)
	soup = BeautifulSoup(page.content, 'html.parser')
	version = str(soup.find_all("h1"))
	version = version.replace('[</h1>', '')
	version = version.replace('</h1>]', '')
	version = version.split("Chinese Words Finder ",1)[1]
	try:
		log = soup.findAll("div", {"class": "shared-item-description pb-3"})
		log = str(log)
		log = log.split("<b>V1.4:</b>",1)[1]
		log = log[:log.index("<b>V1.3:</b>")]
		log = log.strip()
		log = log.replace("-",", ")
		log = log [3:]
	except:
		log ="<i>There was an error</i>"
	if version != "V1.3":
		info = '''You can update Chinese Words Finder to Version %(version)s. You are currently using version V1.3.<br><br><b>Changes:</b><br>%(log)s <br><br><b>Do you want to update now?</b>''' % {'version':version, 'log':log}

		if not askUser(info, title="Chinese Words Finder - UPDATE!"):
			WordFinder()
			return
		else:
			webbrowser.open('https://ankiweb.net/shared/info/2048169015', new = 2)
	else:
		WordFinder()

def extractChinese(output):
	extract = re.compile(u'[^\u4E00-\u9FA5]')
	output = extract.sub(r'', output) 
	return output

def WordFinder():	
	notes_in_deck = []
	decknames = ""
	config = mw.addonManager.getConfig(__name__)
	deckname = config['deckname']
	filter_active = config['filter_active']
	filter_list = config['filter']
	min_length = config['min_length']
	max_lenght = config['max_lenght']
	if max_lenght == 0:
		max_lenght = 25
	for i in deckname:
		decknames = decknames + i + " and "
		searchterm = "deck:'" + i + "'"
		#searchterm = "deck:'%s'" % deckname
		notes_in_deck = mw.col.findNotes(searchterm)

	
		for i in notes_in_deck:
			global all_data
			all_data = all_data + str(mw.col.db.scalar("SELECT flds FROM notes WHERE id=?" ,i, ))
	decknames = decknames[:-5]
	all_data = extractChinese(all_data)
	all_data = ''.join(set(all_data))
	all_data_list = list(all_data)
	number_of_characters = len(all_data_list)
	counter = 0
	found = 0
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

If you delete the info text (everything above, including this line), this text file can be imported into Anki. You need a note type with four fields: traditional, simplified, pinyin, english.

'''
	try:
		anki_file =  open("C:/Users/"+username+"/Desktop/WordsFound.txt", "w", encoding="utf-8")
		anki_file.write(textfile_info)
	except:
		anki_file =  open("WordsFound.txt", "w", encoding="utf-8")
		anki_file.write(textfile_info)
	info = '''
		<b>Unique characters in %(deckname)s: </b>%(number_of_characters)s<br>
		This add-on finds all Chinese words in the CC-CEDICT dictionary that only use the characters
		in your collection and creates a text file with the words, pinyin and English translation
		that can be imported into Anki. This should only take a few seconds. 
		<br><br><b>Go to Tools>Add-ons>Chinese Words Finder>Config and follow the instructions to change the deck(s) you want to analyse and to customize other options.</b>
		<br><br>Licensed under the MIT License.<br>
		<div>
		<b>Do you want to continue?<b>
		''' % {'number_of_characters':number_of_characters, 'deckname':decknames
					}
	if not askUser(info, title="Chinese Words Finder"):
		return

	db_path = join(dirname(realpath(__file__)), 'CC-CEDICT_dictionary.db')
	conn = connect(db_path)
	c = conn.cursor()

	mw.progress.start(immediate=True, min=0, max=possible_combi)
		
	c.execute('SELECT * FROM dictionary')

	config = mw.addonManager.getConfig(__name__)
	tos = config['tos']


	for row in c.fetchall():

		trad = row[tos]
		counter = counter + 1
		l = len(trad)
		lc = 0
		for i in trad:
			if i in all_data_list:
				lc = lc + 1
				
		if lc == l:
			try:
				x = list(row)
			except:
				pass
			traditional = x[0]
			simplified = x[1]
			p = x[2]
			english = x[3]
			english = english[:-3]

			if len(traditional) >= min_length and len(traditional) < max_lenght:  
				if filter_active == "True":
					if any(x in english.lower() for x in filter_list):
						continue

					else:
						found = found + 1
						line = str(traditional + "	" + simplified + "	" + p + "	" + english + "\n")
						anki_file.write(line)
				else:
					found = found + 1
					line = str(traditional + "	" + simplified + "	" + p + "	" + english + "\n")
					anki_file.write(line)

			msg = '''
			<b>%(counter)d / %(total)d <br>
			<b>Searching:</b> %(hanzi)s<br>
			<b>Words found:</b> %(found)d<br>
			''' % {
				'hanzi': trad,
				'counter': counter,
				'total': possible_combi,
				'found': found,
			}
			mw.progress.update(label=msg, value=counter)
	anki_file.close()
	mw.progress.finish()
	showInfo("%s words found. If the file is not on your desktop, you'll find it in the addon folder." % (found), title="Chinese Words Finder")


action = QAction("Chinese Words Finder", mw)
action.setShortcut(QKeySequence("Ctrl+Shift+W"))
action.triggered.connect(Update)
mw.form.menuTools.addAction(action)
