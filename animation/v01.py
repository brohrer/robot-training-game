import json
import logging
from logging import FileHandler
from logging import Formatter
import os
import time
import numpy as np
from pacemaker.v00 import Pacemaker

CLOCK_FREQ_HZ = 2

# valid levels are {DEBUG, INFO, WARNING, ERROR, CRITICAL}
LOGGING_LEVEL = logging.DEBUG


class Animation:
    def __init__(self):
        self.pacemaker = Pacemaker(CLOCK_FREQ_HZ)

        # Set up logging
        os.makedirs("log", exist_ok=True)
        log_name = f"{int(time.time())}"
        self.logger = logging.getLogger("animation")
        self.logger.setLevel(LOGGING_LEVEL)
        logger_file_handler = FileHandler(
            os.path.join("log", f"{log_name}_animation.log")
        )
        logger_file_handler.setLevel(LOGGING_LEVEL)
        logger_file_handler.setFormatter(Formatter("%(message)s"))
        self.logger.addHandler(logger_file_handler)

    def run(
        self,
        interface_command_q,
        interface_reward_q,
        model_action_q,
        world_sensor_q,
    ):
        while True:
            self.pacemaker.beat()

            commands = "!"
            reward = "!"
            actions = "!"
            sensors = "!"
            while not interface_command_q.empty():
                timestamp, commands = interface_command_q.get()
                self.logger.debug(
                    json.dumps(
                        {
                            "level": "DEBUG",
                            "ts": timestamp,
                            "ts_received": time.time(),
                            "commands": list(commands),
                        }
                    )
                )
            while not interface_reward_q.empty():
                timestamp, reward = interface_reward_q.get()
                self.logger.debug(
                    json.dumps(
                        {
                            "level": "DEBUG",
                            "ts": timestamp,
                            "ts_received": time.time(),
                            "reward": reward,
                        }
                    )
                )
            while not model_action_q.empty():
                timestamp, actions = model_action_q.get()
                self.logger.debug(
                    json.dumps(
                        {
                            "level": "DEBUG",
                            "ts": timestamp,
                            "ts_received": time.time(),
                            "actions": list(actions),
                        }
                    )
                )
            while not world_sensor_q.empty():
                timestamp, sensors = world_sensor_q.get()
                self.logger.debug(
                    json.dumps(
                        {
                            "level": "DEBUG",
                            "ts": timestamp,
                            "ts_received": time.time(),
                            "sensors": list(sensors),
                        }
                    )
                )
            try:
                print(
                    commands,
                    reward,
                    actions,
                    sensors,
                    "                                ",
                    end="\r",
                )
            except Exception:
                pass
