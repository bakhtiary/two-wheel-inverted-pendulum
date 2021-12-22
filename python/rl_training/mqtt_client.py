
import paho.mqtt.client

from rl_training import robot_control_pb2


def get_mqtt_client():

    client = paho.mqtt.client.Client(client_id="rl_agent")
    client.connect("0.0.0.0")

    return client


class MQTTLogRecorder:
    def __init__(self):
        self.client = paho.mqtt.client.Client(client_id="rl_agent", userdata=self)
        self.client.connect("0.0.0.0")


