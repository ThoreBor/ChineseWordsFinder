from anki.importing import TextImporter
from aqt import mw
from os.path import dirname, join, realpath
from aqt.utils import showWarning, tooltip
from sqlite3 import connect

db_path = join(dirname(realpath(__file__)), 'database.db')
conn = connect(db_path)
c = conn.cursor()
config = mw.addonManager.getConfig(__name__)
language = config['language']

def importfile(filename, deck, type):
	try:
		file = join(dirname(realpath(__file__)), filename)
		did = mw.col.decks.id(deck)
		mw.col.decks.select(did)
		m = mw.col.models.byName(type)
		deck = mw.col.decks.get(did)
		deck['mid'] = m['id']
		mw.col.decks.save(deck)
		m['did'] = did
		ti = TextImporter(mw.col, file)
		ti.initMapping()
		ti.run()
		tooltip('Successfully imported results.')
	except:
		showWarning('<b>Import error</b><br>Make sure that the notetype and deck exist and that you have enough fields.')