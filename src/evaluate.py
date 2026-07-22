"""
Task 2 — Evaluation: learning curve + trained policy vs. baseline.

Run:  python src/evaluate.py
Outputs:
  results/learning_curve.png        (reward over training time)
  results/policy_landings.csv       (landing positions of trained policy)
  results/comparison.png            (baseline vs. RL landing distances)
"""

import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from stable_baselines3 import PPO

from ball_drop_env import BallDropEnv, TARGET

N_EVAL_EPISODES = 30


def plot_learning_curve():
    steps, rewards = [], []
    with open("results/training_rewards.csv") as f:
        for row in csv.DictReader(f):
            steps.append(int(row["timestep"]))
            rewards.append(float(row["episode_reward"]))
    # smooth with a moving average so the trend is visible
    k = max(1, len(rewards) // 50)
    smooth = np.convolve(rewards, np.ones(k) / k, mode="valid")

    plt.figure(figsize=(8, 4))
    plt.plot(steps, rewards, alpha=0.25, label="episode reward")
    plt.plot(steps[k - 1:], smooth, label=f"moving avg (k={k})")
    plt.xlabel("training timesteps")
    plt.ylabel("episode reward")
    plt.title("PPO learning curve — ball drop task")
    plt.legend()
    plt.tight_layout()
    plt.savefig("results/learning_curve.png", dpi=150)
    print("saved results/learning_curve.png")


def eval_policy():
    env = BallDropEnv()
    model = PPO.load("trained_models/ppo_ball_drop")

    dists = []
    with open("results/policy_landings.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["episode", "x", "y", "dist_to_target_m"])
        for ep in range(N_EVAL_EPISODES):
            obs, _ = env.reset()
            done = False
            while not done:
                action, _ = model.predict(obs, deterministic=True)
                obs, _, terminated, truncated, _ = env.step(action)
                done = terminated or truncated
            ball = env.data.body("ball").xpos
            d = np.linalg.norm(ball[:2] - TARGET)
            dists.append(d)
            w.writerow([ep, ball[0], ball[1], d])
    return np.array(dists)


def plot_comparison(policy_dists):
    base = []
    with open("results/baseline_landings.csv") as f:
        for row in csv.DictReader(f):
            base.append(float(row["dist_to_target_m"]))

    plt.figure(figsize=(6, 4))
    plt.boxplot([np.array(base) * 100, policy_dists * 100],
                labels=["baseline (scripted)", "RL policy"])
    plt.ylabel("landing distance to target (cm)")
    plt.title("Baseline vs. learned behaviour")
    plt.tight_layout()
    plt.savefig("results/comparison.png", dpi=150)
    print("saved results/comparison.png")

    print(f"\nbaseline: mean {np.mean(base)*100:.1f} cm | "
          f"RL: mean {policy_dists.mean()*100:.1f} cm")


if __name__ == "__main__":
    plot_learning_curve()
    d = eval_policy()
    plot_comparison(d)
