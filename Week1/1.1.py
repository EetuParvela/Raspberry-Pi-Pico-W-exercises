import time
from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C

button_left = Pin(7, Pin.IN, Pin.PULL_UP)
button_right = Pin(9, Pin.IN, Pin.PULL_UP)

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)

oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

ufo = "<=>"
ufo_width = 24
ufo_x = 0
ufo_y = oled_height - 8
ufo_speed = 8

while True:
    
    if not button_left.value():
        ufo_x -= ufo_speed
    elif not button_right.value():
        ufo_x += ufo_speed
        
    if ufo_x < 0:
        ufo_x = 0
    elif ufo_x + ufo_width > oled_width:
        ufo_x = oled_width - ufo_width
        
    oled.fill(0)
    oled.text(ufo, ufo_x, ufo_y, 1)
    oled.show()
    
    time.sleep(0.05) 
    