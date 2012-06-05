#!/usr/bin/python2.7
__module_name__ = "mocp-xchat.py"
__module_version__ = "1.0"
__module_description__ = "Now Playing Script for MoC"
__module_author__ = "Ferus"

import xchat
from commands import getoutput
import subprocess
song_info = []
info_dict = {}
'''This dictionary will contain all mocp info.
	Listed below are all the possible keys.

Bitrate
CurrentSec
AvgBitrate
File
TotalTime
CurrentTime
Album
SongTitle
TimeLeft
TotalSec
State
Title
Rate
Artist
'''

def is_running(output):
	if output: 
		return True
	else: 
		return False
def is_stream(info):
	if "http" in info:
		return True
	else: 
		return False
		
def get_info():
	output = getoutput("ps -C mocp").split('\n')[1:]
	if is_running(output):
		song_info = getoutput("mocp --info").split("\n")
		for info in song_info:
			info = info.split(" ")
			info_dict[info[0].strip(":")] = " ".join(info[1:])
		if is_stream(info_dict["File"]):
			string = "{0} ({1})".format(info_dict["Title"], info_dict["File"])
		else:
			string = "{0} - {1} ({2}) {3} [{4}]".format(info_dict["SongTitle"], info_dict["Artist"], info_dict["Album"], info_dict["CurrentTime"], info_dict["TotalTime"])	
		return string
	else: 
		return None

def parse(word, word_eol, userdata):
	try:
		trigger = word[1]
	except:
		trigger = ''
	if trigger == "show":
		xchat.command("ME listening to {0}".format(get_info()))
	elif trigger == "next":
		subprocess.call("mocp -f", shell=True)
		print("Now playing: {0}".format(get_info()))
	elif trigger == "prev":
		subprocess.call("mocp -r", shell=True)
		print("Now playing: {0}".format(get_info()))
	elif trigger == "pause":
		subprocess.call("mocp -G", shell=True)
		print("Triggered pause")
	elif trigger == "stop":
		subprocess.call("mocp -s", shell=True)
		print("Stopping: {0}".format(get_info()))
	elif trigger == "play":
		subprocess.call("mocp -p", shell=True)
		print("Now playing: {0}".format(get_info()))
	elif trigger == "quit" or trigger == "kill":
		subprocess.call("mocp -x", shell=True)
		print("Killing MoC")
	elif trigger == "vol":
		if word[2].isdigit():
			subprocess.call("mocp -v {0}".format(word[2]), shell=True)
		else:
			print("You must specify a volume level, 0-100.")
	elif trigger == "help":
		help()
	else:
		print("You need to pass an argument to this command")
	return xchat.EAT_ALL

def help():
	print('''mocp-xchat.py by Ferus. irc.datnode.net #hacking
			/moc show			Tells the channel what you are listening to in the form of a /me
			/moc next			Plays the next song, and prints it out.
			/moc prev			Plays the prev song, and prints it out.
			/moc pause			Pauses MoC.
			/moc stop			Stops MoC.
			/moc play			Starts MoC.
			/moc quit			Kills MoC.
			/moc kill			Kills MoC.
			/moc vol			Takes a number from 0-100 and sets MoC's volume to that percent.''')




xchat.hook_command("moc", parse, help="/moc takes options to control MoC. /moc help to list commands.")
print("Loaded {0}, version {1}".format(__module_name__, __module_version__))
