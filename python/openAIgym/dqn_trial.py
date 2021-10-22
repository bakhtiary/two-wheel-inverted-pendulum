import pickle
from random import Random

import gym
import numpy as np
from scipy.stats import ttest_rel

from openAIgym.dqn_solver import load_solver_state


def run_one_trial(env, solver, seed):
    observation_space = env.observation_space.shape[0]
    solver.seed(seed)
    env.seed(seed)
    state = env.reset()
    state = np.reshape(state, [1, observation_space])
    step = 0
    original_exploration_rate = solver.exploration_rate
    solver.exploration_rate = -1
    while True:
        step += 1
        env.render()
        action = solver.act(state)
        state_next, _, terminal, info = env.step(action)
        state_next = np.reshape(state_next, [1, observation_space])
        state = state_next
        if terminal:
            break

    solver.exploration_rate = original_exploration_rate
    return step


def main():
    solver = load_solver_state("original_training", 220)
    res1 = get_trials_parallel("CartPole-v1", solver, range(100, 110))

    solver = load_solver_state("original_training", 220)
    res2 = get_trials_parallel("CartPole-v1", solver, range(100, 110))

    print(ttest_rel(res1, res2))


def get_trials(env_name, solver, trial_range):
    results = []
    for i in trial_range:
        env = make_seeded_env(env_name, i)
        results.append(run_one_trial(env, solver, i))
    return results

def make_seeded_env(env_name, seed):
    env = gym.make(env_name)
    env.seed_recorded = seed
    env.seed(seed)
    return env

def get_trials_parallel(env_name, solver, trial_range):

    results = {}
    solver.seed(seed=12345)

    original_exploration_rate = solver.exploration_rate

    envs = [make_seeded_env(env_name, seed) for seed in trial_range]

    states = [env.reset() for env in envs]
    step = 0
    solver.exploration_rate = -1
    while len(envs) > 0:

        step += 1
        envs[0].render()
        states = np.vstack([state for state in states]) if len(states) > 1 else states[0].reshape(1,-1)
        actions = np.argmax(solver.model.predict(states), axis=1)
        states_next = []
        remove_list = []
        for action, env in zip(actions, envs):
            state_next, _, terminal, _ = env.step(action)
            if terminal:
                results[env.seed_recorded] = step
                remove_list.append(env)
            else:
                states_next.append(state_next)

        for env in remove_list:
            envs.remove(env)

        states = states_next

    solver.exploration_rate = original_exploration_rate
    return [results[i] for i in trial_range]


if __name__ == "__main__":
    main()
