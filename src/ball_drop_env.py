"""
Task 2 — Gymnasium environment for the ball-drop task.

This is the "adapter" between MuJoCo (physics) and Stable-Baselines3 (RL).
The RL algorithm only ever calls reset() and step() — everything about our
task (observations, actions, rewards, episode end) is defined HERE.

The reward function lives in _compute_reward(). That's the heart of Task 2.
"""

import numpy as np
import gymnasium as gym
from gymnasium import spaces
import mujoco

SCENE_XML = "models/scene_with_ball.xml"   # TODO: our scene file
BALL_BODY = "ball"
TARGET = np.array([0.35, 0.0])             # target landing point (x, y)
MAX_EPISODE_STEPS = 2000                   # timeout (~4 s at 500 Hz)
FALL_HEIGHT = 0.5                          # torso below this = robot fell


class BallDropEnv(gym.Env):
    """The G1 must drop the ball ~35 cm in front of itself, repeatably."""

    def __init__(self):
        super().__init__()
        self.model = mujoco.MjModel.from_xml_path(SCENE_XML)
        self.data = mujoco.MjData(self.model)
        self.step_count = 0

        # ACTION: one command per actuator, scaled to [-1, 1].
        n_act = self.model.nu
        self.action_space = spaces.Box(-1.0, 1.0, shape=(n_act,), dtype=np.float32)

        # OBSERVATION: what the "brain" gets to see each tick:
        # joint positions + joint velocities + ball position (3).
        n_obs = self.model.nq + self.model.nv + 3
        self.observation_space = spaces.Box(-np.inf, np.inf, shape=(n_obs,),
                                            dtype=np.float32)

    # ------------------------------------------------------------------ core
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        mujoco.mj_resetData(self.model, self.data)
        mujoco.mj_forward(self.model, self.data)
        self.step_count = 0
        return self._get_obs(), {}

    def step(self, action):
        # scale [-1, 1] action to each actuator's real control range
        low, high = self.model.actuator_ctrlrange.T
        self.data.ctrl[:] = low + (action + 1.0) * 0.5 * (high - low)

        mujoco.mj_step(self.model, self.data)
        self.step_count += 1

        obs = self._get_obs()
        reward = self._compute_reward()
        terminated = self._robot_fell() or self._ball_landed()
        truncated = self.step_count >= MAX_EPISODE_STEPS
        return obs, reward, terminated, truncated, {}

    # --------------------------------------------------------------- helpers
    def _get_obs(self):
        ball = self.data.body(BALL_BODY).xpos
        return np.concatenate([self.data.qpos, self.data.qvel, ball]).astype(
            np.float32)

    def _compute_reward(self):
        """THE reward function. The policy learns exactly what we reward."""
        reward = 0.0
        ball = self.data.body(BALL_BODY).xpos

        # 1) shaping: ball horizontally close to target -> less negative
        dist = np.linalg.norm(ball[:2] - TARGET)
        reward += -dist

        # 2) big bonus when the ball lands in the target zone
        if self._ball_landed() and dist < 0.15:
            reward += 100.0

        # 3) heavy penalty for falling over — posture stability matters
        if self._robot_fell():
            reward -= 50.0

        # 4) small penalty on wild movements (smoothness / energy)
        reward -= 0.001 * np.square(self.data.ctrl).sum()

        return reward

    def _ball_landed(self):
        return self.data.body(BALL_BODY).xpos[2] < 0.05  # ball height < 5 cm

    def _robot_fell(self):
        # TODO: replace "torso" with the actual root/torso body name in our XML
        return self.data.body("torso").xpos[2] < FALL_HEIGHT
