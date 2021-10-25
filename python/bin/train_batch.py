import gym

from openAIgym.dqn_solver import save_solver_state
from openAIgym.dqn_training import PerEpisodeTrainer
from openAIgym.encapsulating_end_of_batch_training import EpisodicEnv
from openAIgym.parallel_solver import DQNSolverParallel
from openAIgym.score import ScoreLogger

score_logger = ScoreLogger("LunarLander-v2", "end_of_batch_lunar_lander")
env = gym.make("LunarLander-v2")
env = EpisodicEnv(env)
solver = DQNSolverParallel(env.get_space_specs())
trainer = PerEpisodeTrainer()

for i in range(1200):
    score = trainer.train(solver, env)
    score_logger.add_score(int(score), i)
    save_solver_state(solver, "LunarLander-v2-end_of_batch", i)
