import numpy as np
from gym import Env
from gym.vector.utils import spaces

from rl_training.robot_controller import RobotController


class TwoWheelRobotReal(Env):

    def __init__(self, robotController):
        self.actor = None
        high = 1000
        self.action_space = spaces.Box(-high, high, shape=[2], dtype=np.float32)
        self.observation_space = spaces.Box(-high, high, shape=[3], dtype=np.float32)
        self.robotController: RobotController = robotController
        self.episode_time_seconds = 5
        self.last_activity = None
        self.current_step = None

    def set_actor(self, actor):
        self.actor = actor

    def seed(self, seed=None):
        pass

    def step(self, a):
        step_message = self.last_activity[self.current_step]
        self.current_step += 1
        reward = step_message["reward"]
        observation = step_message["PID_observation"]
        done = self.current_step not in self.last_activity
        return observation, reward, done, {}

    def reset(self):
        self._run_one_episode_and_record_it_()
        return

    def render(self, mode="human"):
        pass

    def _run_one_episode_and_record_it_(self):
        self.robotController.updateWeights(self.actor.parameters())
        self.robotController.activate_nn_controller()

        self.last_activity = self.robotController.record_activity(self.episode_time_seconds)
        self.current_step = 0
        self.robotController.deactivate_robot()

