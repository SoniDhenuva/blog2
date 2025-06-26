import gymnasium as gym
from gymnasium import spaces
import numpy as np

class MyEnv(gym.Env):
    def __init__(self):
        super(MyEnv, self).__init__()
        
        # Define action space: let's say 2 discrete actions
        self.action_space = spaces.Discrete(2)
        
        # Define observation space: 1D state between 0 and 1
        self.observation_space = spaces.Box(low=0, high=1, shape=(1,), dtype=np.float32)
        
        self.state = None
        self.step_count = 0
        self.max_steps = 100

    def reset(self, seed=None, options=None):
        self.state = np.array([0.5], dtype=np.float32)  # Start in the middle
        self.step_count = 0
        return self.state, {}  # Always return obs, info dict

    def step(self, action):
        # Take an action: move left (0) or right (1)
        if action == 0:
            self.state -= 0.05
        else:
            self.state += 0.05

        # Clamp the state to [0, 1]
        self.state = np.clip(self.state, 0.0, 1.0)
        self.step_count += 1

        # Define a simple reward: reward is higher near the value 1
        reward = float(self.state[0])  # Reward is just the state value

        terminated = self.step_count >= self.max_steps
        truncated = False  # Can be used for time limits or other conditions

        return self.state, reward, terminated, truncated, {}

    def render(self):
        print(f"State: {self.state}")

    def close(self):
        pass




from gymnasium.envs.registration import register

register(
    id='MyEnv-v0',
    entry_point='myenv_module:MyEnv',  # change to the actual file/module path
)




from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env

env = MyEnv()
check_env(env)  # Make sure your env follows Gym API

model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)
