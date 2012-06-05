#!/usr/bin/python2.7
__module_name__	= "payback.py"
__module_version__	= "1.0"
__module_description__	= "Payback Plugin"
__module_author__	= "Ferus"

import xchat

def banned(word, word_eol, userdata):
	'''Looks like we've been banned from a channel, lets get payback!'''
	#I was going to add kicking.. Its not really 'pacback' yet..
	if xchat.get_info("server") == "opsimathia.datnode.net":
		print("* \x02[Banned]\x02 Attempting to takeover channel {0}.".format(word[0]))
		xchat.command("SAJOIN {0} {1}".format(xchat.get_info("nick"), word[0]))
		xchat.command("SAMODE {0} +q {1}".format(word[0], xchat.get_info("nick")))
	else:
		print("* \x02[Banned]\x02 from channel {0}.".format(word[0]))
xchat.hook_print('Banned', banned)
print ("Loaded "+ __module_author__ +"'s "+ __module_description__)


