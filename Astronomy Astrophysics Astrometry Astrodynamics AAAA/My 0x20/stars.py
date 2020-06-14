import math
import numpy as np

import stardb

def find_by_angles(a1, a2):
    min_dist = np.inf
    best = None
    for i in range(2500):
        d1 = a1 - stardb.stars_next[i][1]
        d2 = a2 - stardb.stars_next[i][3]
        dist = math.sqrt(d1*d1 + d2*d2)
        if dist < min_dist:
            best = i
            min_dist = dist
    return best

if __name__ == "__main__":
    #0: 0.035250079289107186, 1875, 0.043189355150597519
    #1271: 0.034858929585129123, 1891, 0.035587026733103461),
    print(find_by_angles(0.035250079289107186, 0.043189355150597519))
