import time

from rl_training import robot_control_pb2
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
        CHUNK_SIZE = 32
        for id, params in enumerate(id_param_pair_generator):
            data_to_send = numpy.array(params.data.cpu()).flatten()
            current_idx = 0
            while current_idx < len(data_to_send):
                end_of_chunk = min(current_idx + CHUNK_SIZE, len(data_to_send))
                input = robot_control_pb2.NumbersArray(values=data_to_send[current_idx:end_of_chunk])
                request_message = robot_control_pb2.ModelUpdateRequest(param_id=id, param_start_offset=current_idx,
                                                            param_values=input)
                self.mqttClientHandle.publish("robot/model_update_request", request_message.SerializeToString(), qos=1)
                current_idx = end_of_chunk

    def activate_nn_controller(self):
        self.change_controller(robot_control_pb2.ActivateController.NEURAL_NET)

    def activate_pid_controller(self):
        self.change_controller(robot_control_pb2.ActivateController.PID)

    def deactivate_robot(self):
        self.change_controller(robot_control_pb2.ActivateController.DEACTIVATED)

    def change_controller(self, controller_type):
        self.current_run_id += 1
        request_message = robot_control_pb2.ActivateController(type=controller_type, run_id=self.current_run_id)
        self.mqttClientHandle.publish("robot/activate_controller_request", request_message.SerializeToString(), qos=1)

    def record_activity(self, episode_time):
        time.sleep(episode_time)
        return self.incoming_data[self.current_run_id].copy()

    def _record_message(self, message):
        print(message)
        message_data = json.loads(message)
        run_id = message_data["run_id"]
        loop_number = message_data["loop_number"]
        if run_id not in self.incoming_data:
            self.incoming_data[run_id] = {}

        self.incoming_data[run_id][loop_number] = message_data

def MQTT_log_recorder_on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
    print("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt
    client.subscribe("robot/reward")  # Subscribe to the topic “digitest/test1”, receive any messages published on it

def MQTT_log_recorder_on_message(client, userdata: RobotController, msg):  # The callback for when a PUBLISH message is received from the server.
    userdata._record_message(msg.payload)
