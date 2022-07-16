import json
import time
from getkey import getkey


class Interface:
    def __init__(self, logger):
        self.logger = logger

    def run(self, q):

        while True:
            command = getkey()
            time_issued = time.time()
            q.put((time_issued, command))
            self.logger.debug(json.dumps({
                "level": "DEBUG",
                "time_issued": time_issued,
                "command": command,
            }))

