import json
import time


class Interface:
    def __init__(self, logger):
        self.logger = logger

    def run(self, q):

        for _ in range(100):
            time.sleep(0.8)
            command = "a"
            time_issued = time.time()
            q.put((time_issued, command))
            self.logger.debug(
                json.dumps(
                    {
                        "level": "DEBUG",
                        "time_issued": time_issued,
                        "command": command,
                    }
                )
            )
