from machine import Pin, SPI
import st7789 as st
import font

tft = st.ST7789(
    SPI(1, baudrate=30000000, sck=Pin(18), mosi=Pin(19)),
    135, 240,
    reset=Pin(23, Pin.OUT),
    cs=Pin(5, Pin.OUT),
    dc=Pin(16, Pin.OUT),
    backlight=Pin(4, Pin.OUT),
    rotation=3)
tft.init()


def tft_boot():
    tft.fill(st.RED)
    tft.text(font, "Boot", 0, tft.height() - 16, st.WHITE, 0)  # Boot text on screen


def tft_micrologo():
    tft.fill(0)
    tft.jpg('logo.jpg', 0, 0, 1)
    tft.text(
        font,
        " MICROPYTHON ",
        int(tft.width() / 2 - 105), int(tft.height() - 18),
        st.color565(255, 255, 255),
        st.color565(1, 1, 1)
    )
