
import serial
import io

import time as t

from ursina import *

app = Ursina()

class Oyuncu(Entity):
    def __init__(self, ser,  position = Vec3(0,0,0)):
        super().__init__()
        self.position = position
        self.velocity = Vec3(0, 0, 0)
        self.model='cube'
        self.color = color.blue
        self.scale_y = 1
        self.scale_x = 5
        self.serial = ser
        
    def __del__(self):
        self.serial.close()
        
    def update(self): 
        
        pico_girdisi = 0
        try:
            state=self.serial.readline()
        
            pico_girdisi = int(state)
            
            print(pico_girdisi)
        except Exception as e:
            print(e)
            
            pico_girdisi = 0
        
        #self.velocity += Vec3(0, -1 * time.dt +  (+2*held_keys['w'] * time.dt), 0) 
        
        self.velocity += Vec3(0, -1 * time.dt +  (+2*pico_girdisi * time.dt), 0) 
        
        self.position += self.velocity * time.dt
    


ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0.01)

#documentation of pyserial
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

t.sleep(1)

# Başlangı. pozisyonu
oyuncu_01 = Oyuncu(sio, Vec3(0,5,0))

app.run()