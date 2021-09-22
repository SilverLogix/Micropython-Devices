from machine import Pin, I2C
import ssd1306
import framebuf

# ESP32 Pin assignment
i2c = I2C(-1, scl=Pin(22), sda=Pin(21))

oled_width = int(128)
oled_height = int(64)

oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

def showlogo():
    fb_smile1 = framebuf.FrameBuffer(bytearray(b'\x00~\x00\x03\xff\xc0\x07\x81\xe0\x1e\x00x8\x00\x1c0\x00\x0c`\x00\x0ea\xc3\x86\xe0\x00\x07\xc0\x00\x03\xc0\x00\x03\xc0\x00\x02\xc0\x00\x03\xc0\x00\x03\xe0B\x07`<\x06`\x00\x060\x00\x0c8\x00\x1c\x1e\x00x\x07\x81\xe0\x03\xff\xc0\x00\xff\x00'), 24, 23, framebuf.MONO_HLSB)

    oled.fill(0)
    oled.framebuf.blit(fb_smile1, 0, 20)
    oled.text("Logo", 0, 0)
    oled.text("5", 120, 0)
    oled.text("Hello", 30, 23)
    oled.text("MicroPython", 30, 33)
    oled.show()