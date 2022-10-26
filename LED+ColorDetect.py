from machine import Pin
from machine import I2C
from machine import PWM
from time import sleep_ms
from tcs34725 import TCS34725
import array, time
from machine import Pin
from time import sleep

sensor = I2C(0, sda=Pin(12), scl=Pin(13))
tcs = TCS34725(sensor)
NUM_LEDS = 4
PIN_NUM = 28
brightness = 1


@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)

def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1).side(0)[2]
    jmp(not_x, "do_zero").side(1)[1]
    jmp("bitloop").side(1)[4]
    label("do_zero")
    nop().side(0)[4]

sm = rp2.StateMachine(0, ws2812, freq=8000000, sideset_base=Pin(PIN_NUM))

sm.active(1)

ar = array.array("I", [0 for _ in range(NUM_LEDS)])

ar = array.array("I", [0 for _ in range(NUM_LEDS)])

def pixels_set(i, color):
    ar[i] = (color[1]<<16) + (color[0]<<8) + color[2] #色馬數值16移動位元和移動8位元，因為每個顏色色馬共24位元#

BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
COLORS = (BLACK, RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, WHITE)

def pixels_show(br):
    dimmer_ar = array.array("I", [0 for _ in range(NUM_LEDS)])
    for i,c in enumerate(ar):  #enumerate
        r = int(((c >> 8) & 0xFF) * br)
        g = int(((c >> 16) & 0xFF) * br)
        b = int((c & 0xFF) * br)
        dimmer_ar[i] = (g<<16) + (r<<8) + b
    sm.put(dimmer_ar, 8)
    time.sleep_ms(10)

while True:
    print(tcs.read('dec'))
    print(tcs.read('raw'))
    for i in range(NUM_LEDS):
        pixels_set(i, RED)
        pixels_show(0.01) #show是亮光強度#
        time.sleep(0.1)
    for i in range(NUM_LEDS):
        pixels_set(i, YELLOW)
        pixels_show(0.01) 
        time.sleep(0.1)
    pixels_set(0, GREEN)#0是燈的代號，第0號燈#
    pixels_show(0.1)
    pixels_set(1, CYAN)#1是燈的代號，第1號燈#
    pixels_show(0.01)
    pixels_set(2, BLUE)
    pixels_show(0.01) 
    sleep(0.01)
    time.sleep(1)