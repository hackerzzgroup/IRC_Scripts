#!/usr/bin/python2.7
__module_name__ = "MPD Song Info"
__module_version__ = "2.0"
__module_description__ = "MPD Xchat Plugin"
#Theres a bug in here when loading. Hope to fix soon.
import xchat
import mpd
import os
import time

host = "localhost"
port = "6600"

client = mpd.MPDClient()

def mpd_connect():
	try:
		client.connect(host,port)
		return True
	except:
		print("Failed to connect to MPD: {0}:{1}".format(host,port))  
		return False

def mpd_disconnect():
	client.close()		# send the close command
	client.disconnect()	# disconnect from the server
	return

def get_info():
	current_song = client.currentsong()
	current_status = client.status()
	song_filename = os.path.basename(current_song["file"])
	(song_shortname, song_extension) = os.path.splitext(song_filename)
	(song_pos,song_length) = current_status["time"].split(":")

	song_pos = time.strftime('%M:%S', time.gmtime(float(song_pos)))
	song_length = time.strftime('%M:%S', time.gmtime(float(song_length)))

	try:
		msg = "{0} - {1} - {2} ({3}/{4})".format(current_song["artist"], current_song["album"], current_song["title"], song_pos,song_length)
	except: #It derped, so default back to the basic string.
		msg = "{0} ({1}/{2})".format(song_shortname,song_pos,song_length)
	return msg

def mpdshow_cb(word, word_eol, userdata):
	if mpd_connect():
		xchat.command("ME playing: "+get_info())
		mpd_disconnect()
	return xchat.EAT_ALL

def mpdprev_cb(word, word_eol, userdata):
	if mpd_connect():
		client.previous()
		print("Now Playing: "+get_info())  
		mpd_disconnect() 
	return xchat.EAT_ALL

def mpdnext_cb(word, word_eol, userdata):
	if mpd_connect():
		client.next()
		print("Now Playing: "+get_info())
		mpd_disconnect() 
	return xchat.EAT_ALL

xchat.hook_command("mnext", mpdnext_cb, help="/mnext change to next song")
xchat.hook_command("mprev", mpdprev_cb, help="/mprev change to previous song")
xchat.hook_command("mshow", mpdshow_cb, help="/mshow shows song information to channel")

print("Loaded {0}, version {1}".format(__module_name__, __module_version__))
	
