# Task 3 — Sim2Real Concept, Limitations and Final Communication

Structured to match the Task 3 scoring rubric (4 × 10 pts) and the
ADC_Sim2Real lecture. Graders explicitly want NAMED, SPECIFIC assumptions
that would fail on the real G1 — not generic disclaimers.

## 1. Sim2Real gap analysis  (10 pts)

Frame: reality = simulation + reality gap. Our policy is optimized against
MuJoCo's model, not the world. Specific gaps for OUR ball-drop setup,
ranked by expected impact:

1. **Contact & release physics** — MuJoCo uses a soft, convex contact model
   that allows slight interpenetration. Our "release" is deactivating a weld
   constraint — a mechanism that does not exist physically. On the real G1,
   release timing depends on finger opening dynamics and ball-hand friction.
   Contact is where every simulator lies the most (cf. OpenAI Shadow-hand
   friction cheat) — this is our biggest gap.
2. **Actuator dynamics** — in sim, commanded torque = applied torque in one
   step. Real G1 joints have PD-loop delay, friction, backlash, current
   limits. A policy that learned sharp wrist/elbow motions would overshoot.
3. **Observations** — our policy sees perfect qpos/qvel and exact ball
   position. The real robot has quantized encoders, noisy finite-difference
   velocities, and NO sensor that reports ball position at all — it would
   need vision. This observation gap alone prevents naive zero-shot
   transfer of our current policy.
4. **Latency** — real control loop ≈ 10–20 ms of staleness; in sim, zero.
   For a short ballistic event like a drop, release-timing error of one
   control step directly shifts the landing point.
5. **Fixed-base assumption** — we train with the pelvis anchored; the real
   robot must actively balance during the arm motion (reaction forces from
   moving the arm + releasing 50 g are small but nonzero).
6. **Morphology** — CAD vs. built robot: link masses ±5–15%, CoM ±5–20 mm.
   Affects the arm trajectory slightly, and balance more.

## 2. Robustness concept  (10 pts)

Ordered as the lecture recommends — boring modelling fixes first, then
randomization:

1. **Better modelling first**: cap actuator torque/velocity to G1 driver
   limits; match sim control rate to the real 50 Hz loop; add sensor noise
   from datasheets; model the PD controller in sim.
2. **Domain randomization** (per episode): ball mass 50 g ± 20%, ball-hand
   friction µ ∈ [0.3, 1.2], release-time jitter, link masses ±10%,
   motor gain ±20%, action delay 0–25 ms, observation Gaussian noise.
   Goal: the real world becomes "just one more sample" of the training
   distribution.
3. **Action-rate penalty** ‖a_t − a_{t−1}‖² in the reward (the Cassie
   lesson) — prevents jerky commands real motors can't track.
4. **Exploit check**: watch rollouts, don't just read reward curves. Log max
   joint velocities/torques; if they exceed G1 hardware limits, the policy
   is cheating the simulator.
5. **Safety envelope for deployment**: joint velocity/torque clamps,
   conservative target zone, kill-switch.

## 3. Limitation analysis  (10 pts)

- Ball position observed from sim ground truth — no perception pipeline;
  real deployment would need a camera + estimator (or fixed assumptions).
- Hand/finger release excluded by task definition — our release model
  (weld deactivation) is the least transferable component.
- Fixed base during training → policy never learned balance recovery.
- Single fixed initial pose and ball; no generalization claimed.
- Limited training budget: policy is one completed run, not tuned.
- Trained and evaluated in ONE simulator — MuJoCo-vs-other-engine
  disagreement is a lower bound on our sim-vs-reality disagreement.
- What would need to change for hardware: staged transfer (sim → sim+noise
  → hardware with harness), system identification of arm joints, vision.

## 4. Final presentation (10 pts)

Required story arc: task → baseline → RL approach → results/graphs →
Sim2Real → next steps. Checklist:

- [ ] task definition + success metrics (numbers)
- [ ] baseline behaviour + its honest failures
- [ ] reward function + training config rationale
- [ ] learning curve + baseline-vs-policy comparison graph
- [ ] gap analysis (top 3 gaps, specific to our setup)
- [ ] robustness plan (DR recipe table)
- [ ] limitations, stated plainly
- [ ] next-step recommendations
