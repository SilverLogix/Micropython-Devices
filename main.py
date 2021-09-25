# ---------- #


from machine import Pin, SoftSPI
import random
# import gc

# Custom imports
import st7789
import font
import debug
from debug import profile
from debug import serial_mem

RS = Pin(23, Pin.OUT)
CS = Pin(5,  Pin.OUT)
DC = Pin(16, Pin.OUT)
BL = Pin(4,  Pin.OUT)

# noinspection PyArgumentList
machine.freq(160000000)
debug.pprint()


print("ready\n")


@profile
def oled_init():
    spi = SoftSPI(baudrate=800000000, polarity=1, sck=machine.Pin(18), mosi=machine.Pin(19), miso=Pin(13))
    oled = st7789.ST7789(spi, 135, 240, reset=RS, cs=CS, dc=DC, backlight=BL, rotation=0)
    return oled


def run():
    tft = oled_init()
    print("GO\n")

    while True:
        for rotation in range(4):
            # gc.collect()
            serial_mem(False)
            print("\n" * 2)
            tft.rotation(rotation)
            tft.fill(st7789.BLACK)
            col_max = tft.width - font.WIDTH * 6
            row_max = tft.height - font.HEIGHT

            for _ in range(500):
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


run()
