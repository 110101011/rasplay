#!/bin/bash

con_mode()
{
	sed -i "s/lcd_mode.*/lcd_mode = I2C/" config.py
}

CHOISE=$(whiptail --title "Rasplay Configutation Menu" \
	--menu "Choose an option" \
	20 75 4 \
	"1)" "Choose an connection mode" \
	"2)" "Change I2C Mode options" \
	"3)" "Change GPIO Mode options" \
	"4)" "Change Display options")

case $CHOISE in
	"1)")
		whiptail --title "Connection mode" \
			--radiolist "Choose an connection mode" \
			20 75 2
			"I2C" "Choose connection throught I2C" OFF \
			"GPIO" "Choose connection throught GPIO" OFF
	;;
	"2")
		echo "2"
	;;
	"3")
		echo "3"
	;;
	"4")
		echo "4"
	;;
esac
