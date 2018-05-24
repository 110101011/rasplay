#!/usr/bin/python

"""rasplay.py: Python script that display's system information on to a 
HD44870 charlcd from a Raspberry Pi either via GPIO or I2C"""

#imports
import time
import datetime
import os.path
import logging, sys
import socket
import subprocess

import config

__author__ = 'Justin Verel'
__copyright__ = '...'
__license__ = '...'
__date__ = '23-04-2018'
__version__ = '0.1.0'
__maintainer__ = 'Justin Verel'
__email__ = 'justin@marverinc.nl'
__status__ = 'Development'

lcd = None
first_run = True

SOCKPATH = "/var/run/lirc/lircd"

sock = None

prev_key = "KEY_0"

graden = (
	0b00000,
	0b00100,
	0b01010,
	0b00100,
	0b00000,
	0b00000,
	0b00000,
	0b00000,
)

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def main():
	#main function
	setup_display()
	init_irw()

	global prev_key

	lcd.write_string('Raspberry Pi')
	lcd.cursor_pos = (2, 0)
	lcd.write_string('Rasplay Booting up')

#	lcd.backlight_enabled = 0.9
	
	live = True

#	time.sleep(5)
	
	#Create While loop
	while live == True:
		now_key = next_key()
		if not now_key:
			logging.debug("next_key() is Empty")
			get_command(prev_key)
		else:
			logging.debug("next_key() is %s", next_key())
			prev_key == now_key
			get_command(now_key)

	#Close connection to lcd and clear
	lcd.close(clear=True)

def setup_display():
	global lcd	

	#Setup display in GPIO or I2C mode
	if config.lcd_mode == 'I2C':
		logging.debug('I2C')
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
		#Error no lcd mode has been set!
		logging.debug('LCD Mode has not been set!')

def init_irw():
	global sock
	sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	print ('starting up on %s' % SOCKPATH)
	sock.connect(SOCKPATH)

def next_key():
	while True:
		data = sock.recv(128)
		data.strip()
		if data:
			break
	words = data.split()
	return str(words[2])

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def getTemp():
    """Get Temperature""" 
    cpu = subprocess.Popen("cat /sys/class/thermal/thermal_zone0/temp", shell=True, stdout=subprocess.PIPE).stdout.read()
    cpu = float(cpu) / 1000
    cpu = round(cpu, 1)
    gpu = subprocess.Popen("vcgencmd measure_temp", shell=True, stdout=subprocess.PIPE).stdout.read()
    gpu = gpu.replace("temp=", "")
    gpu = gpu.replace("'C", "\x00C")
    return cpu, gpu

def get_cpu_speed():
    cpu_speed = subprocess.Popen("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq", shell=True, stdout=subprocess.PIPE).stdout.read()
    cpu_speed = int(cpu_speed) / 1000
    return cpu_speed

def show_info():
	#Show information on display
	global first_run
	#get_command()
	#first_time = True
	if first_run == True:
		lcd.clear()
		first_run = False
		logging.debug(first_run)

#	lcd.backlight_enabled = 0.1
	
#	date = datetime.datetime.now().strftime("%d-%m-%y")
#	time = datetime.datetime.now().strftime("%H:%M:%S")

	ip_address = get_ip()

	cpu, gpu = getTemp()

	lcd.create_char(0, graden)

#	lcd.cursor_pos = (0, 0)
#	lcd.write_string(date)
#	lcd.cursor_pos = (0,12)
#	lcd.write_string(time)
	lcd.cursor_pos = (1, 0)
	lcd.write_string("IP:  " + ip_address)
	lcd.cursor_pos = (2, 0)
	lcd.write_string("CPU: " + str(get_cpu_speed()) + "Mhz")
	lcd.cursor_pos = (2, 14)
	lcd.write_string(str(cpu) + "\x00C")
	lcd.cursor_pos = (3, 0)
	lcd.write_string("GPU:")
	lcd.cursor_pos = (3, 14)
	lcd.write_string(str(gpu))

def show_date():
	#Show Date and Time
	global first_run

	if first_run == True:
		lcd.clear()
		first_run = False

	date = datetime.datetime.now().strftime("%d-%m-%y")
	time = datetime.datetime.now().strftime("%H:%M:%S")

	lcd.cursor_pos = (0, 0)
	lcd.write_string(date)
	lcd.cursor_pos = (0, 12)
	lcd.write_string(time)

def show_cpu():
	#Show CPU and GPU information
	get_command()

def show_network():
	#Show Network information
	get_command()

def get_command(key):
	#Get Command from remote
	global first_run
	if key == "KEY_0":
		first_run = True
		show_info()
	elif key == "KEY_1":
		first_run = True
		show_date()
	else:
		first_run = True
		show_info()

if __name__ == "__main__":
	main()
