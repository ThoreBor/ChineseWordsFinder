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
	all_data_list_r = all_data_list[::-1]
	pair_list = []
	word_list = []
	counter = 0
	found = 0
	for pair in itertools.combinations(all_data_list,2):
		pair_list.append(pair)
	for pair in itertools.combinations(all_data_list_r,2):
		pair_list.append(pair)
	possible_combi = len(pair_list)
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
	anki_file =  open("C:/Users/"+username+"/Desktop/WordsFound.txt", "w", encoding="utf-8")
	anki_file.write(textfile_info)
	#<b>Unique characters: </b>%(all_data)s<br>
	info = '''
		<b>Unique characters found: </b>%(number_of_characters)s<br>
		<b>Possible two syllable Words: </b>%(possible_combi)s<br>
		<div>
			This add-on will look for Chinese words in the <b>%(possible_combi)s</b> possible two syllable words made out of the <b>%(number_of_characters)s</b> characters found in your collection
			by looking each one up in the CC-CEDICT dictionary (published by MDBG).<br><br>
			<i> Depending on how many characters there are in your collection, this could take up to several hours and use quite a lot of CPU.
			If you have a large collection, I recommend running this add-on overnight with all other programs closed.</i><br>
			<i>Maybe consider making a backup before you continue - just in case something goes wrong. </i>
			<br><br>
			<b>Do you want to continue?<b>
		''' % {
			'all_data': all_data,
			'number_of_characters': number_of_characters,
			'possible_combi': (f"{possible_combi:,d}")
		}
	if not askUser(info, title="Chinese Words Finder"):
		return

	start = time.time()
	#time_left = "Time is being calculated..."

	db_path = join(dirname(realpath(__file__)), 'CC-CEDICT_dictionary.db')
	conn = connect(db_path)
	c = conn.cursor()

	mw.progress.start(immediate=True, min=0, max=possible_combi)
	for i in pair_list:
		if counter > 99:
			if counter == 100:
				end = time.time()
			timetotal = (end - start)
			searches_left = (possible_combi - counter)
			time_per_search = timetotal/100
			time_left = searches_left*time_per_search
			global seconds
			global minutes
			global hours
			seconds = time_left
			minutes = seconds/60
			hours = minutes/60
			seconds = math.floor(seconds)
			minutes = round(minutes, 1)
			hours = round(hours, 1)
		counter = counter + 1
		single = ''.join(i)
		c.execute('SELECT * FROM dictionary WHERE hanzi_simp=? OR hanzi_trad=?',(single, single))
		for row in c.fetchall():
			word = row[0]
			word_list.append(word)
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
			#p = pinyin.decode(p)
			anki_line = str(traditional + "	" + simplified + "	" + p + "	" + english + "\n")
			anki_file.write(anki_line)
			if float(minutes) > 60:
				msg = '''
				<b>%(counter)d / %(total)d <br>
				<b>Searching:</b> %(hanzi)s<br>
				<b>Words found:</b> %(found)d<br>
				<b>Time remaining (hours):</b> %(time_left)s<br>
				<i> Ctrl+Shift+ESC to cancel.<i>
				''' % {
					'hanzi': single,
					'counter': counter,
					'total': possible_combi,
					'found': found,
					'time_left': hours
				}
				mw.progress.update(label=msg, value=counter)
			if float(minutes) <= 60 and float(minutes) > 1:
				msg = '''
				<b>%(counter)d / %(total)d <br>
				<b>Searching:</b> %(hanzi)s<br>
				<b>Words found:</b> %(found)d<br>
				<b>Time remaining (minutes):</b> %(time_left)s<br>
				<i> Ctrl+Shift+ESC to cancel.<i>
				''' % {
					'hanzi': single,
					'counter': counter,
					'total': possible_combi,
					'found': found,
					'time_left': minutes
				}
				mw.progress.update(label=msg, value=counter)
			if float(minutes) < 1:
					msg = '''
					<b>%(counter)d / %(total)d <br>
					<b>Searching:</b> %(hanzi)s<br>
					<b>Words found:</b> %(found)d<br>
					<b>Time remaining (seconds):</b> %(time_left)s<br>
					<i> Ctrl+Shift+ESC to cancel.<i>
					''' % {
						'hanzi': single,
						'counter': counter,
						'total': possible_combi,
						'found': found,
						'time_left': seconds
					}
					mw.progress.update(label=msg, value=counter)
	anki_file.close()
	mw.progress.finish()
	showInfo("I found %s words. You can find the text file on your desktop." % (found), title="Chinese Words Finder")


# create a new menu item, "test"
action = QAction("Chinese Words Finder", mw)
# set it to call testFunction when it's clicked
action.triggered.connect(WordFinder)
# and add it to the tools menu
mw.form.menuTools.addAction(action)
