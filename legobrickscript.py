# Example using PIO to drive a set of WS2812 LEDs.

import array, utime
from machine import Pin, ADC
import rp2
from ucollections import deque
#################### CONSTANTS ########################
# Configure the number of WS2812 LEDs.
NUM_LEDS = 8
PIN_NUM = 22
brightness = 0.2
AVGNUM = 100

################### VARIABLES #########################

#PINS
white_led = Pin(15, Pin.OUT)
sensor_in = ADC(26)

#MEASUREMENT
senval = 0
mean_sens = 0
min_sens = -1
max_sens = 0
percent = 0
nlights = 0

#FILTERING
dt = 0
t = 0
iavg = 0
avgsum = 0
filtsenval = 0

alpha = 10
tau = 200

#rolling average
NUM_MEASUREMENTS = 20
filtsenvals_list = deque((), NUM_MEASUREMENTS+1)
roll_sum = 0
rolled_avg = 0


@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()


# Create the StateMachine with the ws2812 program, outputting on pin
sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(PIN_NUM))

# Start the StateMachine, it will wait for data on its FIFO.
sm.active(1)

# Display a pattern on the LEDs via an array of LED RGB values.
ar = array.array("I", [0 for _ in range(NUM_LEDS)])

##########################################################################
def pixels_show():
    dimmer_ar = array.array("I", [0 for _ in range(NUM_LEDS)])
    for i,c in enumerate(ar):
        r = int(((c >> 8) & 0xFF) * brightness)
        g = int(((c >> 16) & 0xFF) * brightness)
        b = int((c & 0xFF) * brightness)
        dimmer_ar[i] = (g<<16) + (r<<8) + b
    sm.put(dimmer_ar, 8)
    utime.sleep_ms(10)

def pixels_set(i, color):
    ar[i] = (color[1]<<16) + (color[0]<<8) + color[2]

def pixels_fill(color):
    for i in range(len(ar)):
        pixels_set(i, color)

def pixels_fill_partial(count, color):
    for i in range(count):
        pixels_set(i, color)
    for i in range(count, len(ar)):
        pixels_set(i, BLACK)
    pixels_show()    

def color_chase(color, wait):
    for i in range(NUM_LEDS):
        pixels_set(i, color)
        utime.sleep(wait)
        pixels_show()
    utime.sleep(0.2)

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(NUM_LEDS):
            rc_index = (i * 256 // NUM_LEDS) + j
            pixels_set(i, wheel(rc_index & 255))
        pixels_show()
        utime.sleep(wait)

BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
COLORS = (BLACK, RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, WHITE)

# print("fills")
# for color in COLORS:
#     pixels_fill(color)
#     pixels_show()
#     time.sleep(0.2)
# 
# print("chases")
# for color in COLORS:
#     color_chase(color, 0.01)
# 
# print("rainbow")
# rainbow_cycle(0)
#

def raise_error():
    for x in range(10):
        print('error detected!')
        color_chase(PURPLE, 0.1)
        color_chase(BLACK, 0.1)
        
def init_sensor_unit():
    print('initializing sensor...')
    low_values = []
    high_values = []
    for x in range(3):
    
        white_led.value(0)
        utime.sleep(0.5)
        low_values.append(sensor_in.read_u16())
        white_led.value(1)
        utime.sleep(0.5)
        high_values.append(sensor_in.read_u16())
    
    #test to see if bad sensor plugs
    for x,y in zip(low_values, high_values):
        if x > 20000 or y < 20000:
            raise_error()            

def read_baseline():
    global mean_sens
    global senval
    global min_sens
    global max_sens
    
    start_time = utime.ticks_ms()
    counter = 0
    while (utime.ticks_ms() - start_time) < 3000:
        counter += 1
        senval = sensor_in.read_u16()
        mean_sens = (mean_sens * counter + senval)/(counter + 1)
        
        
        if min_sens > senval or min_sens == -1:
            min_sens = senval
        if max_sens < senval:
            max_sens = senval
            
        utime.sleep_ms(50)
        print("calibrating mean:", mean_sens, "current min:", min_sens, "current max:", max_sens)
        current_time = utime.ticks_ms()
    
    range_sens = max_sens - min_sens
    min_sens = mean_sens
    max_sens = mean_sens + range_sens

rainbow_cycle(0)
color_chase(BLACK, 0.1)

#visuals to show if sensor unit is working correctly
color_chase(YELLOW, 0.1)
init_sensor_unit()
color_chase(BLACK, 0.1)

#turn on led
white_led.value(1)

# establish a generic min/max
color_chase(CYAN, 0.1)
read_baseline()
color_chase(BLACK, 0.1)


#main loop of program
while True:
    utime.sleep(0.1)
    dt = utime.ticks_ms() - t
    print(dt)
    t = utime.ticks_ms()
    
    #####   FILTERING    #####
    alpha = dt/(tau + dt)
    senval = sensor_in.read_u16()
    filtsenval = filtsenval + alpha * (senval-filtsenval)
    print('alpha:', alpha, 'senval', senval, 'filtsenval', filtsenval)
    
    if max_sens < filtsenval:
        print("new max found...")
        max_sens = filtsenval

    ####    ROLLED AVERAGE    ####
    filtsenvals_list.append(filtsenval)
    
    roll_sum += filtsenval
    if len(filtsenvals_list) == NUM_MEASUREMENTS+1:
        roll_sum -= filtsenvals_list.popleft()
    
        
        rolled_avg = roll_sum/NUM_MEASUREMENTS
        
        ####    LIGHT OUTPUT DETERMINATION    ####
        percent = round(100*(rolled_avg - min_sens)/(max_sens - min_sens))
        nlights = round(percent*NUM_LEDS/100)
        
        if nlights < 1:
            print("percent too low, overriding!")
            nlights = 1
            percent = 0
            
        if percent > 100:
            print("GREATER THAN 100, overriding! percent:", percent)
            percent = 100
            nlights = NUM_LEDS
        pixels_fill_partial(nlights, RED)
        print("%: ", percent, "nlights:", nlights, "senval:", senval, "fsenval:", filtsenval, "min:", min_sens, "max:", max_sens)    

    print('len:', len(filtsenvals_list), 'roll sum:', roll_sum, 'roll avg:', rolled_avg)
