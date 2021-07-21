#!/usr/bin/python3
# -*- coding: utf-8 -*-

import serial
import time
import threading
from audioplayer import AudioPlayer

ports = ['/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyUSB2']
keys = ['H', 'S', 'P']
baud = 9600
music = AudioPlayer('music.mp3')


def serialthread(index):
    global ports
    global keys
    global music

    i = '-'

    while True:
        try:
            ser = serial.Serial(ports[index], baud, timeout=0)
            while True:
                try:
                    for c in ser.read_until():
                        c = chr(c)
                        print(f'{c} in {index}')
                        if c in keys:
                            ser.write(b'K')
                            i = c
                            print(f'{index} is {i}')
                        if c == 'B':
                            if i == 'S':
                                music.play(block=False)
                                time.sleep(10)
                                music.stop()
                            else:
                                ser.write(b'N')
                                time.sleep(10)
                                ser.write(b'F')
                                ser.reset_input_buffer()
                except:
                    pass


        except:
            print(f'cant connect {index}')
            pass


if __name__ == "__main__":
    serial_threadA = threading.Thread(target=serialthread, args=(0,))
    serial_threadA.start()

    serial_threadB = threading.Thread(target=serialthread, args=(1,))
    serial_threadB.start()

    serial_threadC = threading.Thread(target=serialthread, args=(2,))
    serial_threadC.start()