import time
from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)

oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

button_down = Pin(9, Pin.IN, Pin.PULL_UP)
button_reset = Pin(8, Pin.IN, Pin.PULL_UP)
button_up = Pin(7, Pin.IN, Pin.PULL_UP)

x, y = 0, 32
color = 1

while True:
    if not button_reset.value():
        oled.fill(0)
        x, y = 0, 32
        
    else:
        dy = 0
        if not button_down.value():
            dy = 1
        elif not button_up.value():
            dy = -1
        
        y = max(0, min(63, y + dy))
        oled.pixel(x, y, color)
        oled.show()

        x += 1
        if x >= oled_width:
            x, y = 0, 32
            
    
        
        
        