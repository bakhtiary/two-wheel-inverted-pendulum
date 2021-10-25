import gym
import numpy as np

from openAIgym.dqn_solver import load_solver_state

solver = load_solver_state("LunarLander-v2-end_of_batch", 700)
env = gym.make("LunarLander-v2")

obs = env.reset()
sum_reward = 0
while True:
    obs = np.array(obs).reshape(1,8)
    action = solver.act(obs)
    obs, reward, done, _, = env.step(action)
    sum_reward += reward
    env.render()
    if done:
        break

print(sum_reward)




