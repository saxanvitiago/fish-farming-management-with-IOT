#programa diseñado por Angela Rico y Javier Cristancho
#Importamos módulos
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from machine import Pin, ADC
import time
import machine

ancho =128
alto =64

# se crea el objeto y se inicializa la pantalla.
i2c = I2C(0,scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C (ancho, alto, i2c)



# Crear objetos
sensor_pin = ADC(Pin(26))
sensor_pin.atten(ADC.ATTN_11DB)




# Configurar el límite de caudal
flow_limit = 30

while True:
    # Leer el caudal actual
    flow = sensor_pin.read()
    print("Caudal actual: {} L/min".format(flow))

 #Inicializar la pantalla
    oled.fill(0)
    oled.text("Caudal {}L/min".format(flow), 0, 0)



    # Comprobar si el caudal es menor al limite
    if flow <= flow_limit:
        oled.text("   !Alerta¡", 0, 16)
        oled.text("  Caudal Bajo",     0, 32)
        print("Caudal bajo!. Peligro...")
        
    else:
        print("Caudal normal.")
        
    oled.show()
    # Esperar antes de volver a leer el caudal
    time.sleep(1)