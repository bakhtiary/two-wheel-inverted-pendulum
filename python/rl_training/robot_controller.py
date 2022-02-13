import time

import numpy as np

import numpy
import json

class RobotController:
    def __init__(self, mqttClientHandle):
        self.mqttClientHandle = mqttClientHandle
        self.current_run_id = 1
        self.incoming_data = {}
        mqttClientHandle.user_data_set(self)
        self.mqttClientHandle.on_connect = MQTT_log_recorder_on_connect
        self.mqttClientHandle.on_message = MQTT_log_recorder_on_message

    def updateWeights(self, id_param_pair_generator):
        CHUNK_SIZE = 8
        for id, params in enumerate(id_param_pair_generator):
            data_to_send = numpy.array(params.data.cpu()).flatten()
            current_idx = 0
            while current_idx < len(data_to_send):
                end_of_chunk = self.send_chunk(CHUNK_SIZE, current_idx, data_to_send, id)
                current_idx = end_of_chunk

    def send_chunk(self, CHUNK_SIZE, current_idx, data_to_send, id):

        end_of_chunk = min(current_idx + CHUNK_SIZE, len(data_to_send))
        request_message = f"""
{{
    "param_id": {id},
    "param_start_offset": {current_idx},
    "param_values": {np.array2string(data_to_send[current_idx:end_of_chunk], separator=', ')}
}}
            """

        self.mqttClientHandle.publish("robot/update_weights", request_message, qos=1)
        return end_of_chunk

    def activate_nn_controller(self):
        return self.change_controller("NEURAL_NET")

    def activate_pid_controller(self):
        return self.change_controller("PID")

    def deactivate_robot(self):
        return self.change_controller("NONE")

    def change_controller(self, controller_type):
        wait_count = 0
        self.current_run_id += 1
        self.mqttClientHandle.publish("robot/set_controller",
                                      json.dumps({"run_id": self.current_run_id, "controller_type": controller_type}),
                                      qos=1)
        while wait_count < 100:
            time.sleep(0.1)
            wait_count += 1
            if self.current_run_id in self.incoming_data:
                return True
        return False

    def reset_position(self):
        self.mqttClientHandle.publish("robot/set_controller", json.dumps({"run_id": 2, "controller_type": "TIMED_MOVE", "lpower": -40, "rpower": -40, "move_millis": 500}))
        time.sleep(2)
        self.mqttClientHandle.publish("robot/set_controller", json.dumps({"run_id": 2, "controller_type": "TIMED_MOVE", "lpower": 30, "rpower": 30, "move_millis": 200}))

    def record_activity(self, episode_time):
        time.sleep(episode_time)
        return self.incoming_data[self.current_run_id].copy()

    def _record_message(self, message):
        message_data = json.loads(message)
        run_id = message_data["run_id"]
        loop_number = message_data["loop_number"]
        if run_id not in self.incoming_data:
            self.incoming_data[run_id] = {}

        self.incoming_data[run_id][loop_number] = message_data

def MQTT_log_recorder_on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
    print("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt
    client.subscribe("robot/alive", qos=1)  # Subscribe to the topic “digitest/test1”, receive any messages published on it

def MQTT_log_recorder_on_message(client, userdata: RobotController, msg):  # The callback for when a PUBLISH message is received from the server.
    userdata._record_message(msg.payload)
