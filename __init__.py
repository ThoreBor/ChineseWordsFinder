from aqt import mw
from aqt.utils import showInfo, showWarning
from PyQt5.QtWidgets import QAction, QMenu
from aqt.qt import *

from sqlite3 import connect
from os.path import dirname, join, realpath
import webbrowser

from .Ui import start_main

all_data = ""
this_version = "v2.2"

###MENU###

def About():
	showInfo("""<h2>Chinese Words Finder %(version)s</h2><br>This add-on uses the <a href="https://cc-cedict.org/wiki/">CC-CEDICT</a> dictionary.
	It is licensed under the <a href="https://creativecommons.org/licenses/by-sa/3.0/">Creative Commons Attribution-Share Alike 3.0 License</a>.
	<br>The HSK list can be downloaded <a href="http://www.chinesetest.cn/godownload.do">here.</a><br>The results of 'Chinese Word Finder' are 
	ordered by frequency based on the results of the BCC corpus. The complete wordlist can be downloaded 
	<a href="http://bcc.blcu.edu.cn/downloads/resources/BCC_LEX_Zh.zip">here.</a><br>
	<a href="https://www.plecoforums.com/threads/word-frequency-list-based-on-a-15-billion-character-corpus-bcc-blcu-chinese-corpus.5859/">More 
	info about the corpus.</a><br><br>The code for this add-on is available on 
	<a href='https://github.com/ThoreBor/ChineseWordsFinder'>GitHub. </a>Licensed under the 
	<a href='https://github.com/ThoreBor/ChineseWordsFinder/blob/master/License.txt'>MIT License.</a><br><br>
	If you like this add-on, rate and review it on <a href='https://ankiweb.net/shared/info/2048169015'>Anki Web</a>, 
	or contribute code on GitHub.</b><br><div>Icon made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> 
	from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div><br><b>©Thore Tyborski 2020</b>""" 
	% {'version':this_version}, title='About')

def github():
	webbrowser.open('https://github.com/ThoreBor/ChineseWordsFinder/issues')

def Main():
	s = start_main()
	if s.exec():
		pass

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

add_menu('&CWF',"&Start", Main, 'Ctrl+W')
add_menu('&CWF',"&Make a feature request or report a bug", github)
add_menu('&CWF',"&About", About)