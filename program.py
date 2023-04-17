import serial
from time import sleep
import requests
import pygame

#Scanner Setup
ser = serial.Serial("/dev/serial0", 9600)
SCAN_CMD = b'\x7E\x00\x08\x01\x00\x02\x01\xAB\xCD'

#Web Setup
url = 'https://logansinclair.me'

#Audio Setup
pygame.mixer.init()
sound = pygame.mixer.Sound('/home/pi/Scanner/sound.wav')


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
		sound.play()
	else:
		print("Invalid Bacode: " + data)

while True:
	i = input()
	ser.write(SCAN_CMD)
	read()
	data = read()
	process(data)


