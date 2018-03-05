#!/usr/bin/env python
import json
import sys

def shelves():
    #   0-17    18-35
    #  71-54    53-36
    #  72-89    90-107
    # 143-126  125-108

    # top left pixel location in room
    GLOBAL_X = 4.5 # m
    GLOBAL_Y = 2.1 # m
    GLOBAL_Z = 2.23 # m

    SHELF_COLS = 2
    SHELF_ROWS = 4
    SHELF_LED_COUNT = 18

    LED_SPACING = 1.0 / 48  # m
    SHELF_H_SPACING = 0.15
    SHELF_V_SPACING = 0.25

    SHELF_WIDTH = SHELF_LED_COUNT * LED_SPACING
    SHELF_HEIGHT = SHELF_WIDTH

    points = []

    for sr in range(SHELF_ROWS):
        sc_r = [reversed(range(SHELF_COLS)), range(SHELF_COLS)][sr % 2]
        for sc in sc_r:
            i_r = [reversed(range(SHELF_LED_COUNT)), range(SHELF_LED_COUNT)][sr % 2]
            for i in i_r:
                x = GLOBAL_X
                y = GLOBAL_Y + (i*LED_SPACING) + (sc*(SHELF_WIDTH+SHELF_H_SPACING))
                z = GLOBAL_Z - sr * (SHELF_HEIGHT+SHELF_V_SPACING)
                points.append({'point':[x, y, z]})

    return points

def main():
    points = shelves()
    print(json.dumps(points, indent=2))

if __name__=='__main__':
    main()
