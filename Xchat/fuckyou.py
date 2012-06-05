#!/usr/bin/python2
__module_name__ = "fuckyou.py"
__module_version__ = "1.0"
__module_description__ = "Sajoin Script"
__module_info__ = "Sajoin to over9000 channels"

import xchat
from random import choice
import string

def sajoin(word, word_eol, userdata):
	derp = 0
	try:
		number = int(word[2])
	except:
		number = ''
	if word[1] and number:
		while derp < number:
			channel = '#'+''.join(choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(1,10))		
			xchat.command("RAW SAJOIN {0} {1}".format(word[1], channel))
			derp = derp+1
	else:
		print("You didn't specify a target.")

	return xchat.EAT_ALL

xchat.hook_command("msajoin", sajoin, help="/msajoin Massive sajoin one person into over9000 channels")
print("Loaded {0}, version {1}".format(__module_name__, __module_version__))

