# RemotePiBot
Remotely controllable Raspberry Pi rover.

### Description
This is a simple set of scripts to remotely control a Raspberry Pi robot and view a video stream from the picamera. An Arduino is used for the actual electronics, connected to the Pi via USB. It can be run with a web interface or without. If you want to control via command line, use camxy.py and ignore "python" and "html".

### Requirements:
#### Hardware:
* Raspberry Pi 3 (or 2 with WiFi dongle)
* Arduino Uno (or comparable)
* Picamera
* 2 Servos (I used 9g hobby ones, may or may not work with others)
* Arduino power source (I used 6 AAs)
* Raspberry Pi power source (The higher the amperage the better, lower may cause RPi crashes)
* Any double 6V DC motor system that supports PWM. (More info [Here](https://learn.adafruit.com/adafruit-arduino-lesson-13-dc-motors/overview "Adafruit to the rescue"), I'm using the guts from an old [Titan Tank](https://www.electronickits.com/titan-tank-robot-kit-ck21531n/))
#### Software
* Python 3
* WebIoPi (web interface only)
* Arduino SDK
* VLC (on the client PC)


### Disclaimer
This project is still under heavy development so run at your own risk. Only use it if you know what you are doing as screwups can result in fried electronics. This code is best used for reference.
