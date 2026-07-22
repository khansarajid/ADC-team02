"""
Task 2 — PPO training script.

Run:  python src/train.py
Outputs:
  trained_models/ppo_ball_drop.zip   (the saved policy = deliverable)
  results/training_rewards.csv       (data for the evaluation graphs)
"""

from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import BaseCallback

from ball_drop_env import BallDropEnv

TOTAL_TIMESTEPS = 500_000      # increase if time allows, decrease to test fast
SEED = 42                      # fixed seed -> reproducibility (scored!)


class RewardLogger(BaseCallback):
    """Logs episode rewards so we can plot the learning curve later."""
    def __init__(self):
        super().__init__()
        self.rows = []

    def _on_step(self):
        for info in self.locals.get("infos", []):
            if "episode" in info:   # Monitor wrapper adds this at episode end
                self.rows.append((self.num_timesteps, info["episode"]["r"]))
        return True


def main():
    env = Monitor(BallDropEnv())

    model = PPO(
        "MlpPolicy",
        env,
        seed=SEED,
        verbose=1,
        # sensible defaults; document any change in docs/ for the
        # "training configuration" scoring criterion
        learning_rate=3e-4,
        n_steps=2048,
        batch_size=64,
        gamma=0.99,
    )

    logger = RewardLogger()
    model.learn(total_timesteps=TOTAL_TIMESTEPS, callback=logger)
    model.save("trained_models/ppo_ball_drop")

    import csv
    with open("results/training_rewards.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["timestep", "episode_reward"])
        w.writerows(logger.rows)

    print("Done. Policy saved to trained_models/ppo_ball_drop.zip")


if __name__ == "__main__":
    main()
