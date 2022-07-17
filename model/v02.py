import json
import time
import numpy as np
from pacemaker.v00 import Pacemaker

CLOCK_FREQ_HZ = 3


class Model:
    def __init__(self, n_actions, logger):
        self.pacemaker = Pacemaker(CLOCK_FREQ_HZ)
        self.n_actions = n_actions
        self.logger = logger

    def run(self, command_q, reward_q, action_q):
        for _ in range(1000):

            self.pacemaker.beat()
            commands = []
            while not command_q.empty():
                gotten = command_q.get()
                commands.append(gotten[1])
                self.logger.debug(json.dumps({
                    "level": "DEBUG",
                    "ts": gotten[0],
                    "command_received": gotten[1],
                }))

            reward = 0
            while not reward_q.empty():
                gotten = reward_q.get()
                reward += gotten[1]
                self.logger.debug(json.dumps({
                    "level": "DEBUG",
                    "ts": gotten[0],
                    "reward_received": gotten[1],
                }))

            actions = self.policy_random()
            action_time = time.time()
            action_q.put((action_time, actions))
            self.logger.info(json.dumps({
                "level": "INFO",
                "ts": action_time,
                "action": list(actions),
            }))

    def policy_random(self):
        """
        Half the time do nothing.
        Half the time randomly pick an action.
        """
        actions = np.zeros(self.n_actions)
        if np.random.sample() < .5:
            i_action = np.random.randint(self.n_actions)
            actions[i_action] = 1
        return actions
