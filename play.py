import logging
from logging import FileHandler
from logging import Formatter
import multiprocessing as mp
import os
import time
from human_interface.v02 import Interface
from model.v02 import Model
from world.v00 import World
from animation.v00 import Animation

# valid levels are {DEBUG, INFO, WARNING, ERROR, CRITICAL}
LOGGING_LEVEL = logging.INFO


def main():
    interface_logger, model_logger = set_up_loggers()

    interface = Interface(interface_logger)
    model = Model(model_logger)

    instructions = """
      Welcome to the Robot Training Game.

      Use keys 0-9 as commands.
      Use space bar as "good job!"
      and the / key  as "don't do that"
    """
    print(instructions)

    # Allow the interface to pass commands to the model
    q_interface_model_command = mp.Queue()
    q_interface_model_reward = mp.Queue()
    p_interface = mp.Process(
        target=interface.run,
        args=(q_interface_model_command, q_interface_model_reward,))
    p_model = mp.Process(
        target=model.run,
        args=(q_interface_model_command, q_interface_model_reward,))

    p_interface.start()
    p_model.start()


def set_up_loggers():
    os.makedirs("log", exist_ok=True)
    time_name = f"{int(time.time())}"

    interface_logger = logging.getLogger("interface")
    interface_logger.setLevel(LOGGING_LEVEL)
    interface_logger_file_handler = FileHandler(
        os.path.join("log", f"{time_name}_interface.log"))
    interface_logger_file_handler.setLevel(LOGGING_LEVEL)
    interface_logger_file_handler.setFormatter(Formatter('%(message)s'))
    interface_logger.addHandler(interface_logger_file_handler)

    model_logger = logging.getLogger("model")
    model_logger.setLevel(LOGGING_LEVEL)
    model_logger_file_handler = FileHandler(
        os.path.join("log", f"{time_name}_model.log"))
    model_logger_file_handler.setLevel(LOGGING_LEVEL)
    model_logger_file_handler.setFormatter(Formatter('%(message)s'))
    model_logger.addHandler(model_logger_file_handler)

    return interface_logger, model_logger


if __name__ == "__main__":
    main()
