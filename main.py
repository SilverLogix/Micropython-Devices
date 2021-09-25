# ---------- #

from machine import Pin, SoftSPI
import gc
import utime
import random

# Custom imports
from debug import b_print
from debug import pro_and_mem
import st7789
import font


# noinspection PyArgumentList
machine.freq(240_000000)
b_print()

RS = Pin(23, Pin.OUT)
CS = Pin(5,  Pin.OUT)
DC = Pin(16, Pin.OUT)
BL = Pin(4,  Pin.OUT)


def oled_init():
    spi = SoftSPI(baudrate=800000000, polarity=1, sck=machine.Pin(18), mosi=machine.Pin(19), miso=Pin(13))
    oled = st7789.ST7789(spi, 135, 240, reset=RS, cs=CS, dc=DC, backlight=BL, rotation=0)
    return oled


tft = oled_init()
gc.collect()


@pro_and_mem
def flash_text():

    utime.sleep_ms(50)
    gc.collect()

    for rotation in range(4):
        tft.rotation(rotation)
        tft.fill(st7789.BLACK)
        col_max = tft.width - font.WIDTH * 6
        row_max = tft.height - font.HEIGHT

        for _ in range(50):
            tft.text(
                font,
                "Hello!",
                random.randint(0, col_max),
                random.randint(0, row_max),
                st7789.color565(
                    random.getrandbits(8),
                    random.getrandbits(8),
                    random.getrandbits(8)),
                st7789.color565(
                    random.getrandbits(8),
                    random.getrandbits(8),
                    random.getrandbits(8))
            )

# ----------------------------------------------------------- #


while True:
    flash_text()
