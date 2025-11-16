from machine import I2C, Pin
from fifo import Fifo
from led import Led
from ssd1306 import SSD1306_I2C
import micropython
import time


i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

led_pins = [22, 21, 20]

micropython.alloc_emergency_exception_buf(200)


class Encoder:
    def __init__(self, rot_a, rot_b, rot_push):
        self.a = Pin(rot_a, Pin.IN)
        self.b = Pin(rot_b, Pin.IN)
        self.push = Pin(rot_push, Pin.IN, Pin.PULL_UP)
        self.last_push_time = 0
        self.fifo = Fifo(30, typecode='i')        

        self.a.irq(handler=self.rot_handler, trigger=Pin.IRQ_FALLING, hard=True)
        self.push.irq(handler=self.push_handler, trigger=Pin.IRQ_FALLING, hard=True)
        
    def rot_handler(self, pin):
        if self.b():                 
            self.fifo.put(1)         
        else:                        
            self.fifo.put(-1)        

    def push_handler(self, pin):
        current_time = time.ticks_ms()
        if current_time - self.last_push_time < 200:
            return
            
        self.last_push_time = current_time
        self.fifo.put(button_push)
        

def draw_menu():
    
    oled.fill(0)
    
    line_height = 16
    
    for i in range(len(leds)):
        led_status = "ON" if led_states[i] else "OFF"
        text = f"Led {i + 1} {led_status}"
        
        y = i * line_height + 8
        
        if i == cursor_pos:
            oled.text(cursor, 0, y)
            
        oled.text(text, 24, y)
        
    oled.show()
    

rot = Encoder(10, 11, 12)

leds = [Led(i) for i in led_pins]
num_leds = len(leds)
led_states = [False] * num_leds

button_push = 0

cursor = "->"
cursor_pos = 0


draw_menu()
while True:
    while rot.fifo.has_data():
        step = rot.fifo.get()
        
        if step == -1 or step == 1:
            cursor_pos += step
            
            if cursor_pos < 0:
                cursor_pos = num_leds - 1
            elif cursor_pos >= num_leds:
                cursor_pos = 0
                
        elif step == button_push:
            current_index = cursor_pos
            new_state = not led_states[current_index]
            led_states[current_index] = new_state
            
            if new_state:
                leds[current_index].on()
            else:
                leds[current_index].off()
                
        draw_menu()

    time.sleep_ms(50)
