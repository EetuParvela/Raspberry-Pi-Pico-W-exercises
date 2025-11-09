import time
from machine import UART, Pin, I2C, Timer, ADC
from ssd1306 import SSD1306_I2C

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)

oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

text_pos_x = 0
text_pos_y = 0

while True:
    user_input = input("Input: ")
    oled.text(user_input, text_pos_x, text_pos_y, 1)
    oled.show()
    
    text_pos_y += 8
    
    if text_pos_y > oled_height - 8:
        oled.scroll(0, -8)
        oled.fill_rect(0, 56, 128, 8, 0)
        text_pos_y = 56
        
    time.sleep(0.05)