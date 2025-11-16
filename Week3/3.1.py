from machine import Pin
from fifo import Fifo
from led import Led
import micropython
import time


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
        

led = Led(22)
brightness = 50

is_led_on = False

button_push = 0
rot = Encoder(10, 11, 12)


led.off()
while True:
    while rot.fifo.has_data():
        step = rot.fifo.get()
        
        if step == button_push:
            is_led_on = not is_led_on
            
            if is_led_on:
                led.brightness(brightness)
                led.on()
            else:
                led.off()
                
        elif step == 1 or step == -1: 
            
            brightness += step * 5
            
            if brightness < 0:
                brightness = 0
            elif brightness > 100:
                brightness = 100
            
            if is_led_on:
                led.brightness(brightness)
