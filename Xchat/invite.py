#!/usr/bin/python2
__module_name__	= "invite.py"
__module_version__	= "1.0"
__module_description__	= "Invite Plugin"
__module_author__	= "Ferus"

import xchat

def invited(word, word_eol, userdata):
	'''Looks like we've been invited to a channel, lets join it!'''
	print("* \x02[Invite]\x02 Invited to {0}, Now joining.".format(word[0]))
	xchat.command("JOIN {0}".format(word[0]))
		


xchat.hook_print('Invited', invited)
print ("Loaded "+ __module_author__ +"'s "+ __module_description__)


