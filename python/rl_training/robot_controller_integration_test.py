from rl_training.mqtt_client import get_mqtt_client
from rl_training.robot_controller import RobotController

client = get_mqtt_client()

robotController = RobotController(client)

robotController.activate_pid_controller()
