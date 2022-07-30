class Animation:
    def _init__(self):
        pass

            q_interface_animation_command,
            q_interface_animation_reward,
            q_model_animation_action,
            q_world_animation_sensor,

# TODO: Write animation printing values at the command line
################## world
import json
import time
import numpy as np
from pacemaker.v00 import Pacemaker

CLOCK_FREQ_HZ = 48
N_ACTIONS = 2
N_POSITIONS = 5


class World:
    """
    In this world, the agent can occupy one of N_POSITIONS on a line.
    It has two actions available, move right and move left by one position.
    Attempts to move past the last position have no effect.

    action[0] indicates a move to the left
    action[1] indicates a move to the right
    """
    def __init__(self, logger):
        self.pacemaker = Pacemaker(CLOCK_FREQ_HZ)
        self.n_actions = N_ACTIONS
        self.n_positions = N_POSITIONS
        self.logger = logger

        # Initialize the world
        self.position = np.random.randint(self.n_positions)


    def run(self, action_q, sensor_q):
        for _ in range(1000):

            self.pacemaker.beat()
            # The combined effect of all actions issued.
            # Positive values are steps to the right.
            # Negative values are steps to the left.
            # Zero means no action.
            net_action = 0
            while not action_q.empty():
                timestamp, actions = action_q.get()
                self.logger.debug(json.dumps({
                    "level": "DEBUG",
                    "ts": timestamp,
                    "action_received": list(actions),
                }))
                net_action = net_action - actions[0] + actions[1]

            # Apply the actions
            self.position += net_action
            # Enforce lower and upper limits
            self.position = np.maximum(0, np.minimum(
                self.n_positions - 1, self.position))
            acted_time = time.time()
            self.logger.debug(json.dumps({
                "level": "DEBUG",
                "ts": acted_time,
                "new_position": int(self.position),
            }))

            # Communicate the new position back to the model
            sensors = np.zeros(self.n_positions)
            try:
                sensors[int(self.position)] = 1
            except IndexError:
                self.logger.debug(json.dumps({
                    "level": "ERROR",
                    "ts": acted_time,
                    "msg": (f"IndexError assigning position {self.position}" +
                        f"to sensor array of size {sensors.size}"),
                }))

            sensor_q.put((acted_time, sensors))
