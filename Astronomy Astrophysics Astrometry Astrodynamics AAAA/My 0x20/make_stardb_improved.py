#!/usr/bin/env python3
import numpy as np

# Optimized angle function with less error checks
def angle_between(v1, v2):
    if (v1 == v2).all():
        return 0
    return np.arccos(np.dot(v1, v2))

ref_catalog = pd.read_csv('test.csv') # import catalog reference vectors

# Form numpy arrays to speed up calculations
star_positions = [np.array([rowt_t[1]['x'], rowt_t[1]['y'], rowt_t[1]['z']]) for rowt_t in ref_catalog.iterrows()]

print("stars_next = (")
for i, star_pos in enumerate(star_positions):
    angels = [angle_between(star_pos, other_star_pos) for other_star_pos in star_positions]
    # Partitioning be faster than sorting but is harder to understand
    #closest_stars = [0, np.argpartition(angels, 1)[1], np.argpartition(angels, 2)[2]]
    closest_stars = np.argsort(angels)[:3]
    a1 = angels[closest_stars[1]]
    a2 = angels[closest_stars[2]]
    ab = angle_between(star_positions[closest_stars[1]], star_positions[closest_stars[2]])

    print(f'({a1}, {a2}, {ab}),')
print(")")
