
import paho.mqtt.client

from rl_training import robot_control_pb2


def get_mqtt_client():

    def on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
        print("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt
        client.subscribe(
            "evaluation_result")  # Subscribe to the topic “digitest/test1”, receive any messages published on it

    def on_message(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
        print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg
        response = robot_control_pb2.ModelEvaluationResponse()
        response.ParseFromString(msg.payload)
        print(response.output_values.values)

    client = paho.mqtt.client.Client(client_id="rl_agent")
    client.connect("0.0.0.0")
    client.on_connect = on_connect  # Define callback function for successful connection
    client.on_message = on_message  # Define callback function for receipt of a message

    return client