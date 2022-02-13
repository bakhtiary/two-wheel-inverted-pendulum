import os

from stable_baselines3 import DDPG

from rl_training.mqtt_client import get_mqtt_client
from rl_training.two_wheel_robot_real_robot import TwoWheelRobotReal
from rl_training.robot_controller import RobotController

client = get_mqtt_client()
client.loop_start()

weightUpdater = RobotController(client)

env = TwoWheelRobotReal(weightUpdater)

result_directory = "./training_results"
model_path = f"{result_directory}/real_model_training_results.zip"
tensorboard_log = f"{result_directory}/tensorboard_log/"
replay_buffer_path = f"{result_directory}/replay_buffer"

if os.path.exists(model_path):
    model = DDPG.load(model_path, env, tensorboard_log=tensorboard_log)
    model.load_replay_buffer(replay_buffer_path)
    model.load(model_path)
    print("model loaded")
else:
    model = DDPG("MlpPolicy", env, verbose=1, policy_kwargs={'net_arch':[6,6]}, learning_starts=0, learning_rate=1e-5, tensorboard_log=tensorboard_log)
    neural_module = model.actor.get_submodule('mu')
    for params in neural_module.parameters():
        params.data.fill_(0.0)

env.set_actor(model.actor)

while True:
    obs = env.reset()
    model.learn(total_timesteps=100,reset_num_timesteps=False, tb_log_name="firstTry", )
    print("saving")
    model.save(model_path)
    model.save_replay_buffer(replay_buffer_path)


