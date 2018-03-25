# This program enables to control the sunfounder car with a Xbox 360 USB controller via a Mac.
# Please install the Xbox 360 driver first and ensure that the controller is connected to the USB port at the time of booting
# This file replaces the file "client_App.py" of the sunfounder software package.
# Make sure you adapt the host IP adress to your system
# Author: Uwe Sterr
# Date: March 2018
# Version: Draft A
# Version working with following limitations
# Speed control only for forward
# Steering only left, right or straight

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Tkinter import *
from socket import *      # Import necessary modules
import pygame


ctrl_cmd = ['forward', 'backward', 'left', 'right', 'stop', 'read cpu_temp', 'home', 'distance', 'x+', 'x-', 'y+', 'y-', 'xy_home']

top = Tk()   # Create a top window
top.title('Sunfounder Raspberry Pi Smart Video Car')

HOST = '192.168.178.67'    # Server(Raspberry Pi) IP address
PORT = 21567
BUFSIZ = 1024             # buffer size
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)   # Create a socket
tcpCliSock.connect(ADDR)                    # Connect with the server


pygame.init()
 
pygame.joystick.init()
clock = pygame.time.Clock()
 
print pygame.joystick.get_count()
_joystick = pygame.joystick.Joystick(0)
_joystick.init()


# =============================================================================
# The function is to send the command forward to the server, so as to make the 
# car move forward.
# ============================================================================= 
def forward_fun(event):
	print 'forward'
	tcpCliSock.send('forward')

def backward_fun(event):
	print 'backward'
	tcpCliSock.send('backward')

def left_fun(event):
	print 'left'
	tcpCliSock.send('left')

def right_fun(event):
	print 'right'
	tcpCliSock.send('right')

def stop_fun(event):
	print 'stop'
	tcpCliSock.send('stop')

def home_fun(event):
	print 'home'
	tcpCliSock.send('home')

def x_increase(event):
	print 'x+'
	tcpCliSock.send('x+')

def x_decrease(event):
	print 'x-'
	tcpCliSock.send('x-')

def y_increase(event):
	print 'y+'
	tcpCliSock.send('y+')

def y_decrease(event):
	print 'y-'
	tcpCliSock.send('y-')

def xy_home(event):
	print 'xy_home'
	tcpCliSock.send('xy_home')

# =============================================================================
# Exit the GUI program and close the network connection between the client 
# and server.
# =============================================================================
def quit_fun(event):
	top.quit()
	tcpCliSock.send('stop')
	tcpCliSock.close()

# =============================================================================
# Bind buttons on the keyboard with the corresponding callback function to 
# control the car remotely with the keyboard.
# =============================================================================
top.bind('<KeyPress-a>', left_fun)   # Press down key 'A' on the keyboard and the car will turn left.
top.bind('<KeyPress-d>', right_fun) 
top.bind('<KeyPress-s>', backward_fun)
top.bind('<KeyPress-w>', forward_fun)
top.bind('<KeyPress-h>', home_fun)
top.bind('<KeyRelease-a>', home_fun) # Release key 'A' and the car will turn back.
top.bind('<KeyRelease-d>', home_fun)
top.bind('<KeyRelease-s>', stop_fun)
top.bind('<KeyRelease-w>', stop_fun)

spd = 50

def changeSpeed(spd):
	tmp = 'speed'
	#global spd
	#spd = event.value
	data = tmp + str(spd)  # Change the integers into strings and combine them with the string 'speed'. 
	print 'sendData = %s' % data
	tcpCliSock.send(data)  # Send the speed data to the server(Raspberry Pi)

label = Label(top, text='Speed:', fg='red')  # Create a label
label.grid(row=6, column=0)                  # Label layout

speed = Scale(top, from_=0, to=100, orient=HORIZONTAL, command=changeSpeed)  # Create a scale
speed.set(50)
speed.grid(row=6, column=1)

def main():
	#top.mainloop()
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.JOYBUTTONDOWN:
				print("Joystick button pressed.")
				print event
			if event.type == pygame.JOYAXISMOTION:
			#print _joystick.get_axis(0)
			#print event
				if event.axis == 0: # this is the x axis
				    if event.value > 0.7:
				       tcpCliSock.send('right')
				    if event.value < -0.7:
				       tcpCliSock.send('left') 
				    if (event.value < 0.7) & (event.value > -0.6):
				       tcpCliSock.send('home')   
				       
				         
				if event.axis == 3: # this is the x axis
				    if event.value < -0.1:
				       tcpCliSock.send('forward')
				       spd = int(100*abs(event.value))
				       changeSpeed(spd)
				    if event.value > 0.2:
				       tcpCliSock.send('backward')
				    if (event.value < 0.2) & (event.value > -0.6):
				       tcpCliSock.send('stop')      
   
				              
					
				if event.axis == 5: # right trigger
					tcpCliSock.send('right')
		xdir = _joystick.get_axis(0)
 
	rtrigger = _joystick.get_axis(5)
	#deadzone
	if abs(xdir) < 0.2:
		xdir = 0.0
	if rtrigger < -0.9:
		rtrigger = -1.0
 
	MESSAGE = pickle.dumps([xdir,rtrigger])
	sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
 
	clock.tick(30)

if __name__ == '__main__':
	main()

