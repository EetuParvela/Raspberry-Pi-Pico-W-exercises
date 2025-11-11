from filefifo import Filefifo
from machine import I2C, Pin
from ssd1306 import SSD1306_I2C

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

start_button = Pin(8, Pin.IN, Pin.PULL_UP)

fifo = Filefifo(10, name='sinewave_250Hz_01.txt')

t = 0.004  

data_list = []
for _ in range(1000):
    if fifo.has_data():
        data_list.append(fifo.get())


def get_peaks(data):
    peaks = []
    indexes = []
    derivative = [data[i] - data[i - 1] for i in range(1, len(data))]

    for i in range(1, len(derivative)):
        if derivative[i - 1] > 0 and derivative[i] <= 0:
            indexes.append(i)
            peaks.append(data[i])
    return peaks, indexes


def get_peak_to_peak_data(indexes, t):
    samples = []
    seconds = []
    frequencys = []

    for i in range(1, len(indexes)):
        s = indexes[i] - indexes[i - 1]
        samples.append(s)
        sec = s * t
        seconds.append(sec)
        frequencys.append(1 / sec)

    avg_frequency = sum(frequencys) / len(frequencys)
    return samples, seconds, frequencys, avg_frequency



oled.fill(0)
oled.text("Task 2.1", 0, 0, 1)
oled.text("press SW1", 0, 8, 1)
oled.show()

while True:
    if not start_button.value():
        oled.fill(0)
        
        peaks, indexes = get_peaks(data_list)
        samples, seconds, frequencys, avg_frequency = get_peak_to_peak_data(indexes, t)
        
        
        for i in range(0, len(samples)):
            ms = seconds[i] * 1000
            oled.text(f"{i+1})int:{samples[i]}-{ms:.0f}ms", 0, i * 10)

        oled.text(f"Freq: {avg_frequency:.4f}Hz", 0, 54)
        oled.show()
