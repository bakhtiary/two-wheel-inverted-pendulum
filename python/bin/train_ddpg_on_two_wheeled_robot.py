import numpy as np
import tensorflow as tf
import ddpgtf.ddpgtf2WithDataGetter as ddpg

class TwoWheelRobotDataGetter:
    pass


def main():
    with tf.compat.v1.Session() as sess:

        data_getter = TwoWheelRobotDataGetter()
        seed = 1234
        np.random.seed(seed)
        tf.compat.v1.set_random_seed(seed)

        tau = 0.005
        minibatch_size = 100
        actor_lr = 0.001
        critic_lr = 0.001
        gamma = 0.99
        summary_dir = './results/tf_ddpg'
        max_trials = 10000000
        buffer_size = 1000000

        actor = ddpg.ActorNetwork(sess, data_getter,
                             actor_lr, tau,
                             minibatch_size)

        critic = ddpg.CriticNetwork(sess, actor,
                               critic_lr, tau,
                               gamma,
                               )

        actor_noise = ddpg.OrnsteinUhlenbeckActionNoise(mu=np.zeros(actor.a_dim))

        ddpg.train(sess, data_getter, actor, critic, summary_dir, buffer_size, seed, minibatch_size, max_trials)
