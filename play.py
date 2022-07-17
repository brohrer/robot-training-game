import logging
from logging import FileHandler
from logging import Formatter
import multiprocessing as mp
import os
import time
from human_interface.v02 import Interface
from model.v02 import Model
from world.v02 import World
from animation.v00 import Animation

# valid levels are {DEBUG, INFO, WARNING, ERROR, CRITICAL}
LOGGING_LEVEL = logging.DEBUG


def main():
    interface_logger, model_logger, world_logger = set_up_loggers()

    world = World(world_logger)
    model = Model(world.n_actions, model_logger)
    interface = Interface(interface_logger)

    instructions = """
      Welcome to the Robot Training Game.

      Use keys 0-9 as commands.
      Use space bar as "good job!"
      and the minus key as "don't do that"
    """
    print(instructions)

    # Allow the interface to pass commands to the model.
    # Each queue handles one variable being passed from one process to another.
    q_interface_model_command = mp.Queue()
    q_interface_model_reward = mp.Queue()
    q_model_world_action = mp.Queue()
    q_model_world_sensor = mp.Queue()

    p_interface = mp.Process(
        target=interface.run,
        args=(
            q_interface_model_command,
            q_interface_model_reward,
        ))
    p_model = mp.Process(
        target=model.run,
        args=(
            q_interface_model_command,
            q_interface_model_reward,
            q_model_world_action,
            q_model_world_sensor,
        ))
    p_world = mp.Process(
        target=world.run,
        args=(
            q_model_world_action,
            q_model_world_sensor,
        ))

    p_interface.start()
    p_model.start()
    p_world.start()


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

    world_logger = logging.getLogger("world")
    world_logger.setLevel(LOGGING_LEVEL)
    world_logger_file_handler = FileHandler(
        os.path.join("log", f"{time_name}_world.log"))
    world_logger_file_handler.setLevel(LOGGING_LEVEL)
    world_logger_file_handler.setFormatter(Formatter('%(message)s'))
    world_logger.addHandler(world_logger_file_handler)

    return interface_logger, model_logger, world_logger


if __name__ == "__main__":
    main()
