#!/usr/bin/python2
__module_name__ = "chanjoin.py"
__module_version__ = "1.0"
__module_description__ = "Sajoin Script"
__module_info__ = "Sajoin one channel to another."

import xchat

def sajoin(word, word_eol, userdata):
	if word[1] and word[2]:
		try:
			context = xchat.find_context(server=xchat.get_info('server'), channel=word[1])
			list_one = context.get_list('users')
			for obj in list_one:
				context.command("raw sajoin {0} {1}".format(obj.nick, word[2]))
		except:
			pass
	else:
		print("You didn't specify the channels.")

	return xchat.EAT_ALL

xchat.hook_command("chanjoin", sajoin, help="/chanjoin Massive sajoin one channel into another channel")
print("Loaded {0}, version {1}".format(__module_name__, __module_version__))

