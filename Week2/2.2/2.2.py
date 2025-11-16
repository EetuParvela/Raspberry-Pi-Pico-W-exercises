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
