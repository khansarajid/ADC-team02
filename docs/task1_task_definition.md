# Task 1 — Robotic Task Definition and Baseline Simulation

## 1. Task description and objective  (10 pts)

The Unitree G1 (29 DoF) humanoid must learn to drop a ball directly in front
of itself in a controlled and repeatable manner, in MuJoCo simulation.

- Start state: robot standing upright, ball held at the hand position.
- Ball: **4 cm diameter, 50 g** (fixed by the task constraints).
- Desired behaviour: TODO — describe the motion (lower arm forward, release,
  ball lands in target zone, robot remains standing).
- Target zone: NOT strictly defined by the organizers — we define and
  justify it. Proposal: circle of radius **15 cm** centred **35 cm** in
  front of the robot's feet (TODO: adjust + justify, e.g. "reachable by a
  natural arm extension, larger than baseline scatter").
- Out of scope: five-fingered hand control (per task definition, release is
  modelled as detaching the ball in simulation).
- Also fixed by constraints: G1 29DoF, non-learning baseline required, at
  least one completed RL run, saved policy handed over, simulation only.
  Free choices we must defend: algorithm (PPO), reward design, obs/action
  spaces, target size, release strategy.

## 2. Success criteria and evaluation metrics  (10 pts)

| Metric | Definition | Success threshold |
|---|---|---|
| Landing accuracy | distance from ball landing point to target point | < 15 cm |
| Repeatability | std. deviation of landing distance over 30 trials | < TODO cm |
| Success rate | % of trials landing inside target zone | > TODO % |
| Posture stability | torso height stays above 0.5 m (no fall) | 100 % of trials |

## 3. Assumptions and constraints

- Hand/finger control provided externally; release = deactivating the
  ball-to-hand constraint.
- Flat ground, fixed ball mass/size, no external disturbances (sim only).
- Fixed initial pose each episode.
- TODO: add anything else we assume.

## 4. Simulation environment setup and validation  (10 pts)

- MuJoCo version: TODO, model: g1_29dof_rev_1_0 + ball added to scene.
- Validation performed: robot loads and stands stably for N seconds without
  actuation drift; ball obeys gravity and rests in hand via constraint;
  contact between ball and floor detected correctly. (TODO: run + document)

## 5. Baseline behaviour and performance summary  (10 pts)

Non-learning baseline: scripted arm trajectory (linear interpolation over
2 s) followed by ball release (src/baseline.py), 30 trials.

Results (from results/baseline_landings.csv):
- mean landing distance: TODO cm
- std deviation: TODO cm
- success rate: TODO %

This baseline serves as the reference the RL policy (Task 2) must beat.
