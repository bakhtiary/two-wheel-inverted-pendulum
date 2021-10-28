from dataclasses import dataclass

from stable_baselines3 import PPO

import numpy as np
from random import Random

from gym.spaces import Discrete
from keras.utils.np_utils import to_categorical


class CachingExtractorDecorator:
    def __init__(self, de):
        self.de = de
        self.cache = {}
    def get_data(self, seed, n):
        key = (seed, n)
        if key in self.cache:
            return self.cache[key]
        else:
            data = self.de.get_data(seed, n)
            self.cache[key] = data
            return data

@dataclass
class DataSet:
    x: np.array
    y: np.array

    def sub_target_dataset(self, idx: int):
        return DataSet(self.x, self.y[:,idx])

    def sub_input_dataset(self, idx):
        return DataSet(self.x[:, idx], self.y)


class DataExtractor:
    def __init__(self, env, get_real_obs_func, agent):
        self.env = env
        self.agent:RandomAgent = agent
        self.get_real_obs_func = get_real_obs_func

    def _get_input_outputs_rewards_for_seed(self, seed):
        r = Random(seed)
        self.env.seed(seed)
        self.agent.reset(r.random())
        self.env.reset()
        obs = self.get_real_obs_func(self.env)
        all_obs = []
        all_rewards = []
        all_dones = []
        all_info = []
        all_actions = []
        dones = False
        while not dones:
            action = self.agent.get_action()
            all_obs.append(obs)
            all_actions.append([action])
            obs, rewards, dones, info = self.env.step(action)
            obs = self.get_real_obs_func(self.env)
            all_rewards.append(rewards)
            all_dones.append(dones)
            all_info.append(info)

        assert isinstance(self.env.action_space, Discrete)
        action_dimentions = self.env.action_space.n
        all_actions_one_hot = to_categorical(all_actions, num_classes=action_dimentions)

        inputs = np.concatenate([all_obs, all_actions_one_hot], axis=1)[:-1]

        outputs_diffs = np.diff(all_obs, axis=0)
        return inputs, outputs_diffs, all_rewards[1:]


    def get_data(self, seed, n):
        all_inputs = []
        all_outputs = []
        for i in range(n):
            inputs, outputs, rewards = self._get_input_outputs_rewards_for_seed(seed + i)
            all_inputs.append(inputs)
            all_outputs.append(outputs[:])


        return DataSet(np.concatenate(all_inputs), np.concatenate(all_outputs))

def get_real_obs_for_luner_lander(env):
    pos = env.lander.position
    vel = env.lander.linearVelocity
    state = [
        pos.x,
        pos.y,
        vel.x,
        vel.y,
        env.lander.angle,
        env.lander.angularVelocity,
        1.0 if env.legs[0].ground_contact else 0.0,
        1.0 if env.legs[1].ground_contact else 0.0,
    ]
    return state


class RandomAgent:
    def reset(self,seed):
        raise NotImplementedError()

    def get_action(self):
        raise NotImplementedError()

class RandomLunarAgent(RandomAgent):
    def __init__(self):
        self.random = Random()

    def reset(self, seed):
        self.random.seed(seed)

    def get_action(self):
        return self.random.choice([0, 1, 2, 3])

if __name__ == "__main__":
    import gym


    env = gym.make('LunarLander-v2')

    de = DataExtractor(env, get_real_obs_for_luner_lander, RandomAgent())

    train_dataX, train_dataY = de.get_data(300, 20)
    test_dataX, test_dataY = de.get_data(1, 10)
