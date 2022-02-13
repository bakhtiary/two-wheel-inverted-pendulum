
import numpy as np
from gym import Env
from gym.vector.utils import spaces

from rl_training.robot_controller import RobotController


def get_observation(step_message):
    observation = np.asarray(step_message["input_values"])
    return observation


class TwoWheelRobotReal(Env):

    def __init__(self, robotController):
        self.actor = None
        self.action_space = spaces.Box(-1.0, 1.0, shape=[2], dtype=np.float32)
        high = 1000
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
        prev_step_message = self.last_activity[self.current_step]
        self.current_step += 1
        cur_step_message = self.last_activity[self.current_step]
        reward = prev_step_message["reward"]
        observation = get_observation(cur_step_message)
        done = (self.current_step + 1) not in self.last_activity
        return observation, reward, done, {}


    def reset(self):
        self._run_one_episode_and_record_it_()
        return get_observation(self.last_activity[self.current_step])


    def render(self, mode="human"):
        pass

    def _run_one_episode_and_record_it_(self):
        activated = False
        self.robotController.reset_position()
        while not activated:
            self.robotController.updateWeights(self.actor.parameters())
            activated = self.robotController.activate_nn_controller()
            if not activated:
                print(f"activated: {activated}  failed activation of nn")
        self.last_activity = self.robotController.record_activity(self.episode_time_seconds)
        self.current_step = 0

        deactivated = False
        while not deactivated:
            deactivated = self.robotController.deactivate_robot()
            if not deactivated:
                print(f"deactivated: {deactivated} failed deactivation")

