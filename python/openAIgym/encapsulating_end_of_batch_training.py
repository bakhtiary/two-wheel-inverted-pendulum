from dataclasses import dataclass

import gym
import numpy as np

@dataclass
class SpaceSpec:
    observation_space: int
    action_space: int

class EpisodicEnv:
    def __init__(self, env):
        self.env = env

    def run_episode(self, solver):
        memory_instances = []
        observation_space = self.env.observation_space.shape[0]
        state = self.env.reset()
        state = np.reshape(state, [1, observation_space])
        step = 0
        while True:
            step += 1
            # env.render()
            action = solver.act(state)
            state_next, reward, terminal, info = self.env.step(action)
            reward = reward if not terminal else -reward
            state_next = np.reshape(state_next, [1, observation_space])
            memory_instances.append((state, action, reward, state_next, terminal))
            state = state_next
            if terminal:
                print("Run:  exploration: " + str(solver.exploration_rate) + ", score: " + str(step))
                break

        return memory_instances

    def get_space_specs(self):
        return SpaceSpec(self.env.observation_space.shape[0], self.env.action_space.n)


class Runner:

    def run(self):
        env = gym.make("CartPole-v1")
        EpisodicEnv(env)

if __name__ == "__main__":
    Runner().run()
    