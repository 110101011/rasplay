#!/usr/bin/python

# Display Mode (I2C or GPIO)
lcd_mode = I2C

# I2C
expander = None
address = None
port = None

# GPIO
pin_rs = None
pin_rw = None
pin_e = None
pins_data = None
numbering_mode = None

# Shared
cols = None
rows = None
dotsize = None
charmap = None
auto_linebreaks = None
