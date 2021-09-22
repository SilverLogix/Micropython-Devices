import micropython
import gc
import machine
import gfx
import webrepl
from utime import sleep_ms


# DO NOT GO BELOW 80Mhz!!!  Will break wifi and complicate serial!
# noinspection PyArgumentList
machine.freq(240000000)
sleep_ms(100)

micropython.alloc_emergency_exception_buf(100)
print('Booting...')

gfx.boot()

webrepl.start(password="password")

gc.enable()
gc.collect()
