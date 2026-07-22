# ADC Team 02 — Ball Drop with Reinforcement Learning

Audi Development Camp 2026 — AI Robotics Use Case.

A simulated Unitree G1 (29 DoF) humanoid learns to drop a ball directly in
front of itself using Reinforcement Learning (PPO) in MuJoCo.

## Project structure

```
models/           G1 robot XML + scene with ball
src/
  baseline.py       Task 1: scripted (non-learning) ball drop
  ball_drop_env.py  Task 2: Gymnasium environment + reward function
  train.py          Task 2: PPO training script
  evaluate.py       Task 2: run trained policy, generate graphs
results/          evaluation graphs, logs, landing-position data
trained_models/   saved policies
docs/             Task 1 task definition, Task 3 Sim2Real concept
```

## Setup

```
python -m venv .venv
.venv\Scripts\activate        # Windows  (Linux/Mac: source .venv/bin/activate)
pip install -r requirements.txt
```

## How to run

```
python src/baseline.py        # run scripted baseline
python src/train.py           # train the RL policy
python src/evaluate.py        # evaluate policy + produce graphs
```

## Team

- Benjamin Collu — <role>
- Khansa Abbasi — <role>
- <add members>

## Task overview

1. **Task 1** — task definition, success criteria, validated sim, scripted baseline
2. **Task 2** — RL pipeline (Gymnasium + Stable-Baselines3 PPO), training, evaluation graphs
3. **Task 3** — Sim2Real gap analysis, robustness concept, limitations, final presentation
