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

#Button Setup
BUTTON = 37
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Status Setup
class Status(Enum):
	READY = 1
	WAITING = 2
	ERROR = 3

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
		setStatus(Status.READY)
		print("Batt SN: " + strings[2] + " || Full Barcode: " + data )
		sound.play()
		sleep(0.3)
		setStatus(Status.WAITING)
		sleep(0.3)
		setStatus(Status.READY)
		sleep(0.4)
	else:
		setStatus(Status.ERROR)
		print("Invalid Bacode: " + data)
		sleep(1)

def setStatus(status):
	if(status==Status.READY):
		GPIO.output(GREEN_LED, GPIO.HIGH)
		GPIO.output(YELLOW_LED, GPIO.LOW)
		GPIO.output(RED_LED, GPIO.LOW)
	elif(status==Status.WAITING):
		GPIO.output(GREEN_LED, GPIO.LOW)
		GPIO.output(YELLOW_LED, GPIO.HIGH)
		GPIO.output(RED_LED, GPIO.LOW)
	elif(status==Status.ERROR):
		GPIO.output(GREEN_LED, GPIO.LOW)
		GPIO.output(YELLOW_LED, GPIO.LOW)
		GPIO.output(RED_LED, GPIO.HIGH)

def signal_handler(sig, frame):
	print("Exiting...")
	GPIO.cleanup()
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

while True:
	setStatus(Status.READY)
	while (GPIO.input(BUTTON) == GPIO.HIGH):
		sleep(0.1)
	setStatus(Status.WAITING)
	ser.write(SCAN_CMD)
	read()
	data = read()
	process(data)

