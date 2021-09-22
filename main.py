import _thread as thread
from os import statvfs
import framebuf
import machine
from machine import Pin, I2C, ADC, PWM
import dht
import time
import ssd1306
import esp32
import gc
# Custom imports
from boot import ap


# =============== Init Variables =============== #
# Init Screen ------------------------
i2c = I2C(-1, scl=Pin(22), sda=Pin(21))  # Set Pins
oled_width = int(128)  # Width of OLED
oled_height = int(64)  # Length of OLED
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
# ------------------------------------

d = dht.DHT11(machine.Pin(4, machine.Pin.PULL_UP))
btn = Pin(0, Pin.IN)
led = Pin(2, Pin.OUT)
adc = ADC(Pin(35))

stop_threads = False
ScreenSelect = int(0)
stop = 0

f = int(0)

# ============================================== #


def deep_sleep():
    # pylint: disable=unexpected-arg
    # put the device to sleep for 10 seconds
    oled.contrast(0)
    machine.deepsleep(10000)


def sound():
    pwm0 = PWM(Pin(15))
    pwm0.freq(1567.98)
    pwm0.duty(512)


def blink():
    while True:
        led.on()
        time.sleep_ms(100)
        led.off()
        time.sleep_ms(1000)
        global stop_threads
        if stop_threads:
            thread.exit()


def get_dht11():  # get sensor info
    while True:

        global stop_threads
        if stop_threads:
            thread.exit()

        try:
            # Get sensor readings
            d.measure()
            gett = d.temperature()
            geth = d.humidity()

            # Convert celsius to fahrenheit
            ctf = (gett * 9 / 5) + 32 - 4 # -4 was calibration for my sensor
            TT = ctf
            HH = geth
            time.sleep_ms(1000)
            return HH, TT

        except OSError as e:
            oled.fill(0)
            oled.text_long("Error", "Failed to", "read sensor", "", "", "")
            oled.show()
            # thread.exit()
            return "Failed to read sensor."

# ========== Screens ========= #

# screen 0 ---------
def scralarm():
    var = str(adc.read())

    oled.fill(0)
    oled.menu_pix(0)
    oled.text_long("Screen", "Alarm_1 = ", var, "", "", "")
    oled.show()


# screen 1 ---------
def display_dht11():
    HH, TT = get_dht11()
    print("temp: " + str(TT))
    print("Humi: " + str(HH))
    print("")
    oled.fill(0)
    oled.menu_pix(1)
    oled.text_long("Sensor", "Temp = {0:0.1f}F".format(TT), "Humidity = {0:0.0f}%".format(HH), "", "", "")
    oled.show()


# screen 2 ---------
def info():  # Get and display Info # SCREEN 2
    if ap.active():
        ip = str(ap.ifconfig()[0])
    else:
        ip = "Wifi Off"

    mfreq = str(machine.freq())
    raw = str(esp32.raw_temperature())

    oled.fill(0)
    oled.menu_pix(2)
    oled.text_long("Info", ip, "CPU temp = " + raw + "F", "", mfreq, "", )
    oled.show()
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

    oled.fill(0)
    oled.menu_pix(3)
    oled.text_long("Space(MB)", "Curr: " + freestr, "", "Old:  " + "1.949219", "", "")
    oled.show()
    gc.collect()


# screen 4 ---------
def draw_shapes():  # Test draw screen
    oled.fill(0)
    oled.menu_pix(4)
    oled.text("Draw", 0, 0)  # Set some text
    # oled.fill_rect(15, 15, 44, 44, 1)
    # oled.rect(10, 10, 40, 40, 1)
    # oled.line(0,0,64,64,1)
    # oled.triangle(10, 10, 55, 20, 5, 40, 1)
    # oled.circle(64, 32, 10, 1)
    oled.round_rect(20, 20, 30, 30, 3, 1)
    oled.show()


# screen 5 ---------
def showlogo():
    fb_smile1 = framebuf.FrameBuffer(bytearray(b'\x00~\x00\x03\xff\xc0\x07\x81\xe0\x1e\x00x8\x00\x1c0\x00\x0c`\x00\x0ea\xc3\x86\xe0\x00\x07\xc0\x00\x03\xc0\x00\x03\xc0\x00\x02\xc0\x00\x03\xc0\x00\x03\xe0B\x07`<\x06`\x00\x060\x00\x0c8\x00\x1c\x1e\x00x\x07\x81\xe0\x03\xff\xc0\x00\xff\x00'), 24, 23, framebuf.MONO_HLSB)

    oled.fill(0)
    oled.framebuf.blit(fb_smile1, 0, 20)
    oled.text("Logo", 0, 0)
    oled.text("Hello", 30, 23)
    oled.text("MicroPython", 30, 33)
    oled.menu_pix(5)
    oled.show()


# =========================== #


# ------------------------------------ #

def my_func(self):  # push button tests
    global stop_threads
    global ScreenSelect

    # stop_threads = True
    led.on()
    ScreenSelect += 1
    led.off()

    print(ScreenSelect)


# ------------------------------------ #

# ttt = thread.start_new_thread(test, ())
# bbb = thread.start_new_thread(blink, ())
thread.start_new_thread(get_dht11, ())

# Boot up flash!
oled.fill(1)
oled.show()
time.sleep_ms(1000)





# ------------ Main Loop ------------- #
while True:
    btn.irq(my_func, Pin.IRQ_RISING)

# -------------------

    if ScreenSelect > 5:
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
