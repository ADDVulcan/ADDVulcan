import stardb_improved
import math
import numpy as np

def find_by_angles(a1, a2, ab=None):
    min_dist = np.inf
    best = None
    for i, stars_next in enumerate(stardb_improved.stars_next):
        d1 = a1 - stars_next[0]
        d2 = a2 - stars_next[1]
        if ab:
            d3 = ab - stars_next[2]
        else:
            d3 = 0
        dist = math.sqrt(d1*d1 + d2*d2 + d3*d3)
        if dist < min_dist:
            best = i
            min_dist = dist
    return best, min_dist
