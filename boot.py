# ---------- #


import machine
import micropython

# noinspection PyArgumentList
machine.freq(240000000)
micropython.alloc_emergency_exception_buf(100)

print("\n" * 5)
print(str('Booting...'))
