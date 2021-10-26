import numpy as np
from gym import utils
from gym.envs.mujoco import mujoco_env
from gym.envs.robotics.rotations import quat_rot_vec


class TwoWheelRobot(mujoco_env.MujocoEnv, utils.EzPickle):
    def __init__(self):
        mujoco_env.MujocoEnv.__init__(self, "/home/amir/projects/two-wheel-inverted-pendulum/python/openAIgym/models/two_wheel_robot.xml", 5)
        utils.EzPickle.__init__(self)

    def step(self, a):
        self.do_simulation(a, self.frame_skip)
        quaternion = self.data.get_body_xquat("buddy")
        up_vec = quat_rot_vec(quaternion, (1, 0, 0))
        lean_up = up_vec[2]
        reward = lean_up
        done = lean_up < 0.5
        ob = self._get_obs()
        return (
            ob,
            reward,
            done,
            dict(
            ),
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
            size=self.model.nq, low=-0.1, high=0.1
        )
        qvel = self.init_qvel + self.np_random.randn(self.model.nv) * 0.1
        self.set_state(qpos, qvel)
        return self._get_obs()

    def viewer_setup(self):
        self.viewer.cam.distance = self.model.stat.extent * 0.5
