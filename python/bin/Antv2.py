from stable_baselines3 import PPO

from openAIgym.two_wheel_robot import TwoWheelRobot

env = TwoWheelRobot()

model = PPO("MlpPolicy", env, verbose=1)

while True:
    obs = env.reset()
    env.render()
    model.learn(total_timesteps=1000)

    for i in range(1000):

        action, _states = model.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action)
        env.render()
        if done:
          obs = env.reset()

env.close()