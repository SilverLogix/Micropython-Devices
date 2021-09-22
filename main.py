from os import statvfs
import machine
from machine import PWM
import dht
import esp32
import gc

# Custom imports
from gfx import *
import gfx
import board as bd
import debug
import uasyncio

# gwifi()
# bd.STA("SSID", "PASS")

# noinspection PyArgumentList
machine.freq(80000000)

debug.space_free()
debug.m_freq()
debug.raw_temp()
debug.showVoltage()

gc.collect()

# =============== Init Variables =============== #
d = dht.DHT11(machine.Pin(15, machine.Pin.PULL_UP))
btn = Pin(0, Pin.IN)

stop_threads = False
ScreenSelect = int(0)


# ============================================== #


def deep_sleep():
    # pylint: disable=unexpected-arg
    # put the device to sleep for 10 seconds
    # noinspection PyArgumentList
    machine.deepsleep(10000)


def l_sleep():
    # noinspection PyArgumentList
    machine.sleep(10000)


def sound():
    pwm0 = PWM(Pin(25))
    pwm0.freq(1567.98)
    pwm0.duty(512)


temp, humi = 0, 0
async def get_dht11():  # get sensor info
    global temp, humi
    while True:
        await uasyncio.sleep(2)
        d.measure()
        temp = d.temperature()
        humi = d.humidity()
        await uasyncio.sleep(9)

    # ========== Screens ========= #


# screen 0 ---------
def scralarm():
    gfx.text_long("Screen", "Alarm_1 = ", "var", "", "", "", "", "", st.WHITE, st.BLACK)


# screen 1 ---------
def display_dht11():
    global temp, humi
    tft.text(font, "Sensor", 0, 0, st.YELLOW, st.BLACK)
    # Convert celsius to fahrenheit
    ctf = (temp * 9 / 5) + 32 - 4  # -4 was calibration for my sensor
    gfx.text_long("Sensor", "", "Temp = {0:0.1f}F".format(ctf), "Humidity = {0:0.0f}%".format(humi), "", "", "", "",
                  st.WHITE, st.BLACK)


# screen 2 ---------
def info():  # Get and display Info # SCREEN 2

    ip = "Wifi Off"

    mfreq = str(machine.freq())
    raw = str(esp32.raw_temperature())

    gfx.text_long("Info", ip, "CPU temp = " + raw + "F", " ", mfreq, " ", " ", " ", st.WHITE, st.BLACK)
    gc.collect()


# screen 3 ---------
def dfree():  # Display remaining free space # SCREEN 3
    # am = str(alarmc1)

    bits = statvfs('/flash')
    # print(str(bits))
    blksize = bits[0]  # 4096
    blkfree = bits[3]  # 12
    freesize = blksize * blkfree  # 49152
    mbcalc = 1024 * 1024  # 1048576
    mbfree = freesize / mbcalc  # 0.046875
    freestr = str(mbfree)

    gfx.text_long("Space(MB)", "Curr: " + freestr, "", "Old:  " + "1.949219", "", "", "", "", st.WHITE, st.BLACK)
    gc.collect()


# screen 4 ---------
def draw_shapes():  # Test draw screen
    pass
    # tft.text("Draw", 0, 0)  # Set some text
    # oled.fill_rect(15, 15, 44, 44, 1)
    # oled.rect(10, 10, 40, 40, 1)
    # oled.line(0,0,64,64,1)
    # oled.triangle(10, 10, 55, 20, 5, 40, 1)
    # oled.circle(64, 32, 10, 1)
    # oled.round_rect(20, 20, 30, 30, 3, 1)


# screen 5 ---------
def showlogo():
    pass
    # tft.text("Logo", 0, 0)
    # tft.text("Hello", 30, 23)
    # tft.text("MicroPython", 30, 33)


# =========================== #


# ------------------------------------ #

def my_func(self):  # push button tests
    global ScreenSelect

    gfx.wipe(st.BLACK)
    ScreenSelect += 1
    print(ScreenSelect)
    gfx.wipe(st.BLACK)


async def sleep_7sec():
    while True:
        print('sleep 7 seconds')
        await uasyncio.sleep(7)


async def show_screens():
    global ScreenSelect
    while True:
        btn.irq(my_func, Pin.IRQ_RISING)

        # -------------------

        if ScreenSelect > 5:
            gfx.wipe(st.BLACK)
            gc.collect()
            ScreenSelect = 0

        if ScreenSelect == 0:
            scralarm()

        if ScreenSelect == 1:
            display_dht11()

        if ScreenSelect == 2:
            info()

        if ScreenSelect == 3:
            dfree()

        if ScreenSelect == 4:
            draw_shapes()

        if ScreenSelect == 5:
            showlogo()

        await uasyncio.sleep_ms(300)

# ------------------------------------ #

# ttt = thread.start_new_thread(test, ())
# bbb = thread.start_new_thread(blink, ())
# thread.start_new_thread(get_dht11, ())

tft.fill(st.BLACK)

loop = uasyncio.get_event_loop()

loop.create_task(show_screens())
loop.create_task(get_dht11())  # schedule asap
loop.create_task(sleep_7sec())

loop.run_forever()

# ------------ Main Loop ------------- #
