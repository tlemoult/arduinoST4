# arduinoST4

A graphical interface in python 2.7 and an arduino program

## GUI
![alt text](https://raw.githubusercontent.com/tlemoult/arduinoST4/master/gui/gui.png)

## Hardware
This project based on read to go commercial product. You just need to do mechanics and connect to ST4 port of your telescope.
* Official Arduino Uno board https://store.arduino.cc/arduino-uno-rev3
* Official 4 relay shield http://www.arduino.org/products/shields/arduino-4-relays-shield
* output connexion described in hardware folder.
![alt text](https://raw.githubusercontent.com/tlemoult/arduinoST4/master/hard/arduino-ST4-connection.jpg)

## On the PC side, you need:
* python 2.7  https://www.python.org/downloads/
* pyserial lib  https://pypi.python.org/pypi/pyserial/2.7

## How to run
* install python and pyserial
* on Windows add python path in you PATH environnement variable.
* in a cmd command on windows, or terminal on linux, run the arduinoST4.py you grab in gui folder. For exemple if your arduino serial port is COM3.
```
 python arduinoST4.py COM3
```

This projet was tested on Windows 10 and Linux Ubuntu 16.04LTS
