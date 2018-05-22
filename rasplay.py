#!/usr/bin/python

"""rasplay.py: Python script that display's system information on to a 
HD44870 charlcd from a Raspberry Pi either via GPIO or I2C"""

#imports
import time
import os.path
import logging, sys

import config

__author__ = 'Justin Verel'
__copyright__ = '...'
__license__ = '...'
__date__ = '23-04-2018'
__version__ = '0.1.0'
__maintainer__ = 'Justin Verel'
__email__ = 'justin@marverinc.nl'
__status__ = 'Development'

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def main():
	#main function
	setup_display()

	lcd.write_string('Raspberry Pi')
	lcd.cursor_pos = (1, 0)
	lcd.write_string('HD44870 Booted up')

	live = True

	sleep(5)
	
	#Create While loop
	while live == True:
		show_info()

	#Close connection to lcd and clear
	lcd.close(clear=True)

def setup_display():
	#Setup display in GPIO or I2C mode
	if config.lcd_mode == 'I2C':
		from RPLCD.i2c import CharLCD
		lcd = CharLCD(expander=config.expander, address=config.address, port=config.port,
				cols=config.cols, rows=config.rows, dotsize=config.dotsize,
				charmap=config.charmap, auto_linebreaks=config.autolinebreaks,
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
		#Error no lcd mode has been set!
		logging.debug('LCD Mode has not been set!')

def show_info():
	#Show information on display
	get_command()

def show_date():
	#Show Date and Time
	get_command()

def show_cpu():
	#Show CPU and GPU information
	get_command()

def show_network():
	#Show Network information
	get_command()

def get_command():
	#Get Command from remote
	get_command()

if __name__ == "__main__":
	main()
