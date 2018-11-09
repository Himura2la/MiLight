#!/usr/bin/python3

from time import sleep
from sys import argv

import lib.mci.bridges as bridges
import lib.mci.bulbs as bulbs

milight_controller_ip = '192.168.1.6'
all = bulbs.ColorGroup(milight_controller_ip, 8899)
first = bulbs.ColorGroup(milight_controller_ip, 8899, group_number=1)
second = bulbs.ColorGroup(milight_controller_ip, 8899, group_number=2)


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


def sunrise_prepare():
    all.brightness(0)
    second.color(155)
    second.brightness(0)
    all.off()


def sunrise(stage):
    if stage == 0:
        sunrise_prepare()
    elif stage == 1:
        night_mode(1)
    elif stage == 2:
        night_mode(2)
    elif stage == 3:
        first.color(155)
        first.brightness(0)
    elif stage == 4:
        second.color(155)
        second.brightness(0)
    elif stage == 5:
        second.white()
        all.brightness(0)
    elif 5 < stage < 27:
        brightness = (stage - 5)
        all.brightness(brightness)
    elif stage >= 27:
        all.white()
        all.brightness(21)

k = float(argv[1]) if len(argv) > 1 else 1

for i in range(1,6):
    sunrise(i)
    sleep(k*3*60)

for i in range(6,28):
    sunrise(i)
    sleep(k*60)

