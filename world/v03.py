import json
import logging
from logging import FileHandler
from logging import Formatter
import os
import time
import numpy as np
from pacemaker.v00 import Pacemaker

CLOCK_FREQ_HZ = 48
N_ACTIONS = 2
N_POSITIONS = 5

# valid levels are {DEBUG, INFO, WARNING, ERROR, CRITICAL}
LOGGING_LEVEL = logging.DEBUG


class World:
    """
    In this world, the agent can occupy one of N_POSITIONS on a line.
    It has two actions available, move right and move left by one position.
    Attempts to move past the last position have no effect.

    action[0] indicates a move to the left
    action[1] indicates a move to the right
    """

    def __init__(self):
        self.pacemaker = Pacemaker(CLOCK_FREQ_HZ)
        self.n_actions = N_ACTIONS
        self.n_positions = N_POSITIONS

        # Initialize the world
        self.position = np.random.randint(self.n_positions)

        # Set up logging
        os.makedirs("log", exist_ok=True)
        log_name = f"{int(time.time())}"
        self.logger = logging.getLogger("world")
        self.logger.setLevel(LOGGING_LEVEL)
        logger_file_handler = FileHandler(
            os.path.join("log", f"{log_name}_world.log"))
        logger_file_handler.setLevel(LOGGING_LEVEL)
        logger_file_handler.setFormatter(Formatter("%(message)s"))
        self.logger.addHandler(logger_file_handler)

    def run(self, model_action_q, model_sensor_q, animation_sensor_q):
        for _ in range(1000):

            self.pacemaker.beat()
            # The combined effect of all actions issued.
            # Positive values are steps to the right.
            # Negative values are steps to the left.
            # Zero means no action.
            net_action = 0
            while not model_action_q.empty():
                timestamp, actions = model_action_q.get()
                self.logger.debug(
                    json.dumps(
                        {
                            "level": "DEBUG",
                            "ts": timestamp,
                            "action_received": list(actions),
                        }
                    )
                )
                net_action = net_action - actions[0] + actions[1]

            # Apply the actions
            self.position += net_action
            # Enforce lower and upper limits
            self.position = np.maximum(
                0, np.minimum(self.n_positions - 1, self.position)
            )
            acted_time = time.time()
            self.logger.debug(
                json.dumps(
                    {
                        "level": "DEBUG",
                        "ts": acted_time,
                        "new_position": int(self.position),
                    }
                )
            )

            # Communicate the new position back to the model
            sensors = np.zeros(self.n_positions)
            try:
                sensors[int(self.position)] = 1
            except IndexError:
                self.logger.debug(
                    json.dumps(
                        {
                            "level": "ERROR",
                            "ts": acted_time,
                            "msg": (
                                f"IndexError assigning position {self.position}"
                                + f"to sensor array of size {sensors.size}"
                            ),
                        }
                    )
                )

            model_sensor_q.put((acted_time, sensors))
            animation_sensor_q.put((acted_time, sensors))
