from pacemaker.v00 import Pacemaker

CLOCK_FREQ_HZ = 3

class Model:
    def __init__(self):
        self.pacemaker = Pacemaker(CLOCK_FREQ_HZ)

    def run(self):
        self.pacemaker.beat()
