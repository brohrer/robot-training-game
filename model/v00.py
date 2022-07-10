import json
import logging
import os
import time
from pacemaker.v00 import Pacemaker

CLOCK_FREQ_HZ = 3
# valid levels are {DEBUG, INFO, WARNING, ERROR, CRITICAL}
LOGGING_LEVEL = logging.DEBUG


class Model:
    def __init__(self, name="_"):
        self.pacemaker = Pacemaker(CLOCK_FREQ_HZ)

        # Set up logging
        os.makedirs("log", exist_ok=True)
        logging.basicConfig(
            filename=os.path.join("log", f"{name}_model.log"),
            format='%(message)s')

        self.logger = logging.getLogger()
        # levels = {DEBUG, INFO, WARNING, ERROR, CRITICAL}
        self.logger.setLevel(LOGGING_LEVEL)

    def run(self):
        over = self.pacemaker.beat()
        self.logger.debug(json.dumps({
            "level": "DEBUG",
            "over": over,
            "time": time.time(),
        }))

