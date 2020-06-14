#!/usr/bin/env python3

import sys
import numpy

file_in_path = sys.argv[1]

d = numpy.fromfile(file_in_path, dtype=numpy.uint8)

for i in range(8):
	p = numpy.packbits(d[i:])
	file_out_path = 'packed_o{:01d}.bin'.format(i)
	p.tofile(file_out_path)
