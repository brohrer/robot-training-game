import json
from pacemaker.v00 import Pacemaker

CLOCK_FREQ_HZ = 48
N_ACTIONS = 2


class World:
    def __init__(self, logger):
        self.pacemaker = Pacemaker(CLOCK_FREQ_HZ)
        self.n_actions = N_ACTIONS
        self.logger = logger

    def run(self, action_q):
        for _ in range(1000):

            self.pacemaker.beat()
            actions = []
            while not action_q.empty():
                gotten = action_q.get()
                actions.append(gotten[1])
                self.logger.debug(
                    json.dumps(
                        {
                            "level": "DEBUG",
                            "ts": gotten[0],
                            "action_received": list(gotten[1]),
                        }
                    )
                )

            # print(f"actions {actions}")
