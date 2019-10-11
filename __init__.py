# Chinese Words Finder V1.6 Copyright 2019 Thore Tyborski

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

from aqt import mw
from aqt.utils import showInfo, askUser, showWarning, tooltip
from PyQt5.QtWidgets import QAction, QMenu
from aqt.qt import *
from sqlite3 import connect
from os.path import dirname, join, realpath
import requests
from bs4 import BeautifulSoup
import webbrowser
from .WordFinder import WordFinder
from .HSK import hskFinder
from .freq import frequency
from .config import start_config

db_path = join(dirname(realpath(__file__)), 'database.db')
conn = connect(db_path)
c = conn.cursor()
all_data = ""
this_version = "V1.6"
config = mw.addonManager.getConfig(__name__)
language = config['language']

###MENU###
def reviews():
	try:
		url = 'https://ankiweb.net/shared/info/2048169015'
		headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36 OPR/62.0.3331.116'}
		page = requests.get(url, headers=headers)
		soup = BeautifulSoup(page.content, 'html.parser')
		review_list = soup.findAll("div", {"class": "review"})
		review = ""
		for i in review_list[:3]:
			review = review + "<br>"+"<i>"+str(i)+"</i>"
		return review
	except:
		review = ''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Review error' ").fetchone())
		return review
def About():
	review = reviews()
	showInfo(''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'About' ").fetchone()) % {'version':this_version,'review':review}, title=''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Title 1' ").fetchone()))

def github():
	webbrowser.open('https://github.com/ThoreBor/ChineseWordsFinder/issues')

def config():
	s = start_config()
	if s.exec():
		pass

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
		showWarning(''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Update error' ").fetchone()), title=''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Title 1' ").fetchone()))
		return
	if version != this_version:
		info = ''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Update info' ").fetchone()) % {'version':version, 'this_version': this_version, 'log':log}

		if not askUser(info, title=''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Title 1' ").fetchone())):
			return
		else:
			download()
	else:
		showInfo(''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'No Update' ").fetchone()) % this_version, title=''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Title 1' ").fetchone()))

def download():
	try:
		mw.mgr = mw.addonManager
		updated = ['2048169015']
		mw.mgr.downloadIds(updated)
		tooltip(_(''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Download success' ").fetchone())))
	except:
		tooltip(_(''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Download fail' ").fetchone())))
	
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

add_menu('CWF',''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Title 1' ").fetchone()), WordFinder, 'Ctrl+W')
add_menu('CWF',''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Title 2' ").fetchone()), hskFinder, 'Ctrl+H')
add_menu('CWF',''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Title 3' ").fetchone()), frequency, 'Ctrl+F')
add_menu('CWF',''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Title 4' ").fetchone()), config, 'Ctrl+Alt+C')
add_menu('CWF',''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Title 5' ").fetchone()), Update, 'Ctrl+U')
add_menu('CWF',''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Title 6' ").fetchone()), github)
add_menu('CWF',''.join(c.execute("SELECT "+language+" FROM language WHERE Description = 'Title 7' ").fetchone()), About)
###MENU###


