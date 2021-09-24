# ---------- #


from machine import Pin, SoftSPI
import random
import st7789
import font
import utime
import gc


def time_acc_function(f, *args, **kwargs):
    ncalls = 0
    ttime = 0.0

    def new_func(*args, **kwargs):
        nonlocal ncalls, ttime
        t = utime.ticks_us()
        result = f(*args, **kwargs)
        delta = utime.ticks_diff(utime.ticks_us(), t)
        ncalls += 1
        ttime += delta
        print('Function: {} Call count = {} Total time = {:6.3f}ms'.format(f.__name__, ncalls, ttime/1000))
        return result
    return new_func


print("ready")


@time_acc_function
def main():
    spi = SoftSPI(baudrate=800000000, polarity=1, sck=machine.Pin(18), mosi=machine.Pin(19), miso=Pin(13))
    oled = st7789.ST7789(
        spi,
        135,
        240,
        reset=Pin(23, Pin.OUT),
        cs=Pin(5, Pin.OUT),
        dc=Pin(16, Pin.OUT),
        backlight=Pin(4, Pin.OUT),
        rotation=0)
    return oled


def run():
    tft = main()
    print("GO")
    gc.collect()
    while True:
        for rotation in range(4):
            tft.rotation(rotation)
            tft.fill(st7789.BLACK)
            col_max = tft.width - font.WIDTH*6
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
