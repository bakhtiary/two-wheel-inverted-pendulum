import os
import pickle

import gym
import numpy as np


def get_data():
    from openAIgym.data_extractor import DataExtractor, get_real_obs_for_luner_lander, RandomLunarAgent
    env = gym.make('LunarLander-v2')
    de = DataExtractor(env, get_real_obs_for_luner_lander, RandomLunarAgent())
    ANGULAR_VEL = 5
    sub_target = ANGULAR_VEL
    inputs = range(8, 12)
    test_data = de.get_data(1000, 10).sub_target_dataset(sub_target).sub_input_dataset(inputs)
    val_data = de.get_data(2000, 10).sub_target_dataset(sub_target).sub_input_dataset(inputs)
    train_data = de.get_data(3000, 10).sub_target_dataset(sub_target).sub_input_dataset(inputs)
    return train_data, val_data, test_data


data_file = "tmp.data.pickle"
if os.path.exists(data_file):
    train, val, test = pickle.load(open(data_file, 'rb'))
    print("loaded data")
else:
    train_val_test = get_data()
    pickle.dump(train_val_test, open(data_file, 'wb'))
    train, val, test = train_val_test


class Model():
    def __init__(self, kernel, bias):
        self.kernel = np.array(kernel)
        self.bias = np.array(bias)

    def predict(self, inputs):
        self.zeroth_layer_activation = inputs
        self.first_layer_activation = inputs @ self.kernel + self.bias
        return self.first_layer_activation

    def compute_gradient(self, error):
        bias_error = np.sum(error)
        kernel_error = error @ self.zeroth_layer_activation
        return bias_error, kernel_error

    def adjust_weights(self, bg, kg):
        self.kernel -= kg
        self.bias -= bg


model = Model([.5, .4, .1, .4], [.5])

for i in range(100):
    prediction = model.predict(train.x[i:i+5])
    pred_error = prediction-train.y[i:i+5]
    print("data")
    print(train.x[0:5])
    print("prediction")
    print(prediction)
    print("pred_error")
    print(pred_error)

    print("gradient")
    bg,kg = model.compute_gradient(pred_error)
    print (f"bg{bg}, kg:{kg}")

    model.adjust_weights(bg*0.01,kg*0.01)