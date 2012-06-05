#!/usr/bin/python2
__module_name__	= "meme.py"
__module_version__	= "2"
__module_description__	= "Meme Plugin; Generator Idea from Proxy"
__module_author__	= "Ferus"

import xchat
import urllib

def ignore():
	if (xchat.get_context()).get_info("channel") in ignore_chans:
		return True
	else:
		return False

def get_meme():
	meme_db = []
	memeurl = "http://api.automeme.net/text?lines=80"
	memes = urllib.urlopen(memeurl).read().replace('_','\x02').split("\n")
	for meme in memes:
		meme_db.append(meme)
	meme_db.pop()
	return meme_db

def meme():
	meme_db = []
	while True:
		if not meme_db:
			print("Getting moar memes!")
			meme_db = get_meme()
		memestr = meme_db[0]
		del meme_db[0]
		yield memestr

def parse(word, word_eol, userdata):
	if not ignore():
		if "!meme" in word[1]:
			xchat.command("SAY "+next(m))
		elif "!gaymeme" in word[1]: #Requires gay.pl
			xchat.command("GAY -1 "+next(m))
		elif "!usameme" in word[1]:
			xchat.command("GAY -2 "+next(m))
		elif "!boxmeme" in word[1]:
			xchat.command("GAY -1 -box "+next(m))
	return None

ignore_chans = ['']
m = meme()
#The hooks go here	
xchat.hook_print('Channel Message', parse)
print ("Loaded " + __module_author__ +"'s " + __module_description__)


