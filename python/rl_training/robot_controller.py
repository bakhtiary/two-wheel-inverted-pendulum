import struct

from rl_training import robot_control_pb2
import numpy

class RobotController:
    def __init__(self, mqttClientHandle):
        self.mqttClientHandle = mqttClientHandle

    def updateWeights(self, id_param_pair_generator):
        CHUNK_SIZE = 32
        for id, params in enumerate(id_param_pair_generator):
            data_to_send = numpy.array(params.data).flatten()
            current_idx = 0
            while current_idx < len(data_to_send):
                end_of_chunk = min(current_idx + CHUNK_SIZE, len(data_to_send))
                input = robot_control_pb2.NumbersArray(values=data_to_send[current_idx:end_of_chunk])
                request_message = robot_control_pb2.ModelUpdateRequest(param_id=id, param_start_offset=current_idx,
                                                            param_values=input)
                self.mqttClientHandle.publish("model_update_request", request_message.SerializeToString(), qos=2)
                current_idx = end_of_chunk

    def activate_nn_controller(self):
        self.change_controller(robot_control_pb2.ActivateController.NEURAL_NET)

    def activate_pid_controller(self):
        self.change_controller(robot_control_pb2.ActivateController.PID)

    def deactivate_robot(self):
        self.change_controller(robot_control_pb2.ActivateController.DEACTIVATED)

    def change_controller(self, controller_type):
        request_message = robot_control_pb2.ActivateController(type=controller_type)
        self.mqttClientHandle.publish("activate_controller_request", request_message.SerializeToString(), qos=1)


    def record_activity(self, episode_time):
        pass

    def deactivate(self):
        pass