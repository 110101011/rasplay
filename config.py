#!/usr/bin/python

# Display Mode (I2C or GPIO)
lcd_mode = "I2C"

# I2C
expander = "PCF8574"
address = 0x27
port = 1
backlight_enabled = "True"

# GPIO
pin_rs = None
pin_rw = None
pin_e = None
pins_data = None
numbering_mode = None

# Shared
cols = 20
rows = 4
dotsize = 8
charmap = "A02"
auto_linebreaks = True
