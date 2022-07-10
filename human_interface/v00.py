import json
# import logging
import os
import time

# valid levels are {DEBUG, INFO, WARNING, ERROR, CRITICAL}
# LOGGING_LEVEL = logging.DEBUG

class Interface:
    def __init__(self, logger):
        self.logger = logger

        # Set up logging
        # os.makedirs("log", exist_ok=True)
        # logging.basicConfig(
        #     filename=os.path.join("log", f"{name}_interface.log"),
        #     format='%(message)s')

        # self.logger = logging.getLogger("interface")
        # self.logger.setLevel(LOGGING_LEVEL)

    def run(self, q):

        for _ in range(100):
            time.sleep(.8)
            command = "a"
            time_issued = time.time()
            q.put((time_issued, command))
            self.logger.debug(json.dumps({
                "level": "DEBUG",
                "time_issued": time_issued,
                "command": command,
            }))

