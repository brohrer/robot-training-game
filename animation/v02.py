import json
import logging
from logging import FileHandler
from logging import Formatter
import os
import time
import numpy as np
import matplotlib.pyplot as plt
from pacemaker.v00 import Pacemaker

CLOCK_FREQ_HZ = 2

# valid levels are {DEBUG, INFO, WARNING, ERROR, CRITICAL}
LOGGING_LEVEL = logging.INFO


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
        self.initialize_display()

    def initialize_display(self):
        x_positive_reward = .7
        x_negative_reward = .3
        y_reward = .25
        fontsize_reward = 18
        self.alpha_positive_reward = 1
        self.alpha_negative_reward = 1

        x_commands = np.linspace(.2, .8, 9)
        y_commands = .75
        fontsize_command = 16
        self.alpha_commands = np.ones(9)

        # The rate (fraction per second) at which
        # reward and command influence fades
        decay_rate_per_second = .5
        self.decay_rate = decay_rate_per_second / CLOCK_FREQ_HZ

        self.fig = plt.figure()
        self.ax_main = self.fig.add_axes((0, 0, 1, 1))

        self.positive_reward_text = self.ax_main.text(
            x_positive_reward,
            y_reward,
            "+1",
            horizontalalignment="center",
            verticalalignment="center",
            fontsize=fontsize_reward,
            alpha=self.alpha_positive_reward,
        )
        self.negative_reward_text = self.ax_main.text(
            x_negative_reward,
            y_reward,
            "-1",
            horizontalalignment="center",
            verticalalignment="center",
            fontsize=fontsize_reward,
            alpha=self.alpha_negative_reward,
        )

        self.command_text = []
        self.command_text.append(self.ax_main.text(
            x_commands[0],
            y_commands,
            "1",
            horizontalalignment="center",
            verticalalignment="center",
            fontsize=fontsize_command,
            alpha=self.alpha_commands[0],
        ))
        self.command_text.append(self.ax_main.text(
            x_commands[1],
            y_commands,
            "2",
            horizontalalignment="center",
            verticalalignment="center",
            fontsize=fontsize_command,
            alpha=self.alpha_commands[1],
        ))
        self.command_text.append(self.ax_main.text(
            x_commands[2],
            y_commands,
            "3",
            horizontalalignment="center",
            verticalalignment="center",
            fontsize=fontsize_command,
            alpha=self.alpha_commands[2],
        ))
        self.command_text.append(self.ax_main.text(
            x_commands[3],
            y_commands,
            "4",
            horizontalalignment="center",
            verticalalignment="center",
            fontsize=fontsize_command,
            alpha=self.alpha_commands[3],
        ))
        self.command_text.append(self.ax_main.text(
            x_commands[4],
            y_commands,
            "5",
            horizontalalignment="center",
            verticalalignment="center",
            fontsize=fontsize_command,
            alpha=self.alpha_commands[4],
        ))
        self.command_text.append(self.ax_main.text(
            x_commands[5],
            y_commands,
            "6",
            horizontalalignment="center",
            verticalalignment="center",
            fontsize=fontsize_command,
            alpha=self.alpha_commands[5],
        ))
        self.command_text.append(self.ax_main.text(
            x_commands[6],
            y_commands,
            "7",
            horizontalalignment="center",
            verticalalignment="center",
            fontsize=fontsize_command,
            alpha=self.alpha_commands[6],
        ))
        self.command_text.append(self.ax_main.text(
            x_commands[7],
            y_commands,
            "8",
            horizontalalignment="center",
            verticalalignment="center",
            fontsize=fontsize_command,
            alpha=self.alpha_commands[7],
        ))
        self.command_text.append(self.ax_main.text(
            x_commands[8],
            y_commands,
            "9",
            horizontalalignment="center",
            verticalalignment="center",
            fontsize=fontsize_command,
            alpha=self.alpha_commands[8],
        ))

        self.ax_main.set_xlim(0, 1)
        self.ax_main.set_ylim(0, 1)
        # self.ax_main.set_facecolor(dark_blue)
        self.ax_main.tick_params(
            bottom=False,
            top=False,
            left=False,
            right=False)
        self.ax_main.tick_params(
            labelbottom=False,
            labeltop=False,
            labelleft=False,
            labelright=False)

        plt.ion()
        plt.show()

    def run(
        self,
        interface_command_q,
        interface_reward_q,
        model_action_q,
        world_sensor_q,
    ):
        while True:
            self.pacemaker.beat()

            self.alpha_positive_reward *= 1 - self.decay_rate
            self.alpha_negative_reward *= 1 - self.decay_rate
            self.alpha_commands = [
                a * (1 - self.decay_rate) for a in self.alpha_commands]

            # commands = "!"
            # reward = "!"
            # actions = "!"
            # sensors = "!"
            while not interface_command_q.empty():
                timestamp, commands = interface_command_q.get()
                for command in list(commands):
                    try:
                        self.alpha_commands[int(command) - 1] = 1
                    except IndexError:
                        pass

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
                if int(reward) == 1:
                    self.alpha_positive_reward = 1
                if int(reward) == -1:
                    self.alpha_negative_reward = 1

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
            self.positive_reward_text.set_alpha(self.alpha_positive_reward)
            self.negative_reward_text.set_alpha(self.alpha_negative_reward)
            self.command_text[0].set_alpha(self.alpha_commands[0])
            self.command_text[1].set_alpha(self.alpha_commands[1])
            self.command_text[2].set_alpha(self.alpha_commands[2])
            self.command_text[3].set_alpha(self.alpha_commands[3])
            self.command_text[4].set_alpha(self.alpha_commands[4])
            self.command_text[5].set_alpha(self.alpha_commands[5])
            self.command_text[6].set_alpha(self.alpha_commands[6])
            self.command_text[7].set_alpha(self.alpha_commands[7])
            self.command_text[8].set_alpha(self.alpha_commands[8])
            self.fig.canvas.flush_events()
            '''
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
            '''
