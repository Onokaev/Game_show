#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import os
from GameGroup import Group

list = []
index = 0
played = False

def colorcode(GroupA):
	global index
	if index == 1:
		GPIO.output(GroupA.BLED, 1)
		GPIO.output(GroupA.RLED, 1)
		GPIO.output(GroupA.GLED, 0)
	elif index == 2:
		GPIO.output(GroupA.BLED, 1)
		GPIO.output(GroupA.RLED, 0)
		GPIO.output(GroupA.GLED, 0)
	elif index == 3:
		GPIO.output(GroupA.BLED, 0)
		GPIO.output(GroupA.RLED, 1)
		GPIO.output(GroupA.GLED, 0)
		
		
def colormatch():
	global list
	for index,GroupA in enumerate(list):
		if index == 0:
			GPIO.output(GroupA.BLED, 1)
			GPIO.output(GroupA.RLED, 1)
			GPIO.output(GroupA.GLED, 0)
		elif index == 1:
			GPIO.output(GroupA.BLED, 1)
			GPIO.output(GroupA.RLED, 0)
			GPIO.output(GroupA.GLED, 0)
		elif index == 2:
			GPIO.output(GroupA.BLED, 0)
			GPIO.output(GroupA.RLED, 1)
			GPIO.output(GroupA.GLED, 0)

GroupA = Group(13,19,6,21,"A")
GroupB = Group(3,4,2,23, "B")
GroupC = Group(10,11,9,25, "C")

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def test(GroupC):
	print("LED {} Test".format(GroupC.Name))
	#GPIO.output(GroupC.RLED, 1)
	#GPIO.output(GroupC.GLED, 1)
	GPIO.output(GroupC.BLED, 1)

	time.sleep(2)

	GPIO.output(GroupC.RLED, 0)
	GPIO.output(GroupC.GLED, 0)
	GPIO.output(GroupC.BLED, 0)
	
def turnoff(Group):
	GPIO.output(Group.RLED, 0)
	GPIO.output(Group.GLED, 0)
	GPIO.output(Group.BLED, 0)
	
GPIO.setup(19, GPIO.OUT )
GPIO.setup(13, GPIO.OUT) #leds for Group A
GPIO.setup(6, GPIO.OUT )

test(GroupA)


GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT) #leds for Group B
GPIO.setup(4, GPIO.OUT)
test(GroupB)

GPIO.setup(10, GPIO.OUT)
GPIO.setup(9, GPIO.OUT) #leds for Group C
GPIO.setup(11, GPIO.OUT)

test(GroupC)

#initialise queue
list = []
os.system('clear')

def callbackA(channel):
	global list,index
	print("Group A")
	#Load into queue
	list.append(GroupA)
	index = index + 1
	#os.system("aplay -qN /home/pi/Success.wav > /dev/null")
	GPIO.remove_event_detect(21)
	#Flash LED strip and make noise
	#colorcode(GroupA)

def callbackB(channel):
	global list,index
	print("Group B")	
	#Load into queue
	list.append(GroupB)
	index = index + 1
	GPIO.remove_event_detect(23)
	#Flash LED strip and make noise
	#colorcode(GroupB)
	
def callbackC(channel):
	global list,index
	print("Group C")
	list.append(GroupC)
	index = index + 1
	#os.system("aplay -qN /home/pi/Success.wav > /dev/null")
	GPIO.remove_event_detect(27)
	#flash led
	#colorcode(GroupC)

def callbackD(channel):
	global list, index, played
	print("Reset")
	os.system('clear')
	for group in list:
		if group.Name == "C":
			GPIO.add_event_detect(27, GPIO.FALLING, callback=callbackC, bouncetime=200)
			
		elif group.Name == "B":
			GPIO.add_event_detect(23, GPIO.FALLING, callback=callbackB, bouncetime=200)
			
		elif group.Name == "A":
			GPIO.add_event_detect(21, GPIO.FALLING, callback=callbackA, bouncetime=200)
			
		else:
			print(' ')
		
		turnoff(group)
		
	list = []
	index = 0
	played = False
	time.sleep(1)
	


GPIO.add_event_detect(21, GPIO.FALLING, callback=callbackA, bouncetime=200)
GPIO.add_event_detect(23, GPIO.FALLING, callback=callbackB, bouncetime=200)
GPIO.add_event_detect(27, GPIO.FALLING, callback=callbackC, bouncetime=200)
GPIO.add_event_detect(5, GPIO.FALLING, callback=callbackD, bouncetime=200)


while 1:
	colormatch()
	if index > 0 and played == False:
		os.system("aplay -qN /home/pi/Success.wav > /dev/null")
		played = True
	pass
	time.sleep(.5)
