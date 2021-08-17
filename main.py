#!/usr/bin/python3
# -*- coding: utf-8 -*-
import serial
import time
import threading
from audioplayer import AudioPlayer
from SineDMX import SineDMX
from MonitoringClient.MonitoringClient import MonitoringClient

time.sleep(10)

mc = MonitoringClient('http://34.64.189.234/post.php')

target_ip = '192.168.1.115'

maps = [[(7, c) for c in reversed(range(0, 369))] + [(6, c) for c in reversed(range(0, 512))],
        [(5, c) for c in reversed(range(72))] + [(4, c) for c in reversed(range(0, 512))] + [(3, c) for c in reversed(range(0, 512))],
        [(2, c) for c in reversed(range(0, 472))] + [(1, c) for c in reversed(range(0, 512))]]
dmx = [SineDMX(target_ip, map, fps=120, speed=3, width=5, brightness=150, color=(1, 1, 1)) for map in maps]


port = '/dev/ttyUSB0'
baud = 9600
states = [False, False, False]

serial = serial.Serial(port, baud, timeout=0)
msg = '-'

def on(i):
    global serial
    global states
    global dmx
    ons = [b'p', b's', b'h']
    if not states[i]:
        states[i] = True
        dmx[i].flow(True)
        serial.write(ons[i])
        if i == 1:
            music_thread = threading.Thread(target=playMusic, args=())
            music_thread.start()
        else:
            off_thread = threading.Thread(target=offThread, args=(i,))
            off_thread.start()

def off(i):
    global serial
    global states
    offs = [b'q', b't', b'g']
    serial.write(offs[i])
    states[i] = False

def dmxOff(i):
    global dmx
    dmx[i].flow(False)

def playMusic():
    global states
    music = AudioPlayer('/home/silo/EnergyExpansion/music.mp3')
    time.sleep(2)
    music.play(block=False)
    time.sleep(17.5)
    dmxOff(1)
    time.sleep(2.5)
    music.stop()
    off(1)

def offThread(i):
    time.sleep(17.5)
    dmxOff(i)
    time.sleep(2.5)
    off(i)

def serialThread(ser):
    global msg

    while True:
        c = ser.read()
        if len(c):
            msg = c
            print(msg)

def playThread():
    global states
    global msg
    global mc

    buttons = [b'P', b'S', b'H']

    while True:
        mc.set('Purifier', states[0])
        mc.set('Speaker', states[1])
        mc.set('Humidifier', states[2])
        if msg in buttons:
            i = buttons.index(msg)
            on(i)
        msg = '-'


if __name__ == "__main__":
    serial_thread = threading.Thread(target=serialThread, args=(serial,))
    serial_thread.start()
    play_thread = threading.Thread(target=playThread, args=())
    play_thread.start()