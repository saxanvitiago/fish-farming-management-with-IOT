#programa diseñado por Angela Rico y Javier Cristancho
#Importamos módulos

from machine import Pin, ADC
import time
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C


ancho =128
alto =64

# se crea el objeto y se inicializa la pantalla.
i2c = I2C(0,scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C (ancho, alto, i2c)
# Crear objeto para el sensor de turbidez
sensor_pin = ADC(Pin(35))
sensor_pin.atten(ADC.ATTN_11DB)


# Configurar el límite de turbidez
turbidity_limit = 1

while True:
    # Leer la turbidez actual
    turbidity = sensor_pin.read()
    print("Turbidez actual: {}".format(turbidity))
    
    oled.fill(0)
    oled.text("   Turbidez:{}".format(turbidity), 0, 0)

    # Comprobar si la turbidez supera el límite
    if turbidity > turbidity_limit:
        oled.text("!!!!Alerta¡¡¡", 0, 16)
        print("Turbidez excedida! ")
        
    else:
        oled.text("     Normal ", 0, 16)
        print("Turbidez normal.")
        
        # Mostrar la pantalla    
    oled.show()
        
    # Esperar antes de volver a leer la turbidez
    time.sleep(.50)