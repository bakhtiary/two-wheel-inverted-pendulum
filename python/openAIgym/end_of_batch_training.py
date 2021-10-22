import tensorflow as tf
tf.compat.v1.disable_eager_execution()

import random

import gym

from openAIgym.dqn_solver import single_train_run_and_log, save_solver_state
from openAIgym.dqn_training import single_training_run, single_training_run_at_end
from openAIgym.parallel_solver import DQNSolverParallel
from openAIgym.score import ScoreLogger

def main():
    score_logger = ScoreLogger("CartPole-v1", "end_of_batch")
    current_step = 0
    env = gym.make("CartPole-v1")
    solver = DQNSolverParallel(env)

    solver.rand = random.Random(12345)
    single_training_run(solver, env)

    for i in range(current_step, current_step + 200):
        single_train_run_and_log(single_training_run_at_end, solver, env, score_logger, i)
        save_solver_state(solver, "new_training", i)


if __name__ == "__main__":
    main()
