import numpy as np


def single_training_run(dqn_solver, env):

    observation_space = env.observation_space.shape[0]

    state = env.reset()
    state = np.reshape(state, [1, observation_space])
    step = 0
    while True:
        step += 1
        env.render()
        action = dqn_solver.act(state)
        state_next, reward, terminal, info = env.step(action)
        reward = reward if not terminal else -reward
        state_next = np.reshape(state_next, [1, observation_space])
        dqn_solver.remember(state, action, reward, state_next, terminal)
        state = state_next
        if terminal:
            print("Run:  exploration: " + str(dqn_solver.exploration_rate) + ", score: " + str(step))
            break
        dqn_solver.experience_replay()
    return step


def single_training_run_at_end(dqn_solver, env):

    observation_space = env.observation_space.shape[0]

    state = env.reset()
    state = np.reshape(state, [1, observation_space])
    step = 0
    while True:
        step += 1
        # env.render()
        action = dqn_solver.act(state)
        state_next, reward, terminal, info = env.step(action)
        reward = reward if not terminal else -reward
        state_next = np.reshape(state_next, [1, observation_space])
        dqn_solver.remember(state, action, reward, state_next, terminal)
        state = state_next
        if terminal:
            print("Run:  exploration: " + str(dqn_solver.exploration_rate) + ", score: " + str(step))
            break

    dqn_solver.experience_replay(step)

    return step

