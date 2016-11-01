#!/usr/bin/env python3

import socket
import picamera as pc
import time
import serial
import threading as th
import sys
import io

stp=th.Event() #Major stop flag for clean exit
strmlive=th.Event()

def streaminit():
	sock=socket.socket()
	try:
		sock.bind(("0.0.0.0",8000))
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
		print("Live!")
		stp.wait()
		cam.stop_recording()
	finally:
		con.close()
		sock.close()
		print("Stream ended!")
	return

def arduinoinit():
	ser=serial.Serial("//dev//ttyACM0",9600)
	print("Serial comms initiated")
	while True:
		if(stp.is_set()):
			ser.write("E000")
			return
		try:
			val=str(input("Ready for command (LNNN): "))
			if(val.upper()!="EXIT" and val.upper()!="HELP"):
				if(len(val)<4):
					l=val[0]
					nums=val[1:3]
					val=l+"0"+nums
				pos=val.encode()
				ser.write(pos)
				print("Written")
			elif(val.upper()=="EXIT"):
				ser.write("E000") #End code
				stp.set()
				return
			elif(val.upper()=="HELP"):
				print("Input commands in format \"LNNN\" where L=Letter and N=Number.\nLetters:\nX = X axis (10-170)\nY = Y axis (10-170)\nR = right motor (0-225)\nL = left motor (0-225)\nE000 = reset to normal\nH = help (this)\n")
		except:
			ser.write("E000")
			err=[]
			for x in range(0,len(sys.exc_info())):
				err.append(sys.exc_info()[x])
			stp.set()
			print("Something broke with error:")
			print(err)
			#stp.set()
			return

def main():
	print("Starting...")
	strm=th.Thread(target=streaminit)
	ardu=th.Thread(target=arduinoinit)
	strm.start()
	print("Stream ready...")
	strmlive.wait()
	print("Stream connected!")
	ardu.start()
	print("Arduino up...")
	stp.wait()
	thrs=th.enumerate()
	if(len(thrs)>0):
		print(thrs)
	print("Done!")
	return

if __name__=="__main__":
	try:
		main()
	except:
		stp.set()
		print("Exited cleanly")
