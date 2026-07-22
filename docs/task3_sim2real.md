# Task 3 — Sim2Real Concept, Limitations and Final Communication

## 1. Sim2Real gap analysis  (10 pts)

Differences between our simulation and a real Unitree G1 that would affect
the learned policy:

- **Actuator dynamics**: real motors have torque limits, delays and friction
  not perfectly modelled in MuJoCo.
- **Contact/friction**: real ball-hand and ball-floor friction differs from
  simulated coefficients.
- **Sensing**: sim gives perfect joint positions and ball pose; the real
  robot has encoder noise and would need vision to locate the ball/target.
- **Latency**: control loop delays (policy inference + communication) absent
  in sim.
- **State estimation**: exact torso pose is known in sim; estimated (noisily)
  on hardware.
- TODO: rank these by expected impact on OUR specific policy.

## 2. Robustness concept  (10 pts)

How we would make the policy transferable:

- **Domain randomization**: during training, randomize ball mass, friction,
  motor strength, sensor noise, initial pose — so the policy doesn't overfit
  to one perfect world.
- **Action smoothing / rate limits** to avoid jerky commands real motors
  can't execute.
- **Conservative success zone** (larger target margin) to tolerate transfer
  error.
- **Staged transfer**: sim -> sim with noise -> hardware-in-the-loop -> real
  robot with safety harness.

## 3. Limitation analysis  (10 pts)

Honest list of what our solution does NOT cover:

- Hand/finger release dynamics excluded by task definition — real release
  timing physics will differ.
- Trained for one fixed initial pose / ball; not general.
- Limited training budget (one day) — policy may be far from optimal.
- No vision: policy uses ground-truth states available only in sim.
- TODO: add what we observed during the project.

## 4. Next-step recommendations

- Longer training + hyperparameter search.
- Domain randomization implementation (see §2).
- Include hand release in the learned control once hand API is available.
- TODO.
