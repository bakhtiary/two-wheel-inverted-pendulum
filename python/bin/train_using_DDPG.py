from stable_baselines3 import DDPG
import torch.onnx

torch.onnx.export()

from rl_training.two_wheel_robot import TwoWheelRobot

env = TwoWheelRobot()


model = DDPG("MlpPolicy", env, verbose=1)

while True:
    obs = env.reset()
    env.render()
    model.learn(total_timesteps=1000)

    for i in range(1000):
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action)
        env.render()
        if done:
            break

