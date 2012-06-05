#!/usr/bin/python2.7
__module_name__ = "mslap.py"
__module_version__ = "1.2"
__module_description__ = "Mass Slap Plugin"
__module_author__ = "Ferus"


import xchat

def slapall(word, word_eol, userdata):
	names = []
	list = xchat.get_list('users')
	if list:
		for i in list:
			names.append(i.nick)
		for i in list:
			for name in names:
				xchat.command("ME slaps {0} around a bit with a {1}".format(i.nick, name))
	return xchat.EAT_ALL

def slapone(word, word_eol, userdata):
	list = xchat.get_list('users')
	if list:
		if word[1]:
			for i in list:
				xchat.command("ME slaps {0} around a bit with a {1}".format(word[1], i.nick))
		else:
			print("Didnt specify a name to slap")
	return xchat.EAT_ALL
def slap(word, word_eol, userdata):
	try:
		xchat.command("ME slaps {0} around a bit with a {1}".format(word[1], ' '.join(word[2:])))
		xchat.command("SAPART {0} {1} {2}".format(word[1], xchat.get_info("channel"), "Slapped!"))
		xchat.command("SAJOIN {0} {1}".format(word[1], xchat.get_info("channel")))
	except:
		print("Syntax is /slap person fish")
	return xchat.EAT_ALL
	
xchat.hook_command("slap", slap, help="Sajoin/part slap a person\nPerson, Fish")	
xchat.hook_command("slapall", slapall, help="Slap everyone, with everyone.")
xchat.hook_command("slapone", slapone, help="Slap one person with everyone.")
print("Loaded {0}, version {1}".format(__module_name__, __module_version__))
	
