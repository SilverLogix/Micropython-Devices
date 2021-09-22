import time

from machine import Pin, PWM

from notes import *

pwm0 = PWM(Pin(15))
ii = 0

tetrisPlay = [E5, B4, C5, D5, C5, B4, A4, A4, C5, E5, D5, C5, B4, C5, D5, E5, C5, A4, A4, A4, B4, C5, D5, F5, A5, G5,
              F5, E5, C5, E5, D5, C5, B4, B4, C5, D5, E5, C5, A4, A4, R, E5, B4, C5, D5, C5, B4, A4, A4, C5, E5, D5, C5,
              B4, C5, D5, E5, C5, A4, A4, A4, B4, C5, D5, F5, A5, G5, F5, E5, C5, E5, D5, C5, B4, B4, C5, D5, E5, C5,
              A4, A4, R, E5, C5, D5, B4, C5, A4, GS4, B4, R, E5, C5, D5, B4, C5, E5, A5, GS5]

tetrisDelay = [X3, X1, X1, X3, X1, X1, X3, X1, X1, X3, X1, X1, X5, X1, X3, X3, X3, X3, X1, X3, X1, X1, X5, X1, X3, X1,
               X1, X5, X1, X3, X1, X1, X3, X1, X1, X3, X3, X3, X3, X3, X3, X3, X1, X1, X3, X1, X1, X3, X1, X1, X3, X1,
               X1, X5, X1, X3, X3, X3, X3, X1, X3, X1, X1, X5, X1, X3, X1, X1, X5, X1, X3, X1, X1, X3, X1, X1, X3, X3,
               X3, X3, X3, X3, X4, X4, X4, X4, X4, X4, X4, X3, X1, X4, X4, X4, X4, X3, X3, X4, X4]

for i in tetrisPlay:
    pwm0.freq(int(i))
    time.sleep(tetrisDelay[ii])
    ii = ii + 1
    # time.sleep(0.2)
else:
    pwm0.deinit()
