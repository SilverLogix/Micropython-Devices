# ---------- #


import _thread as thread
import gc
import utime
# noinspection PyUnresolvedReferences
from machine import Pin

# Custom imports
import st7789
from board import AP
import debug

# =============== Init Board =============== #
gc.enable()

btn0 = Pin(0,  Pin.IN)
btn1 = Pin(35, Pin.IN)
led  = Pin(2,  Pin.OUT)

# noinspection PyArgumentList
machine.freq(240000000)
debug.pprint()

oled = st7789.ST7789(SPI(1, baudrate=40000000, phase=0, polarity=1), 240, 240, reset=machine.Pin(5, machine.Pin.OUT), dc=machine.Pin(2, machine.Pin.OUT))

gc.collect()

# ============================================== #


# ---------- Definitions ---------- #

def deep_sleep(ms):
    machine.deepsleep(ms)   # put the device to sleep for 10 seconds


def sleep_5sec():
    while True:
        # gc.collect()
        mem = gc.mem_free()

        oled.text_long("Online", "", str(mem), "", "", "", "", iplist, oled.WHITE, oled.BLACK)

        utime.sleep(5)


"""

BLANK SPACE

"""

# ---------- Boot up ---------- #
oled.fill(oled.YELLOW)
# oled.text_long("", "", "", "", "", "", " Connecting to", " WiFi", oled.BLACK, oled.YELLOW)
# ifinfo = STA("ROUTER", "PASS")
ifinfo = AP("TTGO", 2, "pass")
print("")

iplist = str(ifinfo.ifconfig()[0])


oled.fill(oled.RED)
utime.sleep_ms(30)
oled.fill(oled.GREEN)
utime.sleep_ms(30)
oled.fill(oled.WHITE)
utime.sleep_ms(30)
oled.fill(oled.BLACK)
oled.text_long("Online", "", "", "", "", "", "", iplist, oled.WHITE, oled.BLACK)


# ========== RUN ========== #

thread.start_new_thread(sleep_5sec, ())
