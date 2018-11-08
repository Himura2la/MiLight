from machine import Pin, idle, reset
from time import time, sleep_ms
import esp
import usocket

from network import WLAN, STA_IF
WCRED = 'SSID', 'PASSWORD'
STA=WLAN(STA_IF);STA.active(1);STA.connect(*WCRED)

esp.sleep_type(esp.SLEEP_LIGHT)
led = Pin(5, Pin.OUT)
led.off()
button = Pin(4, Pin.IN)
button_state_prev = button.value()
button_state_now = button_state_prev

milight_controller_ip = '192.168.1.6'
s = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)
bulbs_on = False

def milight_cmd(cmd, val=b'\x00'):
    s.send(cmd + val + b'\x55')

all_off = b'\x41'
all_on = b'\x42'
all_white = b'\xc2'
brightness = b'\x4e'
color = b'\x40'

def light_sleep(n):
    for _ in range(n):
        idle()

def flash(times=2):
    print('Flashing %d times' % times)
    for i in range(times + 1):
        led.off()  # actually on
        sleep_ms(50)
        led.on()  # actually off
        sleep_ms(50)

def button_pressed():
    global bulbs_on
    print('bulbs -> ' + ('off' if bulbs_on else 'on'))
    if bulbs_on:
        for _ in range(2):
            milight_cmd(all_off)
            idle()
        bulbs_on = False
    else:
        for _ in range(2):
            milight_cmd(all_on)
            sleep_ms(100)
            milight_cmd(all_white)
            sleep_ms(10)
            milight_cmd(all_on)
            sleep_ms(100)
            milight_cmd(brightness, '\x16')
            idle()
        bulbs_on = True

def button_long_pressed():
    print('bulbs -> sunset')
    milight_cmd(all_on)
    sleep_ms(100)
    milight_cmd(brightness, '\x02')
    sleep_ms(100)
    milight_cmd(all_off)
    bulbs_on = False

while True:
    led.off()
    if not STA.isconnected():
        print("Connecting to Wi-Fi...")
        connection_failed_time = time() + 10
        STA.connect(*WIFI_SSID_PASSWORD)
    while not STA.isconnected() and time() < connection_failed_time:
        sleep_ms(10)
    if not STA.isconnected():
        print("Connection FAILED! Going to sleep...")
        light_sleep(1000)
        continue
    print("Connected!")
    flash(3)
    s.connect(usocket.getaddrinfo(milight_controller_ip, 8899)[0][-1])
    long_press_time = 0
    while True:
        try:
            button_state_prev = button_state_now
            button_state_now = button.value()

            # Falling edge detection
            if button_state_prev == 1 and button_state_now == 0:
                button_pressed()

            if button_state_now == 0:
                long_press_time += 1
            if long_press_time > 30:
                long_press_time = 0
                button_long_pressed()

            sleep_ms(100)

        except Exception as e:
            print("%s: %s" % (type(e).__name__, e))
            break
