import math
from robot_env import GridWorldEnv
from stable_baselines3 import PPO
import pygame

def draw_light(angle):
    rad = math.radians(angle)
    x_light = 0
    y_light = 0
    for step in range(1, 200, 5):
        x_light = env.x + step * math.cos(rad)
        y_light = env.y - step * math.sin(rad)
        light = pygame.Rect(0, 0, 5, 5)
        light.center = (int(x_light), int(y_light))
        if not (50<= x_light < 1000) or not (50 <= y_light < 800):
            break
        flag = True
        for j in env.arr:
            if light.colliderect(pygame.Rect(j)):
                flag = False
                break
        if flag == False:
            break
    pygame.draw.line(screen, (255, 255, 0), (env.x, env.y), (x_light, y_light))
    return (x_light, y_light)


pygame.init()
width = 1000
height = 800
screen = pygame.display.set_mode((width, height))

color = (205, 157, 227)

screen.fill(color)

image_big= pygame.image.load("images/png.png")
emoji_sprite = pygame.transform.scale(image_big, (100, 100))
screen.blit(emoji_sprite,(0,0))

pygame.display.flip()

emoji_x = 0
angle = 0
speed = 70
x = 100
y = 400

arr = [(400, 200, 100, 200), (800, 500, 50, 100), (40, 700, 20,100), (20, 500, 100,100)]

goal1 = 950
goal2 = 750

env = GridWorldEnv()
model = PPO.load("models/my_robot")
obs, info = env.reset()

wins = 0
font = pygame.font.Font(None, 36)

run = True
while run:
    screen.fill(color)
    text = font.render(f"Побед: {wins}", True, (0, 0, 0))
    screen.blit(text, (10, 10))
    sensor_data = []

    lights_angle = [-60, -30, 0, 30, 60]
    for ang in lights_angle:
        dots = draw_light(ang + env.angle)
        dist = math.sqrt((env.x - dots[0])**2 + (env.y - dots[1])**2)
    print(sensor_data)

    rotated_image = pygame.transform.rotate(emoji_sprite, env.angle)
    rect = rotated_image.get_rect(center=(int(env.x), int(env.y)))
    screen.blit(rotated_image, rect.topleft)   
    pygame.draw.rect(screen, (255, 0, 0), (0, 0, width, height), 3)


    goal = pygame.draw.circle(screen, (0, 255, 0), (env.goal1, env.goal2), 40)
    
    #рисует препятствия
    for j in arr:
        pygame.draw.rect(screen, (255, 0, 0), j)

    dist = math.sqrt((env.x - env.goal1)**2 + (env.y - env.goal2)**2)
    if dist < 50:
        wins += 1

    action, _ = model.predict(obs)
    obs, reward, terminated, truncated, info = env.step(action)

    if reward > 50:
        wins += 1

    if terminated or truncated:
        
        obs, info = env.reset()

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            run = False
    
    pygame.time.Clock().tick(10)

    pygame.display.flip()

pygame.quit()