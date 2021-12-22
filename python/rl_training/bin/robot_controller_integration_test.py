import os
import time

import paho.mqtt.client
from stable_baselines3 import DDPG

from rl_training.mqtt_client import get_mqtt_client
from rl_training.robot_controller import RobotController
from rl_training.two_wheel_robot_real_robot import TwoWheelRobotReal

client = paho.mqtt.client.Client(client_id="rl_agent")
client.connect("0.0.0.0")

client.loop_start()
robotController = RobotController(client)
robotController.activate_pid_controller()
time.sleep(5)

# env = TwoWheelRobotReal(robotController)
#
# model = DDPG("MlpPolicy", env, verbose=1)
#
# robotController.updateWeights(model.actor.parameters())
#
