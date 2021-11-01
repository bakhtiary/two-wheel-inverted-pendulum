
import numpy as np

from stable_baselines3 import DDPG
from stable_baselines3.common.noise import NormalActionNoise, OrnsteinUhlenbeckActionNoise
from rl_training.two_wheel_robot import TwoWheelRobot

env = TwoWheelRobot()


class RealityMocker:
    def __init__(self, env, number_of_steps):
        self.env = env
        self.number_of_steps = number_of_steps

    def run_trial(self, policy):
        last_run_result = []
        obs = self.env.reset()
        last_run_result.append(obs)
        for i in range(self.number_of_steps):
            action = policy.act(obs)
            result = self.env.step(action)
            last_run_result.append((action, result))

        return last_run_result

reality_mocker = RealityMocker(env, 100)

class RealityWrapper:
    def __init__(self, reality_world):
        self.reality_world = reality_world
        self.step = None

    def reset(self):
        self.step = 0
        self.trial_results = self.reality_world.run_trial()
        return self.trial_results[0]

    def step(self, action):
        self.step += 1
        if self.step >= len(self.trial_results):
            raise 'your asking for more than we have'
        return self.trial_results[self.step][1]


reality_to_simulation = RealityWrapper(reality_mocker)

# The noise objects for DDPG
n_actions = env.action_space.shape[-1]
action_noise = NormalActionNoise(mean=np.zeros(n_actions), sigma=0.1 * np.ones(n_actions))

model = DDPG("MlpPolicy", env, action_noise=action_noise, verbose=1,)

model.learn(total_timesteps=100000, log_interval=10)

