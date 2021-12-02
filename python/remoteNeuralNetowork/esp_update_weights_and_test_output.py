import struct
import time

import onnx
import paho.mqtt.client as mqtt
import remote_network_pb2
import remoteNeuralNetowork.remote_network_pb2 as protos
from remoteNeuralNetowork.get_id_param_pair import get_id_param_pair_iterator

request = remote_network_pb2.ModelEvaluationRequest()
request.input_values.values.append(0)
request.input_values.values.append(0)
request.input_values.values.append(0)

def on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
    print("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt
    client.subscribe("evaluation_result")  # Subscribe to the topic “digitest/test1”, receive any messages published on it


def on_message(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
    print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg
    response = remote_network_pb2.ModelEvaluationResponse()
    response.ParseFromString(msg.payload)
    print(response.output_values.values)


client = mqtt.Client(client_id="constant_request_maker")
client.connect("0.0.0.0")
client.on_connect = on_connect  # Define callback function for successful connection
client.on_message = on_message  # Define callback function for receipt of a message

input_values = protos.NumbersArray(values=[0.0]*45)
request = protos.ModelEvaluationRequest(input_values=input_values)

onnx_model = onnx.load("actor_model.onnx")  # load onnx model
CHUNK_SIZE = 32

def updateWeights(onnx_model, mqttClientHandle):
    id_param_pair_iterator = get_id_param_pair_iterator(onnx_model)
    for id, params in id_param_pair_iterator:
        data_to_send = struct.unpack_from(f"{len(params.raw_data) // 4}f", params.raw_data)
        current_idx = 0
        while current_idx < len(data_to_send):
            end_of_chunk = min(current_idx + CHUNK_SIZE, len(data_to_send))
            input = protos.NumbersArray(values=data_to_send[current_idx:end_of_chunk])
            request_message = protos.ModelUpdateRequest(param_id=id, param_start_offset=current_idx, param_values=input)
            mqttClientHandle.publish("model_update_request", request_message.SerializeToString(), qos=2)
            current_idx = end_of_chunk


client.loop_start()
while True:
    client.publish("evaluation_request", request.SerializeToString())
    updateWeights(onnx_model, client)
    client.publish("evaluation_request", request.SerializeToString())
    time.sleep(5)

