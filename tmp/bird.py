import time
import random

import flappy_bird_gym
import numpy as np

env = flappy_bird_gym.make("FlappyBird-v0")

def compute_action(obs, w, ):
    got = obs @ w[1:] + w[0]
    return 1 if got > 0 else 0

def play_one_game(w, max_frame=1000, render=True):
    w = np.array(w)

    obs = env.reset()

    i_frame = 0
    while True:
        # Next action:
        # (feed the observation to your agent here)
        action = compute_action(obs, w) # for a random action
        #print(action, end='')
        # Processing:
        if action == 1:
            last_jumped_frame = i_frame
        obs, reward, done, info = env.step(action)

        # Rendering the game:
        # (remove this two lines during training)
        if render:
            env.render()
            time.sleep(1 / 30)  # FPS

        # Checking if the player is still alive
        if done:
            break
        i_frame += 1
        if i_frame > max_frame:
            break
    return i_frame

def play_one_gen(ws):
    ret = []
    for w in ws:
        score = play_one_game(w, render=False)
        # print(w, score)
        ret.append((w, score))
    return sorted(ret, key= lambda x: -x[1])

def make_a_random_children(parents):
    p1 = parents[np.random.randint(len(parents))]
    p2 = parents[np.random.randint(len(parents))]
    mix = np.random.rand()
    return mix*p1 + (1-mix)*p2

def ga():

    ws = [np.random.rand(3) * 100 - 50 for i in range(1000)]
    got = play_one_gen(ws)
    strong_ones = [g[0] for g in got[:20]]

    for gen in range(20):
        print('-'*10, gen)
        #print(strong_ones)
        children = [make_a_random_children(strong_ones) for i in range(100)]
        ws = strong_ones + children + [np.random.rand(3) * 100 - 50 for i in range(50)]
        got = play_one_gen(ws)
        for w, score in got[:10]:
            print(w, score)
        strong_ones = [g[0] for g in got[:20]]
    return strong_ones
strong_ones = ga()
#score = play_one_game([ -4.11781455,  -1.65197832, -16.41825312], render=False )
#print(score)
#
# score = play_one_game([ 33.46560804,  -7.95878138, -46.16045625] )
# print(score)
print(strong_ones[0])
score = play_one_game(strong_ones[0], max_frame=10000 , render=True)
print(score)
env.close()
