#!/usr/bin/python2.7
__module_name__ = "Multikick.py"
__module_version__ = "1.0"
__module_description__ = "Kick Plugin"
__module_author__ = "Ferus"

# word[0] == trigger
# word[1] == list of names
# word[2:] == reason

import xchat

def kick(word, word_eol, userdata):
	for nick in word[1].split(","):
		try:
			xchat.command("KICK {0} {1}".format(nick, ' '.join(word[2:])))
		except:
			print("You are not an op in this channel.")
	return xchat.EAT_ALL
	
xchat.hook_command("multikick", kick, help="Kick multiple users, separate names with a comma.")
print("Loaded {0}, version {1}".format(__module_name__, __module_version__))
	
