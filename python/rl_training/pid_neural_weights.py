import torch

def set_weights(net):
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