import json
import logging
from logging import FileHandler
from logging import Formatter
import os
import time
from getkey import getkey

# valid levels are {DEBUG, INFO, WARNING, ERROR, CRITICAL}
LOGGING_LEVEL = logging.DEBUG


class Interface:
    def __init__(self):
        # Set up logging
        os.makedirs("log", exist_ok=True)
        log_name = f"{int(time.time())}"
        self.logger = logging.getLogger("interface")
        self.logger.setLevel(LOGGING_LEVEL)
        logger_file_handler = FileHandler(
            os.path.join("log", f"{log_name}_interface.log")
        )
        logger_file_handler.setLevel(LOGGING_LEVEL)
        logger_file_handler.setFormatter(Formatter("%(message)s"))
        self.logger.addHandler(logger_file_handler)

    def run(
        self,
        model_command_q,
        model_reward_q,
        animation_command_q,
        animation_reward_q,
    ):
        self.model_command_q = model_command_q
        self.model_reward_q = model_reward_q
        self.animation_command_q = animation_command_q
        self.animation_reward_q = animation_reward_q

        while True:
            key = getkey()
            self.logger.debug(
                json.dumps(
                    {
                        "level": "DEBUG",
                        "key_ts": time.time(),
                        "key_grabbed": key,
                    }
                )
            )

            if key == " ":
                self._reward(reward=1)
            if key == "-":
                self._reward(reward=-1)
            if key in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
                self._command(command=key)

    def _command(self, command=None):
        command_time = time.time()
        self.model_command_q.put((command_time, command))
        self.animation_command_q.put((command_time, command))
        self.logger.info(
            json.dumps(
                {
                    "level": "INFO",
                    "ts": command_time,
                    "command": command,
                }
            )
        )

    def _reward(self, reward=None):
        reward_time = time.time()
        self.model_reward_q.put((reward_time, reward))
        self.animation_reward_q.put((reward_time, reward))
        self.logger.info(
            json.dumps(
                {
                    "level": "INFO",
                    "ts": reward_time,
                    "reward": reward,
                }
            )
        )
