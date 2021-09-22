from machine import Pin, PWM
import time
from notes import *

pwm0 = PWM(Pin(15))
ii = 0
pwm0.duty(512)

songOfStromArray = [D4, F4, D5, D4, F4, D5, E5, F5, E5, F5, E5, C5, A4, A4, D4, F4, G4, A4, A4, D4, F4, G4, E4]
songOfStormDelay = [X2, X1, X6, X2, X1, X6, X5, X1, X1, X1, X1, X1, X6, X2, X2, X1, X1, X6, X2, X3, X1, X2, X7]

for i in songOfStromArray:
    pwm0.freq(int(i))
    time.sleep(songOfStormDelay[ii])
    ii = ii + 1
else:
    pwm0.deinit()

'''
song = {
    'note': [1, 2, 3], 
    'dura': [2, 4, 3]
        }
'''
