import serial
from time import sleep
import requests

ser = serial.Serial("/dev/serial0", 9600)
url = 'https://logansinclair.me'
SCAN_CMD = b'\x7E\x00\x08\x01\x00\x02\x01\xAB\xCD'

def read():
	recieved_data = ser.read()
	sleep(0.03)
	data_left = ser.inWaiting()
	recieved_data += ser.read(data_left)
	return recieved_data.decode("utf8")

def write(data):
	ser.write(data)
	return read()

def process(data):
	strings = data.split(":")
	if(len(strings) == 3):
		print("Batt SN: " + strings[2] + " || Full Barcode: " + data )
	else:
		print("Invalid Bacode: " + data)

while True:
	i = input()
	ser.write(SCAN_CMD)
	read()
	data = read()
	process(data)


