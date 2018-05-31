#!/usr/bin/python

from mpd import MPDClient

client = None

def init():
	global client
	client = MPDClient()
	client.idletimeout = 10
	client.connect("localhost", 6600)
	print("client connected")

# Play/Pauze
def mpd_play_pauze():
	client.pause()

# Next song
def mpd_next_song():
	client.next()

# Previous song
def mpd_previous_song():
	client.previous()

def mpd_elapsed_time():
	elapsed = client.status()['time']

	return elapsed
""" Needs mpd 0.20 """
#def mpd_duration_time():
#	duration = client.status()['duration']

#	return duration

# Show volume
def mpd_volume_show():
	level = client.status()['volume']
#	level_string = str(level)
	
	return level

# Volume up
def mpd_volume_up():
	if client.status()['volume'] < 100:
		level = int(client.status()['volume']) + 10
		level = max(min(level, 100), 0)
		client.setvol(level)

# Volume Down
def mpd_volume_down():
	if client.status()['volume'] > 0:
		level = int(client.status()['volume']) - 10
		level = max(min(level, 100), 0)
		client.setvol(level)

# Show playlists

# Next playlist

# Previous playlist
