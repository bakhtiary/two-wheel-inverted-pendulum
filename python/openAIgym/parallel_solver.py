import random

import gym
import numpy as np
from scipy.stats import ttest_rel

from openAIgym.dqn_solver import load_solver_state, DQNSolver, save_solver_state
from openAIgym.score import ScoreLogger

def main():
    score_logger = ScoreLogger("CartPole-v1", "parallel_solver")
    current_step = 0
    env = gym.make("CartPole-v1")
    solver = DQNSolverParallel(env)

    for i in range(current_step, current_step + 100):
        single_train_run_and_log(single_training_run, solver, env, score_logger, i)
        print("saving")
        save_solver_state(solver, "new_training", i)


class DQNSolverParallel(DQNSolver):
    def __init__(self, env):
        super().__init__(env)
        self.batch_size = 20

    def experience_replay(self, batch_multiplier=1):
        if len(self.memory) < self.batch_size*batch_multiplier:
            return
        batch = self.rand.sample(self.memory, self.batch_size*batch_multiplier)
        states = np.vstack([x[0] for x in batch])
        actions = [x[1] for i, x in enumerate(batch)]
        rewards = np.array([x[2] for x in batch])
        next_states = np.vstack([x[3] for x in batch])
        terminals = [0 if x[4] else 1 for x in batch]

        optimal_values = np.amax(self.model.predict(next_states), axis=1) * terminals
        q_updates = np.array(rewards) + optimal_values
        q_values = self.model.predict(states)
        for i, action in enumerate(actions):
            q_values[i, action] = q_updates[i]
        self.model.fit(states, q_values, verbose=0)

        for i in range(batch_multiplier):
            self.exploration_rate *= self.EXPLORATION_DECAY
            self.exploration_rate = max(self.EXPLORATION_MIN, self.exploration_rate)




if __name__ == "__main__":
    main()


