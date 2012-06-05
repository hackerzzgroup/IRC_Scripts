__module_name__ = 'care.py'
__module_version__ = '1.0'
__module_description__ = 'Sajoin to #care Plugin'
__module_author__ = 'Ferus'

import xchat
def isChan():
	net = (xchat.get_context()).get_info('network')
	if net == 'DatNode':
		return True
	else:
		return False

def lols(word, word_eol, userdata):
	if isChan():
		try:
			msg = word[1].replace(",","").split()
			if msg[1] == '#care':
			#	users = xchat.get_list('users')
				person = msg[0]
			#	for i in users:
			#		if person == i.nick:
				xchat.command("RAW SAJOIN {0} #care".format(person))
		except:
			pass
	return None

xchat.hook_print("Your Message", lols)
print("Loaded {0}, version {1}".format(__module_name__, __module_version__))
