import json
from pacemaker.v00 import Pacemaker

CLOCK_FREQ_HZ = 3


class Model:
    def __init__(self, logger):
        self.pacemaker = Pacemaker(CLOCK_FREQ_HZ)
        self.logger = logger

    def run(self, command_q, reward_q):
        for _ in range(1000):

            self.pacemaker.beat()
            commands = []
            while not command_q.empty():
                gotten = command_q.get()
                commands.append(gotten[1])
                self.logger.debug(json.dumps({
                    "level": "DEBUG",
                    "time_issued": gotten[0],
                    "command_received": gotten[1],
                }))

            reward = 0
            while not reward_q.empty():
                gotten = reward_q.get()
                reward += gotten[1]
                self.logger.debug(json.dumps({
                    "level": "DEBUG",
                    "time_issued": gotten[0],
                    "reward_received": gotten[1],
                }))

            print(f"commands {commands}, reward {reward}")
