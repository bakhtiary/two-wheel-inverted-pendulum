from stable_baselines3 import DDPG

from rl_training.two_wheel_robot import TwoWheelRobotSimulation

env = TwoWheelRobotSimulation()

model = DDPG("MlpPolicy", env, verbose=1, )

while True:
    obs = env.reset()
    env.render()
    model.learn(total_timesteps=1000,)

    for i in range(1000):
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action)
        env.render()
        if done:
            break

