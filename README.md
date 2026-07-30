# ADC Team 02 — Ball Throw with Reinforcement Learning

Audi Development Camp 2026 — AI Robotics Use Case.

A simulated Unitree G1 (29 DoF) humanoid learns to drop a ball directly in
front of itself using Reinforcement Learning (PPO) in MuJoCo.

## Project structure

```
assets/unitree_g1/  official Unitree G1 29DoF MuJoCo model (from unitree_mujoco)
envs/               Gymnasium environment (adapted from course throw env)
scripts/            scene creation, training, evaluation, playback scripts
                    (adapted from humanoid-robot-fundamentals course repo)
src/                commented reference skeletons (learning material)
models/             (unused — kept for extra scene files)
results/            evaluation graphs, logs, landing-position data
trained_models/     saved policies
docs/               Task 1 task definition, Task 3 Sim2Real concept
```

Credits: G1 model from https://github.com/unitreerobotics/unitree_mujoco;
pipeline scripts adapted from the course repo by Rudolf Krecht.

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

- Benjamin Collu
- Khansa Rajid
- Andrej Krizan
- Daniel Sirghii
- Assyl Mursalim
- Natalia Stranovska

## Task overview

1. **Task 1** — task definition, success criteria, validated sim, scripted baseline
2. **Task 2** — RL pipeline (Gymnasium + Stable-Baselines3 PPO), training, evaluation graphs
3. **Task 3** — Sim2Real gap analysis, robustness concept, limitations, final presentation
