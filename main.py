import time

import lib.mci.bridges as bridges
import lib.mci.bulbs as bulbs

bridges = bridges.DiscoverBridge().discover()
if len(bridges) != 1:
    print('No bridge')
    exit()

all = bulbs.ColorGroup(bridges[0][0], 8899)
first = bulbs.ColorGroup(bridges[0][0], 8899, group_number=1)
second = bulbs.ColorGroup(bridges[0][0], 8899, group_number=2)


def night_mode(group_number=None):
    if not group_number:
        all.send_command(b"\x41")
        all.send_command(b"\xC1")
    else:
        all.send_command((0x44 + group_number * 2).to_bytes(1, byteorder='big'))
        all.send_command((0xC4 + group_number * 2).to_bytes(1, byteorder='big'))


def basic_light():
    all.on()
    all.white()
    all.brightness(21)


def sunrise(stage):
    if stage == 0:  # preparation, flashes
        all.brightness(0)
        second.color(155)
        second.brightness(0)
        all.off()
    elif stage == 1:
        night_mode(1)
    elif stage == 2:
        night_mode(2)
    elif stage == 3:
        first.brightness(0)
    elif stage == 4:
        second.brightness(0)
    elif stage == 5:
        all.brightness(1)
        second.color(155)
    elif 5 < stage < 27:
        brightness = (stage - 5)
        all.brightness(brightness)
        print(stage, brightness)
    elif stage >= 27:
        second.white()
        all.brightness(21)
        print(stage, 'full')


for i in range(28):
    sunrise(i)
    time.sleep(1)