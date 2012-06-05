#!/usr/bin/env python

# WeeMPD_NP.py - Weechat MPD "Now Playing" script
# Licensed under GPL3, Free Software etc etc
# Requires python-mpd

import weechat
import re
from time import strftime, gmtime
try:
	import mpd
except ImportError:
	weechat.prnt(weechat.current_buffer(), "MPD=>\tmpd module not found, Error importing.")

NAME = "WeeMPD_NP.py"
AUTHOR = "Ferus - irc.datnode.net #hacking"
VERSION = "1.0"
LICENSE = "GPL3"
DISC = "Weechat MPD Now Playing Script"

# default settings
settings = {'mpd.look.prefix_show': 'MPD=>'
	,'mpd.look.message': "is playing: '%title%' by '%artist%' from the album '%album%'"
	,'mpd.look.action': 'me'
	,'mpd.look.default_flag': '-say'
	,'mpd.look.notag': '[No Tag Found]'
	,'mpd.server.host': 'localhost'
	,'mpd.server.port': '6601'
	}

if weechat.register(NAME, AUTHOR, VERSION, LICENSE, DISC, "", ""):
	for option, value in settings.items():
		if not weechat.config_is_set_plugin(option):
			weechat.config_set_plugin(option, value)

VARIABLES = {
	# Status
	'%songid%': 'songid'
	,'%playlistlength%': 'playlistlength'
	,'%playlist%': 'playlist'
	,'%repeat%': 'repeat'
	,'%consume%': 'consume'
	,'%mixrampdb%': 'mixrampdb'
	,'%random%': 'random'
	,'%state%': 'state'
	,'%xfade%': 'xfade'
	,'%volume%': 'volume'
	,'%single%': 'single'
	,'%mixrampdelay%': 'mixrampdelay'
	,'%nextsong%': 'nextsong'
	,'%time%': 'time'
	,'%song%': 'song'
	,'%elapsed%': 'elapsed'
	,'%bitrate%': 'bitrate'
	,'%nextsongid%': 'nextsongid'
	,'%audio%': 'audio'
	# Currentsong
	,'%album%': 'album'
	,'%artist%': 'artist'
	,'%track%': 'track'
	,'%title%': 'title'
	,'%pos%': 'pos'
	,'%last-modified%': 'last-modified'
	,'%disc%': 'disc'
	,'%file%': 'file'
	,'%date%': 'date'
	,'%genre%': 'genre'
	,'%id%': 'id'
	}

class Client(object):
	def __init__(self):
		self.Client = mpd.MPDClient()
		self.Info = {}
		self.Flags = {
			'-say': [self.SendNowPlaying, "Say the current playing song."]
			,'-show': [self.PrintNowPlaying, "Show the current playing song."]
			,'-stop': [self.CallStop, "Stop MPD."]
			,'-play': [self.CallPlay, "Start MPD."]
			,'-help': [self.Help, "Show this help."]
			,'-next': [self.CallNext, "Plays next song in queue."]
			,'-pause': [self.CallPause, "Pauses MPD."]
			,'-prev': [self.CallPrevious, "Plays the previous song in queue."]
			,'-random': [self.TriggerRandom, "Triggers random on and off."]
			,'-repeat': [self.TriggerRepeat, "Triggers repeat on and off."]
			,'-single': [self.TriggerSingle, "Triggers single on and off."]
			}
		
		if self._mpd_connect():
			status = self.Client.status()
			self.Random = status['random']
			self.Repeat = status['repeat']
			self.Single = status['single']
			self._mpd_disconnect()

	def _mpd_connect(self):
		try:
			self.Client.connect(self.GetSetting('mpd.server.host'), int(self.GetSetting('mpd.server.port')))
			return True
		except mpd.ConnectionError:
			return False
		except Exception, e:
			self.PrintMessage("Failed to connect to MPD Server; {0}".format(repr(e)))
			return False

	def _mpd_disconnect(self):
		self.Client.close()
		self.Client.disconnect()
		return None

	def _get_info(self):
		self.Info = {}
		try:
			for k, v in self.Client.currentsong().items():
				self.Info[k] = v
			for k, v in self.Client.status().items():
				self.Info[k] = v
			return True
		except:
			return False

	def _format_string(self):
		if not self.Info or not self._get_info():
			self.PrintMessage("No Info")
			return None
		x = self.GetSetting('mpd.look.message')
		for k, v in VARIABLES.items():
			try:
				if re.search(k, x):
					x = re.sub(k, self.Info[v], x)
			except KeyError:
				x = re.sub(k, self.GetSetting("mpd.look.notag"), x)
		self.Info = {}
		return x

	def GetSetting(self, Setting):
		return weechat.config_string(weechat.config_get('plugins.var.python.weempd_np.py.'+Setting))

	def PrintMessage(self, Message):
		weechat.prnt(weechat.current_buffer(), '{0}\t{1}'.format(self.GetSetting('mpd.look.prefix_show'), Message))

	def SendNowPlaying(self):
		if not self._mpd_connect():
			return None
		self._get_info()
		x = self._format_string()
		self._mpd_disconnect()
		if not x:
			self.PrintMessage("Error: Nothing to send.") #Debug.
			return None
		weechat.command(weechat.current_buffer(), '/{0} {1}'.format(self.GetSetting('mpd.look.action'), x))

	def PrintNowPlaying(self):
		if not self._mpd_connect():
			return None
		self._get_info()
		x = self._format_string()
		self._mpd_disconnect()
		if not x:
			self.PrintMessage("Error: Nothing to send.")
			return None
		self.PrintMessage(x)

	def CallStop(self):
		if not self._mpd_connect():
			return None
		self.Client.stop()
		self._mpd_disconnect()

	def CallPlay(self):
		if not self._mpd_connect():
			return None
		self.Client.play()
		self._mpd_disconnect()

	def CallNext(self):
		if not self._mpd_connect():
			return None
		self.Client.next()
		self._mpd_disconnect()

	def CallPause(self):
		if not self._mpd_connect():
			return None
		self.Client.pause()
		self._mpd_disconnect()

	def CallPrevious(self):
		if not self._mpd_connect():
			return None
		self.Client.previous()
		self._mpd_disconnect()

	def TriggerRandom(self):
		if not self._mpd_connect():
			return None
		if self.Random == '0':
			self.Client.random(1)
			self.Random = '1'
			self.PrintMessage("Random now set to on.")
		else:
			self.Client.random(0)
			self.Random = '0'
			self.PrintMessage("Random now set to off.")
		self._mpd_disconnect()
	
	def TriggerRepeat(self):
		if not self._mpd_connect():
			return None
		if self.Repeat == '0':
			self.Client.repeat(1)
			self.Repeat = '1'
			self.PrintMessage("Repeat now set to on.")
		else:
			self.Client.repeat(0)
			self.Repeat = '0'
			self.PrintMessage("Repeat now set to off.")
		self._mpd_disconnect()
	
	def TriggerSingle(self):
		if not self._mpd_connect():
			return None
		if self.Single == '0':
			self.Client.single(1)
			self.Single = '1'
			self.PrintMessage("Single now set to on.")
		else:
			self.Client.single(0)
			self.Single = '0'
			self.PrintMessage("Single now set to off.")
		self._mpd_disconnect()

	def Help(self):
		for flag in self.Flags.keys():
			self.PrintMessage("{0} {1}".format(flag, self.Flags[flag][1]))

	def Parse(self, args):
		if not args:
			#execute default
			self.Flags[self.GetSetting('mpd.look.default_flag')][0]()
			return weechat.WEECHAT_RC_OK

		for arg in args:
			if arg in self.Flags.keys():
				self.Flags[arg][0]()
		return weechat.WEECHAT_RC_OK

MPD = Client()
def Main(data, buffer, args):
	return MPD.Parse(args.split())

hook = weechat.hook_command(
	"mpd"
	,"MPD NP Script, for help see /mpd -help"
	,""
	,"If no flags are specified, we default to 'mpd.look.default_flag'\n"
	"To set output format use `/set plugins.var.python.weempd_np.py.mpd.look.message'\n"
	"{0}".format("\n".join(VARIABLES))

	,""
	,"Main"
	,"")
