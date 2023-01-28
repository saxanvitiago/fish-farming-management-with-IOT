
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from machine import Pin
import time 
import dht


ancho =128
alto =64

# se crea el objeto y se inicializa la pantalla.
i2c = I2C(0,scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C (ancho, alto, i2c)

sensor = dht.DHT11(Pin(5))

while True:
    sensor.measure()
    print("Temp = "+str(sensor.temperature())+" Hum = "+str(sensor.humidity()))
   
    
    
    oled.text("Temp="+str(sensor.temperature())+" Hum ="+str(sensor.humidity()), 0, 0)
    
    
    oled.show()
    time.sleep(2)
    
   