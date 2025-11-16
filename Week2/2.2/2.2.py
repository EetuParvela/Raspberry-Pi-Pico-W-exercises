from filefifo import Filefifo
from machine import I2C, Pin
from ssd1306 import SSD1306_I2C
import time

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

start_button = Pin(8, Pin.IN, Pin.PULL_UP)

fifo = Filefifo(10, name='sinewave_250Hz_02.txt')

data_list = []
for _ in range(2500):
    if fifo.has_data():
        data_list.append(fifo.get())


def scale_values(data):
    
    min_val = min(data)
    max_val = max(data)
    new_val = 0
    new_values = []
    
    for i in data:
        new_val = round((i - min_val) * (100 / (max_val - min_val)))
        new_values.append(new_val)
        
    return new_values


oled.fill(0)
oled.text("Task 2.2", 0, 0, 1)
oled.text("press SW1", 0, 8, 1)
oled.show()

while True:
    if not start_button.value():
        oled.fill(0)
        
        values = scale_values(data_list)
        text_pos_y = 64
        text_pos_x = 0
        
        for i in values:
            
            text_pos_y -= 8
            
            oled.text(f"{i}", text_pos_x, text_pos_y, 1)
            oled.hline(24, text_pos_y + 4, i, 1)
            oled.show()
            
            if text_pos_y < oled_height - 8:
                oled.scroll(0, -8)
                oled.fill_rect(0, 56, 128, 8, 0)
                text_pos_y = 56
