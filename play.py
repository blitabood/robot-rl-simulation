from robot_env import GridWorldEnv
from stable_baselines3 import PPO

env = GridWorldEnv()
model = PPO.load("models/my_robot")

obs, info = env.reset()
done = False
total_reward = 0

while not done:
    action, _ = model.predict(obs)
    obs, reward, terminated, truncated, info = env.step(action)
    total_reward += reward
    done = terminated or truncated

print("Итоговая награда:", total_reward)