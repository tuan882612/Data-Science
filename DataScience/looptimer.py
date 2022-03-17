from tools import timeit #get timeit from tools.py (custom module)
import random
def random_walk(n):
    position = 0
    walk = [position]
    for i in range(n):
        position += 2*random.randint(0, 1)-1 #position takes up random values
        walk.append(position)# append position to walk
    return walk

n = 1
walk = random_walk(n) #call the function random_walk
timeit("random_walk(n=10000)", globals()) # calculates the total loops and time per loop