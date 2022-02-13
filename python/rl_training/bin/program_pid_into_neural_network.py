import time
import paho.mqtt.client
import torch
from torch import nn
import torch.nn.functional as F

from rl_training.pid_neural_weights import set_weights
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

set_weights(net)

for params in net.parameters():
    print(params)
#
# client = paho.mqtt.client.Client(client_id="rl_agent")
# client.connect("0.0.0.0")
#
# client.loop_start()
# robotController = RobotController(client)
# robotController.updateWeights(net.parameters())
# robotController.activate_nn_controller()
# time.sleep(50)
