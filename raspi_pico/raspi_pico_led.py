from machine import Pin, Timer, ADC
import utime

class Pico(object):
    def __init__(self):
        self.led_pini = Pin(25, Pin.OUT)
        self.zamanlayici = Timer()
        
    def sicaklik_sensoru_ayarla(self):
        self.sicaklik_sensoru = ADC(4)
    
    def zamanlayiciyi_ayarla(self, frekans, mod, cb):
        self.zamanlayici.init(freq=frekans, mode=mod, callback=cb)
        
    def zamanlayiciyi_durdur(self):
        self.zamanlayici.deinit()
        
    def led_yaksöndür(self, zamanlayici):
        self.led_pini.toggle()
        
    def celcius_oku(self):
        #Referans:
        #https://github.com/raspberrypi/pico-micropython-examples/blob/master/adc/temperature.py
        ham_deger = self.sicaklik_sensoru.read_u16() * 3.3 / (65535)
        
        return 27 - (ham_deger - 0.706)/0.001721
        
pico = Pico()
pico.zamanlayiciyi_ayarla(2, Timer.PERIODIC, pico.led_yaksöndür)
pico.sicaklik_sensoru_ayarla()

while True:
    sicaklik = pico.celcius_oku()
    
    print(sicaklik)
    
    utime.sleep(2)
