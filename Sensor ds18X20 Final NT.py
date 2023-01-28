#programa diseñado por Angela Rico y Javier Cristancho
#Importamos módulos

from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time
import onewire
import ds18x20


ancho =128
alto =64

# se crea el objeto y se inicializa la pantalla.
i2c = I2C(0,scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C (ancho, alto, i2c)

#se crean los objetos y se inicializa el sensor.
dat = Pin(4)
ds = ds18x20.DS18X20(onewire.OneWire(dat))


while True:
    # Escanear los dispositivo
    roms = ds.scan() 
    ds.convert_temp()
    time.sleep_ms(750)
    # Obtener la temperatura
    temp = ds.read_temp(roms[0])
   
    #Inicializar la pantalla
    oled.fill(0)
    oled.text("Temp: {}°C".format(temp), 0, 0)
    
    
   # Comprobar la temperatura contra los límites de alerta
    if temp > 32:
        oled.text("   !Alerta¡", 0, 16)
        oled.text("   Temp Alta",     0, 32)
        print("Temperatura: {}°C, \n !Alerta¡ esta muy alta.".format(temp))
       
    elif temp < 23:
        oled.text("   !Alerta¡", 0, 16)
        oled.text("   Temp Baja", 0, 32)
        print("Temperatura: {}°C, !Alerta¡ esta muy Baja.".format(temp))
        
    else:
        oled.text("  Temp Optima", 0, 16)
        oled.text("      :)     ", 0, 32)
        print("La temperatura {}°C Temperatura optima.".format(temp))
    # Mostrar la pantalla    
    oled.show()
        
    # Esperar antes de volver a leer la temperatura
    time.sleep(2)