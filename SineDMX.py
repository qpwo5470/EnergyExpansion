from Fixture import Fixture
import time
import math
import threading

class SineDMX:
    def __init__(self, ip, map, fps=60, width=4, speed=0.1, brightness=255, color=(1,1,1)):
        self.ip = ip
        self.map = map
        self.fps = fps
        self.width = width/speed
        self.speed = speed
        self.brightness = brightness
        self.color = color
        self.fixture = Fixture(ip, map, fps=fps)
        self.angle = 0
        self.flowing = False
        self.main_loop = threading.Thread(target=self.loop, args=())
        self.main_loop.daemon = True
        self.main_loop.start()
        
    def flow(self, state):
        self.flowing = state
        
    def loop(self):
        while True:
            for i in reversed(range(self.speed*3, len(self.map))):
                self.fixture.copy(i, i-self.speed*3)
            for i in range(self.speed):
                if self.flowing:
                    sine_val = (math.sin(self.angle+math.floor(i/3)*(1/self.width))+1)*self.brightness
                else:
                    sine_val = 0
                self.fixture.set(0+i*3, sine_val*self.color[0])
                self.fixture.set(1+i*3, sine_val*self.color[1])
                self.fixture.set(2+i*3, sine_val*self.color[2])
            self.angle += 1/self.width
            time.sleep(1/self.fps)