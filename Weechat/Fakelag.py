#!/usr/bin/env python

# Fakelag.py - Auto Fakelag excempt for authenticated clients.
# Licensed under GPL3, Free Software etc etc

import weechat
import re

NAME = "Fakelag.py"
AUTHOR = "Ferus - irc.datnode.net #hacking"
VERSION = "1.0"
LICENSE = "GPL3"
DISC = "Auto Fakelag exempt script for clients who authenticate to nickserv."

# default settings
settings = {
	'server': 'DatNode'
	,'channel': '#services'
	,'command': '/quote privmsg operserv flood {0}'
	,'allowed': 'stal,WhergBot'
	}

if weechat.register(NAME, AUTHOR, VERSION, LICENSE, DISC, "", ""):
	for option, value in settings.items():
		if not weechat.config_is_set_plugin(option):
			weechat.config_set_plugin(option, value)

def GetSetting(Setting):
	return weechat.config_string(weechat.config_get('plugins.var.python.fakelag.py.'+Setting))

def Main(data, buffer, date, tags, displayed, highlight, prefix, message):
	for x in GetSetting('allowed').split(','):
		if re.match("NickServ: {0}!.*?@.*? identified for nick {0}".format(x), message):
			weechat.command(buffer, GetSetting('command').format(x))
			break
	return weechat.WEECHAT_RC_OK

hook = weechat.hook_print(
	GetSetting("server")
	,"irc_privmsg,notify_message,nick_Global,log1"
	,""
	,1
	,"Main"
	,""
	)
