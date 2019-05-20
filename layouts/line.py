#!/usr/bin/env python
"""Create a layout containing a line."""
import json

SPACING = 1.0 / 60  # m
TOTAL = 4 * 60

points = []
x = y = z = 0

for c in range(-TOTAL / 2, TOTAL / 2):
    x = -c * SPACING
    points.append({"point": [x, y, z]})

print(json.dumps(points, indent=2))
