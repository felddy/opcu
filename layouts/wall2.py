#!/usr/bin/env python
"""Create wall layout."""
import json

spacing = 0.11  # m

lines = []
for c in range(-12, 13):
    rs = [range(50), reversed(range(50))][c % 2]
    for r in rs:
        line = {"point": [c * spacing, 0, (r - 24.5) * spacing]}
        lines.append(line)

print(json.dumps(lines, indent=2))
