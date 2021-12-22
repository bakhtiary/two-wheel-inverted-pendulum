import time

from rl_training.robot_controller import RobotController
import paho.mqtt.client

client = paho.mqtt.client.Client(client_id="rl_agent")
client.connect("0.0.0.0")

client.loop_start()
robotController = RobotController(client)
robotController.deactivate_robot()
time.sleep(5)