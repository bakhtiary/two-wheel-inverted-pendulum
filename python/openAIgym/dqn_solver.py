import pickle
import random

import gym
import keras
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizer_v2.adam import Adam

from openAIgym.score import ScoreLogger

ENV_NAME = "CartPole-v1"


class DQNSolver:

    def __init__(self, env_spaces):

        self.GAMMA = 0.95
        self.LEARNING_RATE = 0.001

        self.MEMORY_SIZE = 1000000
        self.BATCH_SIZE = 20

        self.EXPLORATION_MAX = 1.0
        self.EXPLORATION_MIN = 0.01
        self.EXPLORATION_DECAY = 0.995

        self.rand = random.Random(12345)
        self.exploration_rate = self.EXPLORATION_MAX

        self.observation_space = env_spaces.observation_space
        self.action_space = env_spaces.action_space

        self.memory = deque(maxlen=self.MEMORY_SIZE)

        self.model = Sequential()
        self.model.add(Dense(24, input_shape=(self.observation_space,), activation="relu"))
        self.model.add(Dense(24, activation="relu"))
        self.model.add(Dense(self.action_space, activation="linear"))
        self.model.compile(loss="mse", optimizer=Adam(lr=self.LEARNING_RATE))



    def seed(self, seed):
        self.rand = random.Random(seed)

    def remember(self, memory_instance):
        self.memory.append(memory_instance)

    def act(self, state):
        if self.rand.uniform(0,1) < self.exploration_rate:
            return self.rand.randrange(self.action_space)
        q_values = self.model.predict(state)
        return np.argmax(q_values[0])

    def experience_replay(self):
        if len(self.memory) < self.BATCH_SIZE:
            return
        batch = self.rand.sample(self.memory, self.BATCH_SIZE)
        for state, action, reward, state_next, terminal in batch:
            q_update = reward
            if not terminal:
                q_update = (reward + self.GAMMA * np.amax(self.model.predict(state_next)[0]))
            q_values = self.model.predict(state)
            q_values[0][action] = q_update
            self.model.fit(state, q_values, verbose=0)
        self.exploration_rate *= self.EXPLORATION_DECAY
        self.exploration_rate = max(self.EXPLORATION_MIN, self.exploration_rate)

    def experience_replay_for_batch_size(self, batch_size):
        if len(self.memory) < batch_size:
            return
        batch = self.rand.sample(self.memory, batch_size)
        for state, action, reward, state_next, terminal in batch:
            q_update = reward
            if not terminal:
                q_update = (reward + self.GAMMA * np.amax(self.model.predict(state_next)[0]))
            q_values = self.model.predict(state)
            q_values[0][action] = q_update
            self.model.fit(state, q_values, verbose=0)
        self.exploration_rate *= self.EXPLORATION_DECAY
        self.exploration_rate = max(self.EXPLORATION_MIN, self.exploration_rate)

def main():
    env = gym.make(ENV_NAME)
    observation_space = env.observation_space.shape[0]
    action_space = env.action_space.n
    dqn_solver = DQNSolver(observation_space, action_space)

    score_logger = ScoreLogger(ENV_NAME,"normal")

    current_step = 0
    if current_step > 0:
        dqn_solver = load_solver_state("new_training", current_step)

    for i in range(current_step, current_step + 400):
        single_train_run_and_log(single_training_run, dqn_solver, env, score_logger, i)
        print("saving")
        save_solver_state(dqn_solver, "new_training", i)


def load_solver_state(training_name: str, current_step: int):
    dqn_solver = pickle.load(open(dqn_filename(training_name, current_step), "rb"))
    dqn_solver.model = keras.models.load_model(model_filename(training_name, current_step))
    return dqn_solver


def save_solver_state(dqn_solver, file_path, i):
    keras.models.save_model(dqn_solver.model, model_filename(file_path, i))
    model = dqn_solver.model
    dqn_solver.model = None
    pickle.dump(dqn_solver, open(dqn_filename(file_path, i), "wb"))
    dqn_solver.model = model


def model_filename(file_path, i):
    return f"{file_path}/training_step_{i}" + ".model"


def dqn_filename(file_path, i):
    return f"{file_path}/training_step_{i}.dqn_solver"


if __name__ == "__main__":
    main()