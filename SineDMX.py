from Fixture import Fixture
import time
import math
import threading


class SineDMX:
    def __init__(self, ip, map, fps=60, width=4, speed=0.1, brightness=255, color=(1, 1, 1), color_mode=False):
        self.ip = ip
        self.map = map
        self.fps = fps
        self.width = width / speed
        self.speed = speed
        self.brightness = brightness
        self.color = color
        self.fixture = Fixture(ip, map, fps=fps)
        self.angle = 0
        self.flowing = False
        self.color_mode = False
        self.main_loop = threading.Thread(target=self.loop, args=())
        self.main_loop.daemon = True
        self.main_loop.start()

    def flow(self, state):
        self.flowing = state
        self.dim = False

    def colorize(self, col):
        self.color_mode = True
        self.color = col

    def map_value(self, src, src_min, src_max, dst_min, dst_max):
        return (src-src_min)/(src_max-src_min) * (dst_max-dst_min) + dst_min

    def constrain(self, src, dst_min, dst_max):
        return min(max(src, dst_min), dst_max)

    def loop(self):
        while True:
            if self.color_mode:
                br = float(self.brightness)
                for i in range(0, len(self.map), 3):
                    self.fixture.set(i, self.color[i]*br)
                    self.fixture.set(i+1, self.color[i+1]*br)
                    self.fixture.set(i+2, self.color[i+2]*br)
            else:
                int_speed = int(self.speed)
                for i in reversed(range(int_speed * 3, len(self.map))):
                    self.fixture.copy(i, i - int_speed * 3)
                for i in range(int_speed):
                    if self.flowing:
                        sine_val = self.constrain(self.map_value(math.sin(self.angle + math.floor(i / 3) * (1 / self.width)), -1, 1, -150, self.brightness), 0, self.brightness)
                    else:
                        sine_val = 0
                    self.fixture.set(0 + i * 3, sine_val * self.color[0])
                    self.fixture.set(1 + i * 3, sine_val * self.color[1])
                    self.fixture.set(2 + i * 3, sine_val * self.color[2])
                if self.speed > 1.01:
                    self.speed -= 0.01
                print(self.speed)
                self.angle += 1 / self.width
            time.sleep(1 / self.fps)
