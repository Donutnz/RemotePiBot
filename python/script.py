#!/usr/bin/env python3

import socket
import picamera as pc
import time
import serial
import threading as th
import sys
import io
import webiopi
import atexit

stp=th.Event() #Major stop flag for clean exit
strmlive=th.Event()

def streaminit():
	sock=socket.socket()
	try:
		sock.bind(("0.0.0.0",8001))
	except:
		stp.set()
		strmlive.set()
		print("Address already in use error")
		return
	sock.listen(0)
	#sock.connect(("192.168.20.15",8000)) #Enable for client handshake mode
	#con=sock.makefile("wb") #Re-enable for when within network
	con=sock.accept()[0].makefile("wb")
	print("Socks setup")
	try:
		cam=pc.PiCamera()
		cam.resolution=(480,320)
		cam.annotate_text="Hello World"
		cam.framerate=24
		time.sleep(1)
		cam.start_recording(con,format="h264")
		strmlive.set()
		print("Interp: "+str(th.main_thread().name))
		print("Live!")
		stp.wait()
		print("stp called!")
		#mainth=th.main_thread().name
		#mainth.join()
		cam.stop_recording()
	finally:
		con.close()
		sock.close()
		print("Stream ended!")
		return
print("loaded!")

"""@webiopi.macro
def test(val):
	print("Working! "+str(val))
	return val*2"""

"""def arduinoinit():
	global ser
	ser=serial.Serial("//dev//ttyACM0",9600)
	print("Serial comms initiated")
	while True:
		if(stp.is_set()):
			csh="E000"
			ser.write(csh.encode())
			return"""

ser=serial.Serial("//dev//ttyACM0",9600)

@webiopi.macro
def camX(val):
	global ser
	if(len(val)<3):
		val="0"+str(val)
	val="X"+str(val)
	pos=val.encode()
	ser.write(pos)
	print("Wrote "+str(val)+" to the X axis")
	return val
	
@webiopi.macro
def camY(val):
	global ser
	if(len(val)<3):
		val="0"+str(val)
	val="Y"+str(val)
	pos=val.encode()
	ser.write(pos)
	print("Wrote "+str(val)+" to the Y axis")
	return val
	
@webiopi.macro
def motR(val):
	global ser
	if(len(val)<3):
		val="0"+str(val)
	val="R"+str(val)
	pos=val.encode()
	ser.write(pos)
	return val
	
@webiopi.macro
def motL(val):
	global ser
	if(len(val)<3):
		val="0"+str(val)
	val="L"+str(val)
	pos=val.encode()
	ser.write(pos)
	return val
	
@webiopi.macro
def stop():
	ext="E000"
	ext=ext.encode()
	ser.write(ext)
	return True
	
@webiopi.macro
def test(val):
	print("Working! "+str(val))
	return 2

def main():
	global ser
	print("Starting...")
	strm=th.Thread(target=streaminit)
	#ardu=th.Thread(target=arduinoinit)
	strm.start()
	print("Stream ready...")
	#strmlive.wait()
	print("Stream connected!")
	#ardu.start()
	#print("Arduino up...")
	#stp.wait()
	thrs=th.enumerate()
	if(len(thrs)>0):
		print(thrs)
	#rst="E000"
	#ser.write(rst.encode())
	print("Done!")
	return

def parachute():
	stp.set()
	print("May have crashed cleanly!")

atexit.register(parachute)

#if __name__=="__main__" or __name__=="__myscript__":
try:
	main()
except:
	stp.set()
	print("Exited cleanly")

def destroy():
	stp.set()
	print("Destroy called")
	print("Threads: "+str(th.enumerate()))

#stp.set()
print("End of code")




#Written by Donutnz
