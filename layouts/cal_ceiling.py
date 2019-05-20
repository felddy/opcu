#!/usr/bin/env python
"""Create a layout for the CAL ceiling."""
import json

# draw a U-shape on ceiling.  Pixel 0 is at lab manager door.

SPACING = 1.0 / 60  # m
EACH_SIDE = 4 * 60

points = []
x = y = 0
z = 2.5  # m

for c in range(0, EACH_SIDE):
    y = c * SPACING
    points.append({"point": [x, y, z]})

for c in range(0, EACH_SIDE):
    x = c * SPACING
    points.append({"point": [x, y, z]})

for c in range(EACH_SIDE, 0, -1):
    y = c * SPACING
    points.append({"point": [x, y, z]})

print(json.dumps(points, indent=2))
