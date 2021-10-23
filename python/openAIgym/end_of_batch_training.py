
from openAIgym.dqn_training import PerEpisodeTrainer

import gym

from openAIgym.dqn_solver import  save_solver_state
from openAIgym.encapsulating_end_of_batch_training import EpisodicEnv
from openAIgym.parallel_solver import DQNSolverParallel
from openAIgym.score import ScoreLogger

def main():
    score_logger = ScoreLogger("CartPole-v1", "end_of_batch")
    env = gym.make("CartPole-v1")
    gym.wrappers
    env = EpisodicEnv(env)
    solver = DQNSolverParallel(env.get_space_specs())
    trainer = PerEpisodeTrainer()

    for i in range(200):
        score = trainer.train(solver, env)
        score_logger.add_score(score, i)
        save_solver_state(solver, "new_training", i)


if __name__ == "__main__":
    main()
