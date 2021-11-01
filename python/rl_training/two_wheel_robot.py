import numpy as np
from gym import utils
from gym.envs.mujoco import mujoco_env
from gym.envs.robotics.rotations import quat_rot_vec

class TwoWheelRobot(mujoco_env.MujocoEnv, utils.EzPickle):
    def __init__(self):
        mujoco_env.MujocoEnv.__init__(self, "/home/amir/projects/two-wheel-inverted-pendulum/python/rl_training/models/two_wheel_robot.xml", 1)
        utils.EzPickle.__init__(self)


    def step(self, a):
        xposbefore = np.copy(self.get_body_com("buddy"))
        self.do_simulation(a, self.frame_skip)
        xposafter = self.get_body_com("buddy")
        quaternion = self.data.get_body_xquat("buddy")
        up_vec = quat_rot_vec(quaternion, (1, 0, 0))
        lean_up = up_vec[2]
        done = lean_up < 0.6
        movement_reward = -np.linalg.norm(xposbefore - xposafter) * 1000
        done_reward = -100 if done else + 10
        action_reward = -np.sum(np.abs(a))
        reward = done_reward + action_reward + movement_reward
        ob = self._get_obs()
        return (
            ob,
            reward,
            done,
            dict(done_reward=done_reward, movement_reward=movement_reward, action_reward = action_reward),
        )

    def _get_obs(self):
        return np.concatenate(
            [
                self.sim.data.qpos.flat[2:],
                self.sim.data.qvel.flat,
                np.clip(self.sim.data.cfrc_ext, -1, 1).flat,
            ]
        )

    def reset_model(self):
        qpos = self.init_qpos + self.np_random.uniform(
            size=self.model.nq, low=-0.01, high=0.01
        )
        qvel = self.init_qvel + self.np_random.randn(self.model.nv) * 0.01
        self.set_state(qpos, qvel)
        return self._get_obs()

    def viewer_setup(self):
        self.viewer.cam.distance = self.model.stat.extent * 0.5
