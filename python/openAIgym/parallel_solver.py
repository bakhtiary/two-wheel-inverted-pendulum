import random

import gym
import numpy as np
from scipy.stats import ttest_rel

from openAIgym.dqn_solver import load_solver_state, DQNSolver, single_train_run_and_log, save_solver_state
from openAIgym.dqn_training import single_training_run
from openAIgym.score import ScoreLogger

BATCH_SIZE = 20
GAMMA = 0.95
EXPLORATION_MAX = 1.0
EXPLORATION_MIN = 0.01
EXPLORATION_DECAY = 0.995


def main():
    score_logger = ScoreLogger("CartPole-v1")
    current_step = 100
    env = gym.make("CartPole-v1")
    observation_space = env.observation_space.shape[0]
    action_space = env.action_space.n
    solver = DQNSolverParallel(observation_space, action_space)

    solver.__class__ = DQNSolverParallel
    solver.rand = random.Random(12345)
    single_training_run(solver, env)

    for i in range(current_step, current_step + 100):
        single_train_run_and_log(solver, env, score_logger, i)
        print("saving")
        save_solver_state(solver, "new_training", i)


class DQNSolverParallel(DQNSolver):
    def __init__(self, observation_space, action_space):
        super().__init__(observation_space, action_space)

    def experience_replay(self):
        if len(self.memory) < BATCH_SIZE:
            return
        batch = self.rand.sample(self.memory, BATCH_SIZE)
        states = np.vstack([x[0] for x in batch])
        actions = [x[1] for i,x in enumerate(batch)]
        rewards = np.array([x[2] for x in batch])
        next_states = np.vstack([x[3] for x in batch])
        terminals = [0 if x[4] else 1 for x in batch]

        optimal_values = np.amax(self.model.predict(next_states), axis=1) * terminals
        q_updates = np.array(rewards) + optimal_values
        q_values = self.model.predict(states)
        for i,action in enumerate(actions):
            q_values[i, action] = q_updates[i]
        self.model.fit(states, q_values, verbose=0)

        # for state, action, reward, state_next, terminal in batch:
        #     q_update = reward
        #     if not terminal:
        #         q_update = (reward + GAMMA * np.amax(self.model.predict(state_next)[0]))
        #     q_values = self.model.predict(state)
        #     q_values[0][action] = q_update
        #     self.model.fit(state, q_values, verbose=0)
        self.exploration_rate *= EXPLORATION_DECAY
        self.exploration_rate = max(EXPLORATION_MIN, self.exploration_rate)


if __name__ == "__main__":
    main()


