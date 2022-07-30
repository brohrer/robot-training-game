import multiprocessing as mp
from human_interface.v03 import Interface
from model.v03 import Model
from world.v03 import World
from animation.v01 import Animation


def main():
    world = World()
    model = Model(world.n_actions)
    interface = Interface()
    animation = Animation()

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
    q_interface_animation_command = mp.Queue()
    q_interface_animation_reward = mp.Queue()

    q_model_world_action = mp.Queue()
    q_model_animation_action = mp.Queue()

    q_world_model_sensor = mp.Queue()
    q_world_animation_sensor = mp.Queue()

    p_interface = mp.Process(
        target=interface.run,
        args=(
            q_interface_model_command,
            q_interface_model_reward,
            q_interface_animation_command,
            q_interface_animation_reward,
        ),
    )
    p_model = mp.Process(
        target=model.run,
        args=(
            q_interface_model_command,
            q_interface_model_reward,
            q_model_world_action,
            q_model_animation_action,
            q_world_model_sensor,
        ),
    )
    p_world = mp.Process(
        target=world.run,
        args=(
            q_model_world_action,
            q_world_model_sensor,
            q_world_animation_sensor,
        ),
    )
    p_animation = mp.Process(
        target=animation.run,
        args=(
            q_interface_animation_command,
            q_interface_animation_reward,
            q_model_animation_action,
            q_world_animation_sensor,
        ),
    )

    p_interface.start()
    p_model.start()
    p_world.start()
    p_animation.start()


if __name__ == "__main__":
    main()
