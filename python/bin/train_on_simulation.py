import tensorflow as tf

import numpy as np
import gym

import ddpgtf.ddpgtf2WithDataGetter as ddpg
from rl_training.two_wheel_robot import TwoWheelRobot

class DataGetter:
    def __init__(self, env, max_number_of_steps, actor_noise, render):
        self.env = env
        self.max_number_of_steps = max_number_of_steps
        self.actor_noise = actor_noise
        self.render = render

    def run_trial(self, policy):
        last_run_result = []
        obs = self.env.reset()
        for i in range(self.max_number_of_steps):
            self.env.render()
            a = policy.predict(np.reshape(obs, (1, policy.s_dim))) + self.actor_noise()
            obs2, r, done, info = self.env.step(a[0])
            last_run_result.append((obs, a, obs2, r, done, info))
            obs = obs2
            if done:
                break

        return last_run_result


class OnestepDataGetter:
    def __init__(self, env, max_number_of_steps, actor_noise, render):
        self.env = env
        self.max_number_of_steps = max_number_of_steps
        self.actor_noise = actor_noise
        self.render = render

    def run_trial(self, policy):
        last_run_result = []
        obs = self.env.reset()
        for i in range(self.max_number_of_steps):
            self.env.render()
            a = policy.predict(np.reshape(obs, (1, policy.s_dim))) + self.actor_noise()
            obs2, r, done, info = self.env.step(a[0])
            last_run_result.append((obs, a, obs2, r, done, info))
            obs = obs2



def main():
    with tf.compat.v1.Session() as sess:

        # env = TwoWheelRobot()
        env = gym.envs.make("Pendulum-v0")

        seed = 1234
        np.random.seed(seed)
        tf.compat.v1.set_random_seed(seed)
        env.seed(seed)

        tau = 0.001
        minibatch_size = 64
        actor_lr = 0.0001
        critic_lr = 0.001
        gamma = 0.99
        summary_dir = './results/tf_ddpg'
        max_trials = 1000
        buffer_size = 1000000

        actor = ddpg.ActorNetwork(sess, env,
                             actor_lr, tau,
                             minibatch_size)

        critic = ddpg.CriticNetwork(sess, actor,
                               critic_lr, tau,
                               gamma,
                               )

        actor_noise = ddpg.OrnsteinUhlenbeckActionNoise(mu=np.zeros(actor.a_dim))
        data_getter = OnestepDataGetter(env, 100, actor_noise, True)

        ddpg.train(sess, data_getter, actor, critic, summary_dir, buffer_size, seed, minibatch_size, max_trials)


if __name__ == "__main__":
    main()
