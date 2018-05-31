#!/usr/bin/python3.5

"""rasplay.py: Python script that display's system information on to a 
HD44870 charlcd from a Raspberry Pi either via GPIO or I2C"""

# imports
import time
import datetime
import os.path
import logging, sys
import threading

# Local imports
import config
import custom_characters
import functions
import irw
import mpd_functions

__author__ = 'Justin Verel'
__copyright__ = '...'
__license__ = '...'
__date__ = '23-04-2018'
__last_modified__ = '31-05-2018'
__version__ = '0.3.3'
__maintainer__ = 'Justin Verel'
__email__ = 'justin@marverinc.nl'
__status__ = 'Development'

lcddata = []
live = True
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
key = "KEY_1"

def main():
	global key

	# main function
	logging.debug("Starting up display")
	setup_display()
	irw.init()
	mpd_functions.init()

#	key = "KEY_1"

	thread = irw.NextKey(irw.next_key)
	thread.start()

	lcd.write_string('Raspberry Pi')
	lcd.cursor_pos = (2, 0)
	lcd.write_string('Rasplay Booting up')
	
	time.sleep(2)	
	lcd.clear()

	#Create While loop
	while live == True:
		if key != irw.now_key:
			lcd.clear()

		key = irw.now_key
		if irw.now_key == 'KEY_1':
			key = irw.now_key
			show_date()
			time.sleep(1)
			for rows in range(len(lcddata)):
				lcd.cursor_pos = (lcddata[rows][0], lcddata[rows][1])
				lcd.write_string(lcddata[rows][2])
		elif irw.now_key == "KEY_2":
			key = irw.now_key
			show_cpu()
			time.sleep(1)
			for rows in range(len(lcddata)):
				lcd.cursor_pos = (lcddata[rows][0], lcddata[rows][1])
				lcd.write_string(lcddata[rows][2])
		elif irw.now_key == "KEY_3":
			key = irw.now_key
			show_network()
			time.sleep(1)
			for rows in range(len(lcddata)):
				lcd.cursor_pos = (lcddata[rows][0], lcddata[rows][1])
				lcd.write_string(lcddata[rows][2])
		elif irw.now_key == "KEY_4":
			key = irw.now_key
			show_disk()
			time.sleep(1)
			for rows in range(len(lcddata)):
				lcd.cursor_pos = (lcddata[rows][0], lcddata[rows][1])
				lcd.write_string(lcddata[rows][2])
		elif irw.now_key == "KEY_6" or irw.now_key == "KEY_PLAYPAUSE":
			key = irw.now_key
			show_mpd()
			time.sleep(1)
			for rows in range(len(lcddata)):
				lcd.cursor_pos = (lcddata[rows][0], lcddata[rows][1])
#				print(lcddata[rows][2])
				lcd.write_string(lcddata[rows][2])
		else:
			print("Not assigned at the moment!")
			time.sleep(1)

	# Close connection to lcd and clear
	lcd.close(clear=True)

def setup_display():
	global lcd

	# Setup display in GPIO or I2C mode
	if config.lcd_mode == 'I2C':
		from RPLCD.i2c import CharLCD
		lcd = CharLCD("PCF8574", address=config.address, port=config.port,
				cols=config.cols, rows=config.rows, dotsize=config.dotsize,
				charmap=config.charmap, auto_linebreaks=config.auto_linebreaks,
				backlight_enabled=config.backlight_enabled)
	elif config.lcd_mode == 'GPIO':
		from RPLCD.gpio import CharLCD
		from RPi import GPIO
		lcd = CharLCD(pin_rs=config.pin_rs, pin_rw=config.pin_rw, pin_e=config.pin_e,
				pins_data=config.pins_data,
				numbering_mode=config.numbering_mode,
				cols=config.cols, rows=config.rows, dotsize=config.dotsize,
				charmap=config.charmap, auto_linebreaks=config.auto_linebreaks)
	else:
		# Error no lcd mode has been set!
		logging.debug('LCD Mode has not been set!')

def show_date():
	# (1) Show Date and Time
	global lcddata

	day = datetime.datetime.now().strftime("%A")

	date = datetime.datetime.now().strftime("%d-%m-%y")
	time = datetime.datetime.now().strftime("%H:%M:%S")

	lcddata = [0, 0, day], [0, 12, time], [1, 0, date]

	return lcddata

def show_cpu():
	# (2) Show CPU and GPU information
	global lcddata

	cpu, gpu = functions.getTemp()

	lcd.create_char(0, custom_characters.graden)

	cpu_string = "CPU: "
	cpu_speed_string = str(functions.get_cpu_speed()) + " Mhz"
	cpu_temp_string = str(cpu) + "\x00C"
	gpu_string = "GPU:"
	gpu_temp_string = str(gpu)

	lcddata = [0, 0, cpu_string], [0, 10, cpu_speed_string], [1, 13, cpu_temp_string], [2, 0, gpu_string], [3, 13, gpu_temp_string]

	return lcddata

def show_network():
	# (3) Show Network information
	global lcddata

	ip_address = functions.get_ip()

	ip_string = "ip address:"

	lcddata = [0, 0, ip_string], [1, 0, ip_address]

	return lcddata

def show_disk():
	# (4) Show Disk information
	global lcddata

	print("Disk information")

	lcddata = []

def show_mpd():
	# (6) Show MPD information
	global lcddata
	global key

	print("MPD Information")

	mpd = "running"

	if mpd == "running":
		if mpd_functions.client.status()['state'] == "play":
			# Show Artist / Song / Time played / Total time / Volume

			level = mpd_functions.mpd_volume_show()
			elapsed = mpd_functions.mpd_elapsed_time()

			artist = mpd_functions.client.currentsong()['artist']
			title = mpd_functions.client.currentsong()['title']
			title = (title[:17] + '..') if len(title) > 17 else title

			lcddata = [0, 0, "MPD Client"], [1, 0, artist], [2, 0, title], [3, 0, elapsed], [3, 16, level]
			if irw.now_key == "KEY_PLAYPAUSE":
				mpd_functions.mpd_play_pause()
				key = "KEY_6"
	return lcddata

"""			if key == KEY_PLAYPAUZE:
				Play / Pauze song and set key to KEY_6
			if key == KEY_NEXT:
				Play next song and set key to KEY_6
			if key == KEY_PREV:
				Play previous song and set key to KEY_6
			if key == KEY_VOLUMEUP:
				Turn volume up and set key to KEY_6
			if key == KEY_VOLUMEDOWN:
				Turn volume down an set key to KEY_6
		if mpd == stopped:
			Show playlists (Scroll with Prev / Next and select with PlayPauze)
			if key == KEY_PLAY:
				Play selected playlist and set key to KEY_6
			if key == KEY_NEXT:
				Select next playlist and set key to KEY_6
			if key == KEY_PREV:
				Select previous playlist and set key to KEY_6
"""

#	return lcddata

if __name__ == "__main__":
	main()
