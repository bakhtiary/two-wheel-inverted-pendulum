from stable_baselines3 import DDPG

from rl_training.mqtt_client import get_mqtt_client
from rl_training.two_wheel_robot_real_robot import TwoWheelRobotReal
from rl_training.robot_controller import RobotController

client = get_mqtt_client()
client.loop_start()

weightUpdater = RobotController(client)

env = TwoWheelRobotReal(weightUpdater)
model = DDPG("MlpPolicy", env, verbose=1, policy_kwargs={'net_arch':[6,6]})
env.set_actor(model.actor)
while True:
    obs = env.reset()
    model.learn(total_timesteps=1000, )

    for i in range(1000):
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action)
        env.render()
        if done:
            break

