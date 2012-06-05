#!/usr/bin/python2.7
__module_name__ = "trap.py"
__module_version__ = "2.2"
__module_description__ = "Channel Trap Plugin"
__module_author__ = "Ferus"

import xchat
from random import randint

server = 'DatNode'
channel = '#ItsATrap'

def isChan():
	if (xchat.get_context()).get_info("network") == server:
		if(xchat.get_context()).get_info("channel") == channel:
			return True

def number():
	return str(randint(0,15))

def trap(word, word_eol, userdata):
	try:
		if isChan():
			if userdata:
				message = word[3].split()
				if number() in message:
					pass
				else:
					xchat.command("raw sajoin {0} {1}".format(word[0], channel))
			else: 
				xchat.command("raw sajoin {0} {1}".format(word[0], channel))
	except:
		pass
	return None

xchat.hook_print('Part', trap, userdata = False)
xchat.hook_print('Part with Reason', trap, userdata = True)
print("Loaded {0}, version {1}".format(__module_name__, __module_version__))


