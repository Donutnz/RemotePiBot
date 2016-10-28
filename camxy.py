#!/usr/bin/env python3

import socket
import picamera as pc
import time
import serial
import threading as th
import sys
import io

stp=th.Event() #Major stop flag for clean exit! Only touch if you know what you're doing.
strmlive=th.Event()

def streaminit():
	sock=socket.socket()
	sock.bind(("0.0.0.0",8000)) #From wherever VLC is on your client PC put in "vlc tcp/h264://my_pi_address:8000/" to connect.
	sock.listen(0)
	#sock.connect(("192.168.20.15",8000)) #Enable for client handshake mode. Also use your PC's IP.
	#con=sock.makefile("wb") #Enable for client handshake mode
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
	finally:
		cam.stop_recording()
		con.close()
		sock.close()
		return

def arduinoinit():
	ser=serial.Serial("//dev//ttyACM0",9600)
	print("Serial comms initiated")
	while True:
		try:
			if(stp.is_set()):
				return
			val=str(input("Rotate to: "))
			if(val.upper()!="EXIT"):
				pos=val.encode()
				ser.write(pos)
				print("Written")
			elif(val.upper()=="EXIT"):
				stp.set()
				return
		except:
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

if __name__=="__main__":
	try:
		main()
	except:
		stp.set()
		print("Exited cleanly")




#Written by Donutnz. Use at your own risk.
