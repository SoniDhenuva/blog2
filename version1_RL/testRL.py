import gym

env_name = "CartPole-v1"
env = gym.make(env_name, render_mode="human")  # specify render_mode here
observation = env.reset()

print("Starting episode")
done = False
while not done:
    action = env.action_space.sample()
    observation, reward, terminated, truncated, info = env.step(action)
    done = terminated or truncated
    env.render()
    print(f"Reward: {reward}, Done: {done}")
print("Episode finished")
env.close()

