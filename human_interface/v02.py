import json
import time
from getkey import getkey


class Interface:
    def __init__(self, logger):
        self.logger = logger

    def run(self, command_q, reward_q):
        self.command_q = command_q
        self.reward_q = reward_q

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
        self.command_q.put((command_time, command))
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
        self.reward_q.put((reward_time, reward))
        self.logger.info(
            json.dumps(
                {
                    "level": "INFO",
                    "ts": reward_time,
                    "reward": reward,
                }
            )
        )
