#!/usr/bin/python3
# -*- coding: utf-8 -*-

import serial
import time
import threading
from audioplayer import AudioPlayer

time.sleep(10)

ports = ['/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyUSB2']
keys = ['H', 'S', 'P']
baud = 9600
music = AudioPlayer('/home/silo/EnergyExpansion/music.mp3')

serials = []
threads = []

for port in ports:
    serials.append(serial.Serial(port, baud, timeout=0))


def serialthread(ser):
    global ports
    global keys
    global music

    i = '-'

    while True:
        for c in ser.read_until():
            c = chr(c)
            if c in keys:
                ser.write(b'K')
                i = c
            if c == 'B':
                print(f'{c} in {i}')
                if i == 'S':
                    music.play(block=False)
                    time.sleep(10)
                    music.stop()
                    ser.reset_input_buffer()
                else:
                    ser.write(b'N')
                    time.sleep(20)
                    ser.write(b'F')
                    ser.reset_input_buffer()


if __name__ == "__main__":
    for ser in serials:
        serial_thread = threading.Thread(target=serialthread, args=(ser,))
        threads.append(serial_thread)
        serial_thread.start()