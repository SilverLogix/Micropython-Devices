# ---------- #


import machine
import micropython

# noinspection PyArgumentList
machine.freq(240_000000)
micropython.alloc_emergency_exception_buf(100)


print(f"\n Booting... \n")
