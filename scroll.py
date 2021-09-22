from machine import Pin, I2C
import ssd1306
import time

# ESP32 Pin assignment
i2c = I2C(-1, scl=Pin(22), sda=Pin(21))

oled_width = int(128)
oled_height = int(64)

oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

while True:
    oled.text("Hello World!", 0, 0)
    for i in range(0, 164):
        oled.scroll(1,0)
        oled.show()
        time.sleep(0.01)
