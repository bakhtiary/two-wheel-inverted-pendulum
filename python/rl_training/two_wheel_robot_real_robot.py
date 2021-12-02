import numpy as np
from gym import utils
from gym.envs.mujoco import mujoco_env
from gym.envs.robotics.rotations import quat_rot_vec

class TwoWheelRobot():
    def __init__(self, policy):
        self.policy = policy

    def seed(self):
        pass

    def step(self, a):
        pass

    def _get_obs(self):
        pass

    def reset(self):
        self._run_one_episode_and_record_it_()
        return

    def render(self):
        pass

    def _run_one_episode_and_record_it_(self):
        self._upload_weights_()
        self._reset_robot_()
        self._record_observations_()
        pass

    def _upload_weights_(self):
        pass

    def _reset_robot_(self):
        pass

    def _record_observations_(self):
        pass
