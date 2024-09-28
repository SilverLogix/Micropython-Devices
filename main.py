# import ftp
import gc
import wifi
import gfx
import utime
import _thread


N = 200_000
M = 9999
C = 0
T = 0


gfx.fill(gfx.BLUE)

gc.enable()

wifi.kill_all(False)
wifi.access_point('ttgo', 'password')

# ftp.FtpTiny().start()

utime.sleep_ms(1000)
gfx.fill(gfx.BLACK)


def test(n):
    sum1 = 0
    for i in range(n):
        sum1 += i
    return sum1
# debug.time_it(test, N)


def counter():
    global C
    count = 0
    while True:
        count = count + 1

        C = f"{count} "
        utime.sleep_ms(50)


def show_mem():
    while True:
        global M
        mem = gc.mem_free()
        M = f"{mem}    "
        utime.sleep_ms(2000)


def text_roll():
    global T
    while True:
        if T >= 256:
            T = 0
        else:
            T = T + 1
            utime.sleep_ms(1000)


def screen_update():
    while True:
        gfx.text(C, 0, 0, gfx.WHITE, gfx.BLACK)
        gfx.text(T, 0, 18, gfx.WHITE, gfx.BLACK)

        gfx.text(M, 0, 114, gfx.YELLOW, gfx.BLACK)


gfx.backlight(64)
_thread.stack_size(16) # noqa
_thread.start_new_thread(counter, ()) # noqa
_thread.start_new_thread(show_mem, ()) # noqa
_thread.start_new_thread(text_roll, ()) # noqa

_thread.stack_size(64) # noqa
_thread.start_new_thread(screen_update, ()) # noqa
