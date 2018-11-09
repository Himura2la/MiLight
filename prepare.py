#!/usr/bin/python3

import lib.mci.bridges as bridges
import lib.mci.bulbs as bulbs

bridges = bridges.DiscoverBridge().discover()
if len(bridges) != 1:
    print('No bridge')
    exit()

all = bulbs.ColorGroup(bridges[0][0], 8899)
first = bulbs.ColorGroup(bridges[0][0], 8899, group_number=1)
second = bulbs.ColorGroup(bridges[0][0], 8899, group_number=2)

all.white()
all.brightness(0)
all.color(155)
all.brightness(0)
all.off()

