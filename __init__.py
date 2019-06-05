# Copyright 2019 Thore Tyborski

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
all_data = ""
seconds = 0
minutes = 0
hours = 0
possible_combi = 116721

def extractChinese(output):
	extract = re.compile(u'[^\u4E00-\u9FA5]')
	output = extract.sub(r'', output) 
	return output

def WordFinder():	
	for flds in mw.col.db.execute("select flds from notes"):
		global all_data
		all_data = all_data + str(flds)

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
Version: 2019-02-07 07:15:06

If you delete the info text (everything above, including this line), this text file can be imported into Anki. You need a note type with four fields: traditional, simplified, pinyin, english.

'''
	try:
		anki_file =  open("C:/Users/"+username+"/Desktop/WordsFound.txt", "w", encoding="utf-8")
		anki_file.write(textfile_info)
	except:
		anki_file =  open("WordsFound.txt", "w", encoding="utf-8")
		anki_file.write(textfile_info)
	#<b>Unique characters: </b>%(all_data)s<br>
	info = '''
		<b>Unique characters found: </b>%(number_of_characters)s<br>
		This add-on finds all Chinese words in the CC-CEDICT dictionary that only use the characters
		in your collection and creates a text file with the words, pinyin and English translation
		that can be imported into Anki. This should only take a few seconds. 
		<br> If you use traditional characters got to Tools>Add-ons>Chinese Words Finder>Config and follow the instructions. 
		<br>Licensed under the MIT License.
		<div>
		<b>Do you want to continue?<b>
		''' % {'number_of_characters':number_of_characters
					}
	if not askUser(info, title="Chinese Words Finder"):
		return

	start = time.time()
	#time_left = "Time is being calculated..."

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
					found = found + 1
				except:
					pass
				traditional = x[0]
				simplified = x[1]
				p = x[2]
				english = x[3]
				english = english[:-3]
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
					'time_left': minutes
				}
				mw.progress.update(label=msg, value=counter)
	anki_file.close()
	mw.progress.finish()
	showInfo("%s words found. If the file is not on your desktop, you'll find it in the addon folder." % (found), title="Chinese Words Finder")


# create a new menu item, "test"
action = QAction("Chinese Words Finder", mw)
# set it to call testFunction when it's clicked
action.triggered.connect(WordFinder)
# and add it to the tools menu
mw.form.menuTools.addAction(action)
