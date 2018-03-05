#!/usr/bin/env python
import json
import sys

def ceiling():
    SPACING = 1.0 / 60  # m
    ROOM_WIDTH = 4.5 #m
    ROOM_LENGTH = 6.0 #m
    NORTH_LEDS = SOUTH_LEDS = int(ROOM_LENGTH * 60)
    EAST_LEDS = WEST_LEDS = int(ROOM_WIDTH * 60)


    # 0,0           y-axis             0,6.0
    # -->>------- North 6m --------------
    # |            Rack       Bath      |
    # |                                 v
    # | West 4.5m             East 4.5m v
    # ^ Screen                          |
    # ^                                 |
    # |  Shelves              Back door |
    # ----------- South 6m ----------<<--
    # 4.5,0                           4.5,6.0
    #           x 4.5,1.93
    #           | 2.23m high

    points = []
    x = y = 0
    z = 2.4 #m

    # North
    for c in range(0, NORTH_LEDS):
        y = c * SPACING
        points.append({'point':[x,y,z]})
    y = (c+1) * SPACING

    # East
    for c in range(0, EAST_LEDS):
        x = c * SPACING
        points.append({'point':[x,y,z]})
    x = (c+1) * SPACING

    # South
    for c in range(SOUTH_LEDS, 0, -1):
        y = c * SPACING
        points.append({'point':[x,y,z]})
    y = (c-1) * SPACING

    # West
    for c in range(WEST_LEDS, 0, -1):
        x = c * SPACING
        if c == WEST_LEDS - 20:
            # drop below screen soffit
            z -= 0.2
        elif c == 20:
            # up after screen
            z += 0.2
        points.append({'point':[x,y,z]})

    return points

def main():
    points = ceiling()
    print(json.dumps(points, indent=2))

if __name__=='__main__':
    main()
