import math
from filefifo import Filefifo
from machine import I2C, Pin
from ssd1306 import SSD1306_I2C
  
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

fs = 250  

start_button = Pin(8, Pin.IN, Pin.PULL_UP)

fifo = Filefifo(10, name='sinewave_250Hz_03.txt')

data_list = []
for _ in range(1000):
    if fifo.has_data():
        data_list.append(fifo.get())
        

def find_frequency(data_list, sampling_rate):
    
    data = data_list
    num_samples = len(data)

    t = 1.0 / sampling_rate
    sample_times = []
    for i in range(num_samples):
        sample_times.append(i * t)
    
    min_val = min(data)
    max_val = max(data)
            
    threshold = (min_val + max_val) // 2

    rising_edges = []
    
    for i in range(1, num_samples):
        if data[i-1] < threshold and data[i] >= threshold:
            rising_edges.append(i)
            
    num_crossings = len(rising_edges)
    
    time_first_crossing = sample_times[rising_edges[0]]
    time_last_crossing = sample_times[rising_edges[-1]]
    
    num_periods_measured = num_crossings - 1
    
    total_time_span = time_last_crossing - time_first_crossing
    
    calculated_frequency = num_periods_measured / total_time_span
    
    print(f"Freq: {calculated_frequency:.4f} Hz")
    
    return calculated_frequency


oled.fill(0)
oled.text("Task 2.3", 0, 0, 1)
oled.text("press SW1", 0, 8, 1)
oled.show()

while True:
    if not start_button.value():
        oled.fill(0)
        
        frequency = find_frequency(data_list, fs)
        
        oled.text(f"Freq: {frequency:.4f}Hz", 0, 0, 1)
        oled.show()