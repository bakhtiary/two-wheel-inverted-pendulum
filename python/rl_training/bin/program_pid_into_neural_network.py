import time
import paho.mqtt.client
import torch
from torch import nn
import torch.nn.functional as F

from rl_training.robot_controller import RobotController


class Net(nn.Module):

    def __init__(self):
        self.first_layer_size = 6
        self.second_layer_size = 6

        super(Net, self).__init__()
        # an affine operation: y = Wx + b
        self.fc1 = nn.Linear(3, self.first_layer_size)  # 5*5 from image dimension
        self.fc2 = nn.Linear(self.first_layer_size, self.second_layer_size)
        self.fc3 = nn.Linear(self.second_layer_size, 2)

    def forward(self, x):
        x = torch.flatten(x, 1) # flatten all dimensions except the batch dimension
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

net = Net()

def set_weights(net: Net):
    for params in net.parameters():
        params.data.fill_(0.0)

    net.fc1.weight.data[0, 0] = 1.0
    net.fc1.weight.data[1, 0] = -1.0

    net.fc1.weight.data[2, 1] = 1.0
    net.fc1.weight.data[3, 1] = -1.0

    net.fc1.weight.data[4, 2] = 1.0
    net.fc1.weight.data[5, 2] = -1.0

    const_mult_factor = 500
    P = 650/ const_mult_factor
    I = 5.0/ const_mult_factor
    D = 600/ const_mult_factor

    net.fc2.weight.data = torch.eye(net.first_layer_size)

    net.fc3.weight.data[0, 0] = P
    net.fc3.weight.data[0, 1] = -P
    net.fc3.weight.data[1, 0] = P
    net.fc3.weight.data[1, 1] = -P

    net.fc3.weight.data[0, 2] = I
    net.fc3.weight.data[0, 3] = -I
    net.fc3.weight.data[1, 2] = I
    net.fc3.weight.data[1, 3] = -I

    net.fc3.weight.data[0, 4] = D
    net.fc3.weight.data[0, 5] = -D
    net.fc3.weight.data[1, 4] = D
    net.fc3.weight.data[1, 5] = -D



set_weights(net)

for params in net.parameters():
    print(params)

client = paho.mqtt.client.Client(client_id="rl_agent")
client.connect("0.0.0.0")

client.loop_start()
robotController = RobotController(client)
robotController.updateWeights(net.parameters())
robotController.activate_nn_controller()
time.sleep(50)
