import gymnasium as gym
import math
import numpy as np

class GridWorldEnv(gym.Env):

    def __init__(self):
        self.max_steps = 500
        self.current_steps = 0

        self.observation_space = gym.spaces.Box(
            low=np.array([0, 0, 0, 0, 0, 0, -180], dtype=float),
            high=np.array([200, 200, 200, 200, 200, 1281, 180], dtype=float),
            shape=(7,),
            dtype=float
            )
        
        self.action_space = gym.spaces.Discrete(3)

        self.x = 50
        self.y = 50
        self.angle = 0
        self.speed = 70
        self.arr = [(400, 200, 100, 200), (800, 500, 50, 100), (40, 700, 20,100), (20, 500, 100,100)]
        self.goal1 = 950
        self.goal2 = 750
        self.width = 1000
        self.height = 800

    def _get_obs(self):
        ans = []
        lights_angle = [-60, -30, 0, 30, 60]
        for ang in lights_angle:
            rad = math.radians(ang + self.angle)
            x_light = 0
            y_light = 0
            for step in range(1, 200, 5):
                x_light = self.x + step * math.cos(rad)
                y_light = self.y - step * math.sin(rad)
                if not (50<= x_light < 1000) or not (50 <= y_light < 800):
                    break
                flag = True
                for j in self.arr:
                    if j[0] < x_light < j[0] + j[2] and j[1] < y_light < j[1] + j[3]:
                        flag = False
                        break
                if flag == False:
                    break
            ans.append(((self.x - x_light)**2 + (self.y - y_light) **2)**0.5)
            
        ans.append(((self.x - self.goal1)**2 + (self.y - self.goal2)**2)**0.5)

        dx = self.goal1 - self.x
        dy = self.goal2 - self.y
        angle_to_goal = math.degrees(math.atan2(-dy, dx))
        relative_angle = angle_to_goal - self.angle
        ans.append(relative_angle)
        return ans

    def reset(self, seed = None, options = None):
        self.current_steps = 0
        self.x = 100
        self.y = 400
        self.angle = 0

        ans = self._get_obs()
        
        return np.array(ans), {}
    
    def step(self, action):
        terminated = False
        self.current_steps += 1
        if self.current_steps >= self.max_steps:
            terminated = True
        reward = 0
        reward -= 0.1
        
        if action == 0:
            self.angle += 15
        elif action == 1:
            self.angle -= 15
        else:
            rad = math.radians(self.angle)
            new_x = self.x + self.speed * math.cos(rad)
            new_y = self.y - self.speed * math.sin(rad)
            collision = False
            for j in self.arr:
                if j[0] < new_x < j[0] + j[2] and j[1] < new_y < j[1] + j[3]:
                    collision = True
                    break

            if collision:
                terminated = True
                reward -= 10
            else:
                self.x = new_x
                self.y = new_y
                if not (50 < self.x < 950 and 50 < self.y < 750):
                    terminated = True
                    reward -= 10

            dist = math.sqrt((self.x - self.goal1)**2 + (self.y - self.goal2)**2)
            if dist < 50:
                reward += 100
                import random
                goal_valid = False
                while not goal_valid:
                    self.goal1 = random.randint(100, self.width - 50)
                    self.goal2 = random.randint(100, self.height - 50)
                    temp = False
                    for j in self.arr:
                        if j[0] < self.goal1 < j[0] + j[2] and j[1] < self.goal2 < j[1] + j[3]:
                            temp = True
                            break
                    if not temp:
                        goal_valid = True
                

        
        ans = self._get_obs()
        return np.array(ans), reward, terminated, False, {}