from StupidArtnet import StupidArtnet
import threading
import time


class Fixture:
    def __init__(self, ip, map, fps=60):
        self.ip = ip
        self.map = map
        self.fps = fps
        universes = set([univ for (univ, chan) in self.map])
        self.artnet = {}
        self.data = {}
        self.change = {}
        for universe in universes:
            a = StupidArtnet(self.ip, universe, 512, fps=fps)
            a.start()
            self.artnet[universe] = a
            self.data[universe] = [0] * 512
            self.change[universe] = False
        self.sender = threading.Thread(target=self.loop, args=())
        self.sender.daemon = True
        self.sender.start()

    def set(self, index, value):
        univ, chan = self.map[index]
        self.data[univ][chan] = self.fit(value)
        self.change[univ] = True

    def copy(self, target_index, source_index):
        univ, chan = self.map[source_index]
        temp = self.data[univ][chan]
        univ, chan = self.map[target_index]
        self.data[univ][chan] = temp
        self.change[univ] = True

    def fit(self, value):
        new_value = min(max(int(value), 0), 255)
        return new_value

    def loop(self):
        while True:
            for universe in self.artnet:
                if self.change[universe]:
                    a = self.artnet[universe]
                    a.set(self.data[universe])
                    self.change[universe] = False
            time.sleep(1 / self.fps)
