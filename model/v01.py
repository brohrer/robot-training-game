import json
from pacemaker.v00 import Pacemaker

CLOCK_FREQ_HZ = 3


class Model:
    def __init__(self, logger):
        self.pacemaker = Pacemaker(CLOCK_FREQ_HZ)
        self.logger = logger

    def run(self, q):
        for _ in range(1000):

            self.pacemaker.beat()
            commands = []
            while not q.empty():
                gotten = q.get()
                commands.append(gotten[1])
                self.logger.debug(
                    json.dumps(
                        {
                            "level": "DEBUG",
                            "time_issued": gotten[0],
                            "command_received": gotten[1],
                        }
                    )
                )

            if " " in commands:
                print("rewarded")
            if "/" in commands:
                print("punished")
            print("commands", commands)
