import numpy as np

from openAIgym.encapsulating_end_of_batch_training import EpisodicEnv


class PerActionTrainer:
    def train(self, dqn_solver, env):

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

class PerEpisodeTrainer:
    def train(self, dqn_solver, env: EpisodicEnv):

        memory_instances = env.run_episode(dqn_solver)
        steps = len(memory_instances)
        for memory_instance in memory_instances:
            dqn_solver.remember(memory_instance)
        dqn_solver.experience_replay(steps)

        return steps


def single_train_run_and_log(run_func, dqn_solver, env, score_logger, run):
    score = run_func(dqn_solver, env)
    score_logger.add_score(score, run)
