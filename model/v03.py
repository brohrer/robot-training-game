import json
import logging
from logging import FileHandler
from logging import Formatter
import os
import time
import numpy as np
from pacemaker.v00 import Pacemaker

CLOCK_FREQ_HZ = 3

# valid levels are {DEBUG, INFO, WARNING, ERROR, CRITICAL}
LOGGING_LEVEL = logging.INFO


class Model:
    def __init__(self, n_actions):
        self.pacemaker = Pacemaker(CLOCK_FREQ_HZ)
        self.n_actions = n_actions

        # Set up logging
        os.makedirs("log", exist_ok=True)
        log_name = f"{int(time.time())}"
        self.logger = logging.getLogger("model")
        self.logger.setLevel(LOGGING_LEVEL)
        logger_file_handler = FileHandler(
            os.path.join("log", f"{log_name}_model.log"))
        logger_file_handler.setLevel(LOGGING_LEVEL)
        logger_file_handler.setFormatter(Formatter("%(message)s"))
        self.logger.addHandler(logger_file_handler)

    def run(
        self,
        interface_command_q,
        interface_reward_q,
        world_action_q,
        animation_action_q,
        world_sensor_q,
    ):
        for _ in range(1000):

            self.pacemaker.beat()
            commands = []
            while not interface_command_q.empty():
                gotten = interface_command_q.get()
                commands.append(gotten[1])
                self.logger.debug(
                    json.dumps(
                        {
                            "level": "DEBUG",
                            "ts": gotten[0],
                            "command_received": gotten[1],
                        }
                    )
                )

            reward = 0
            while not interface_reward_q.empty():
                gotten = interface_reward_q.get()
                reward += gotten[1]
                self.logger.debug(
                    json.dumps(
                        {
                            "level": "DEBUG",
                            "ts": gotten[0],
                            "reward_received": gotten[1],
                        }
                    )
                )

            sensors = []
            while not world_sensor_q.empty():
                gotten = world_sensor_q.get()
                sensors.append(gotten[1])
                self.logger.debug(
                    json.dumps(
                        {
                            "level": "DEBUG",
                            "ts": gotten[0],
                            "sensor_received": list(gotten[1]),
                        }
                    )
                )

            actions = self.policy_random()
            action_time = time.time()
            world_action_q.put((action_time, actions))
            animation_action_q.put((action_time, actions))
            self.logger.info(
                json.dumps(
                    {
                        "level": "INFO",
                        "ts": action_time,
                        "action": list(actions),
                    }
                )
            )

    def policy_random(self):
        """
        Half the time do nothing.
        Half the time randomly pick an action.
        """
        actions = np.zeros(self.n_actions)
        if np.random.sample() < 0.5:
            i_action = np.random.randint(self.n_actions)
            actions[i_action] = 1
        return actions
