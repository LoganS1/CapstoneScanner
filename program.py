import serial
from time import sleep
import requests
import pygame
import RPi.GPIO as GPIO
import signal
from enum import Enum

#Scanner Setup
ser = serial.Serial("/dev/serial0", 9600)
SCAN_CMD = b'\x7E\x00\x08\x01\x00\x02\x01\xAB\xCD'

#Web Setup
url = 'https://logansinclair.me'

#Audio Setup
pygame.mixer.init()
sound = pygame.mixer.Sound('/home/pi/Scanner/sound.wav')

#LED Setup
GREEN_LED =  16
YELLOW_LED = 18
RED_LED = 22

GPIO.setmode(GPIO.BOARD)
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(YELLOW_LED, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)

#Status Setup
Class Status(Enum):
	READY = 1
	WAITING = 2
	ERROR = 3

def read():
	setStatus(Status.WAITING)
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
		GPIO.output(led, GPIO.HIGH)
		sleep(1)
		GPIO.output(led, GPIO.LOW)
	else:
		print("Invalid Bacode: " + data)
		setStatus(Status.ERROR)
def setStatus(status):
	if(status==Status.READY):
	else if(status==Status.WAITING):
	else if(status==Status.ERROR):

def signal_handler(sig, frame):
	print("Exiting...")
	GPIO.cleanup()
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

while True:
	i = input()
	ser.write(SCAN_CMD)
	read()
	data = read()
	process(data)

