#!/usr/bin/env python3
import pandas as pd
import numpy as np

import angle

ref_catalog = pd.read_csv('test.csv') # import catalog reference vectors

for i,rowt in ref_catalog.iterrows():
    star_cat = np.array([rowt['x'], rowt['y'], rowt['z']])

    next_1_a = np.inf
    next_1_i = None
    next_2_a = np.inf
    next_2_i = None
    for i_t,rowt_t in ref_catalog.iterrows():
        if i == i_t:
            continue
        star_cat_t = np.array([rowt_t['x'], rowt_t['y'], rowt_t['z']])
        a = angle.angle_between(star_cat, star_cat_t)
        if a < next_1_a:
            next_2_a = next_1_a
            next_2_i = next_1_i
            next_1_a = a
            next_1_i = i_t
        elif a < next_2_a:
            next_2_a = a
            next_2_i = i_t
    print("Two closest stars next to", i, ":", next_1_i, next_1_a, next_2_i, next_2_a)
