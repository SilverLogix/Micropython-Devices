import micropython
import machine
# noinspection PyUnresolvedReferences
from machine import Pin

# noinspection PyArgumentList
machine.freq(240000000)
micropython.alloc_emergency_exception_buf(100)

print(str('Booting...'))
