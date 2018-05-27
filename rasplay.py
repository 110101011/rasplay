#!/usr/bin/python3.5

"""rasplay.py: Python script that display's system information on to a 
HD44870 charlcd from a Raspberry Pi either via GPIO or I2C"""

#imports
import time
import datetime
import os.path
import logging, sys
import socket
import subprocess
import threading

import config

__author__ = 'Justin Verel'
__copyright__ = '...'
__license__ = '...'
__date__ = '23-04-2018'
__version__ = '0.2.5'
__maintainer__ = 'Justin Verel'
__email__ = 'justin@marverinc.nl'
__status__ = 'Development'

lcd = None
lcddata = []
first_run = True

SOCKPATH = "/var/run/lirc/lircd"

sock = None
live = True

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
	global now_key

	logging.debug("Starting up display")
	setup_display()
	logging.debug("Starting up irw socket")
	init_irw()

	now_key = "KEY_1"
	key = "KEY_1"

	thread = NextKey(next_key)
	thread.start()

	lcd.write_string('Raspberry Pi')
	lcd.cursor_pos = (2, 0)
	lcd.write_string('Rasplay Booting up')
	
	time.sleep(2)	
	lcd.clear()

	#Create While loop
	logging.debug("Starting while loop")
	while live == True:
		#logging.debug("now_key = %s", now_key)

		if key != now_key:
			lcd.clear()

		key = now_key
		if now_key == 'KEY_1':
			logging.debug("show_date() - " + now_key)
			key = now_key
			show_date()
			time.sleep(1)
			for rows in range(len(lcddata)):
				lcd.cursor_pos = (lcddata[rows][0], lcddata[rows][1])
				lcd.write_string(lcddata[rows][2])
		elif now_key == "KEY_2":
			logging.debug("show_cpu()- " + now_key)
			key = now_key
			show_cpu()
			time.sleep(1)
			for rows in range(len(lcddata)):
				lcd.cursor_pos = (lcddata[rows][0], lcddata[rows][1])
				lcd.write_string(lcddata[rows][2])
		elif now_key == "KEY_3":
			logging.debug("show_network() - " + now_key)
			show_network()
			time.sleep(1)
			for rows in range(len(lcddata)):
				lcd.cursor_pos = (lcddata[rows][0], lcddata[rows][1])
				lcd.write_string(lcddata[rows][2])
		else:
			print("Fucked")
			time.sleep(1)

	#Close connection to lcd and clear
	lcd.close(clear=True)

def setup_display():
	global lcd

	#Setup display in GPIO or I2C mode
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
		#Error no lcd mode has been set!
		logging.debug('LCD Mode has not been set!')

def init_irw():
	global sock
	sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	logging.debug('starting up on %s' % SOCKPATH)
	sock.connect(SOCKPATH)

class NextKey(threading.Thread):

	def __init__(self, function_next_key):
		threading.Thread.__init__(self)
		self.runnable = function_next_key
		self.deamon = True

	def run(self):
		self.runnable()

def next_key():
	global now_key
	while live == True:
		while True:
			data = sock.recv(128)
			data.strip()
			if data:
				break
		words = data.split()
		key = str(words[2])
		key = key.split("b'")[1]
		key = key.split("'")[0]
		now_key = key

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
	gpu = gpu.decode('utf-8')
	gpu = gpu.replace("temp=", "")
	gpu = gpu.replace("'C", "\x00C")

	return cpu, gpu

def get_cpu_speed():
    cpu_speed = subprocess.Popen("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq", shell=True, stdout=subprocess.PIPE).stdout.read()
    cpu_speed = int(cpu_speed) / 1000
    return cpu_speed

def show_date():
	#Show Date and Time
	global lcddata

	day = datetime.datetime.now().strftime("%A")

	date = datetime.datetime.now().strftime("%d-%m-%y")
	time = datetime.datetime.now().strftime("%H:%M:%S")

	lcddata = [0, 0, day], [0, 12, time], [1, 0, date]

	return lcddata

def show_cpu():
	#Show CPU and GPU information
	global lcddata

	cpu, gpu = getTemp()

	lcd.create_char(0, graden)

	cpu_string = "CPU: "
	cpu_speed_string = str(get_cpu_speed()) + " Mhz"
	cpu_temp_string = str(cpu) + "\x00C"
	gpu_string = "GPU:"
	gpu_temp_string = str(gpu)

	lcddata = [0, 0, cpu_string], [0, 11, cpu_speed_string], [1, 14, cpu_temp_string], [2, 0, gpu_string], [3, 14, gpu_temp_string]

	return lcddata

def show_network():
	#Show Network information
	global lcddata

	ip_address = get_ip()

	ip_string = "ip address:"

	lcddata = [0, 0, ip_string], [1, 0, ip_address]

	return lcddata

#def get_command(key):
#	#Get Command from remote
#	logging.debug("Key: %s", key)
#	global first_run
#	if key == "KEY_0":
#		first_run = True
#		show_info()
#	elif key == "KEY_1":
#		first_run = True
#		show_date()
#	else:
#		first_run = True
#		show_info()

if __name__ == "__main__":
	main()
