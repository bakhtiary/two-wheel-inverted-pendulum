from dataclasses import dataclass

import gym
import numpy as np
from Box2D import b2Vec2


@dataclass
class SpaceSpec:
    observation_space: int
    action_space: int


class DifficultyAdjuster:
    def __init__(self):
        self.difficulty = 0.0

    def recieved_reward(self, reward):
        if reward > 100:
            self.difficulty += 0.01
        elif reward < 100:
            self.difficulty -= 0.01
        self.difficulty = max(min(self.difficulty, 1.0), 0.0)

    def adjustDifficulty(self, env):
        heightdown = (1-self.difficulty) * 9.5

        self.move_body_down(heightdown, env.lander)
        self.move_body_down(heightdown, env.legs[0])
        self.move_body_down(heightdown, env.legs[1])

    def move_body_down(self, heightdown, lander):
        originalpos = lander.position
        lander.position = b2Vec2(originalpos.x, originalpos.y - heightdown)


class EpisodicEnv:
    def __init__(self, env):
        self.env = env
        self.difficulty_adjuster = DifficultyAdjuster()

    def run_episode(self, solver):
        memory_instances = []
        observation_space = self.env.observation_space.shape[0]
        state = self.env.reset()
        self.difficulty_adjuster.adjustDifficulty(self.env)
        state = np.reshape(state, [1, observation_space])
        step = 0
        while True:
            step += 1
            self.env.render()
            action = solver.act(state)
            state_next, reward, terminal, info = self.env.step(action)
            state_next = np.reshape(state_next, [1, observation_space])
            memory_instances.append((state, action, reward, state_next, terminal))
            state = state_next
            if terminal:
                break

        total_reward = np.sum([m[2] for m in memory_instances])
        print("exploration: " + str(solver.exploration_rate) + ", steps: " + str(step) + " last score:" + str(reward) +
              " total reward:" + str(total_reward) + " difficulty:" + str(self.difficulty_adjuster.difficulty))

        self.difficulty_adjuster.recieved_reward(total_reward)

        return memory_instances

    def get_space_specs(self):
        return SpaceSpec(self.env.observation_space.shape[0], self.env.action_space.n)


class Runner:

    def run(self):
        env = gym.make("CartPole-v1")
        EpisodicEnv(env)

if __name__ == "__main__":
    Runner().run()
    