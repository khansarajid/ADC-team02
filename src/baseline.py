"""
Task 1 — Non-learning baseline behaviour.

What this script does:
  1. Loads the G1 robot + ball scene in MuJoCo.
  2. Executes a FIXED, hand-scripted arm motion (no AI, no learning):
     lower the arm in front of the robot, then release the ball.
  3. Repeats the drop N times and logs where the ball lands each time.
  4. Saves the landing positions to results/baseline_landings.csv

Why: this is the "before" reference. In Task 2 the RL policy must beat this.

NOTE: adjust JOINT INDICES and the scene path to match our model —
run src/inspect_joints.py (or exercise_01 from the course repo) to find them.
"""

import csv
import numpy as np
import mujoco
import mujoco.viewer

# ---------------------------------------------------------------- settings
SCENE_XML = "models/scene_with_ball.xml"   # TODO: our scene file (robot + ball)
N_TRIALS = 30                              # how many drops to log
TARGET = np.array([0.35, 0.0])             # target landing point (x, y) in metres,
                                           # ~35 cm in front of the robot
BALL_BODY = "ball"                         # TODO: name of ball body in the XML
VISUALIZE = True                           # set False for fast headless runs

# Scripted motion: which actuators move, from what angle to what angle.
# TODO: fill in real actuator indices after inspecting the model.
ARM_ACTUATORS = {
    # actuator_index: (start_angle, end_angle)
    # example: 15: (0.0, 1.2),   # right shoulder pitch
    # example: 18: (0.3, 0.9),   # right elbow
}
MOTION_STEPS = 1000     # ticks to complete the arm motion (~2 s at 500 Hz)
SETTLE_STEPS = 1500     # ticks to wait after release for ball to land/settle


def run_one_trial(model, data, viewer=None):
    """One scripted drop. Returns the ball's final (x, y) landing position."""
    mujoco.mj_resetData(model, data)
    mujoco.mj_forward(model, data)

    # --- Phase 1: scripted arm motion (linear interpolation start -> end)
    for step in range(MOTION_STEPS):
        t = step / MOTION_STEPS  # goes 0.0 -> 1.0
        for idx, (start, end) in ARM_ACTUATORS.items():
            data.ctrl[idx] = start + t * (end - start)
        mujoco.mj_step(model, data)
        if viewer is not None:
            viewer.sync()

    # --- Phase 2: release the ball.
    # Hand control is out of scope per the task definition, so "release" =
    # detaching the ball constraint in the sim (e.g. disable the weld/equality
    # holding the ball to the hand).
    # TODO: implement release for our scene, e.g.:
    #   data.eq_active[BALL_WELD_ID] = 0
    release_ball(model, data)

    # --- Phase 3: let physics play out, then read where the ball ended up.
    for _ in range(SETTLE_STEPS):
        mujoco.mj_step(model, data)
        if viewer is not None:
            viewer.sync()

    ball_pos = data.body(BALL_BODY).xpos  # [x, y, z]
    return ball_pos[0], ball_pos[1]


def release_ball(model, data):
    """Detach the ball from the hand. Implementation depends on our scene XML."""
    # TODO
    pass


def main():
    model = mujoco.MjModel.from_xml_path(SCENE_XML)
    data = mujoco.MjData(model)

    viewer = mujoco.viewer.launch_passive(model, data) if VISUALIZE else None

    landings = []
    for i in range(N_TRIALS):
        x, y = run_one_trial(model, data, viewer)
        dist = np.linalg.norm(np.array([x, y]) - TARGET)
        landings.append((i, x, y, dist))
        print(f"trial {i:02d}: landed at ({x:.3f}, {y:.3f}), "
              f"distance to target = {dist*100:.1f} cm")

    # --- save results
    with open("results/baseline_landings.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["trial", "x", "y", "dist_to_target_m"])
        w.writerows(landings)

    dists = np.array([l[3] for l in landings])
    print("\n=== Baseline summary ===")
    print(f"mean distance to target: {dists.mean()*100:.1f} cm")
    print(f"std  (repeatability):    {dists.std()*100:.1f} cm")
    print(f"success rate (<15 cm):   {(dists < 0.15).mean()*100:.0f} %")

    if viewer is not None:
        viewer.close()


if __name__ == "__main__":
    main()
