#!/usr/bin/python

import subprocess
import socket

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

