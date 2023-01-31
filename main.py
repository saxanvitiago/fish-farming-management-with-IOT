#programa diseñado por Angela Rico y Javier Cristancho
#_____________Importamos módulos___________________
from machine import Pin, I2C ,ADC
from ssd1306 import SSD1306_I2C
import time 
import onewire
import ds18x20
from hcsr04 import HCSR04
from time import sleep
import network, time, urequests
#_____________Objetos_____________________________
# se crea el objeto y se inicializa la pantalla.
ancho =128
alto =64

i2c = I2C(0,scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C (ancho, alto, i2c)

#se crean los objetos y se inicializa el sensor temperatura
dat = Pin(4)
ds = ds18x20.DS18X20(onewire.OneWire(dat))

# Crear objeto para el sensor de turbidez
sensor_pin = ADC(Pin(32))
sensor_pin.atten(ADC.ATTN_11DB)
# Configurar el límite de turbidez
turbidity_limit = 100

# Crear objeto para el sensor de distancia
hcsr04 = HCSR04(trigger_pin= 13, echo_pin=12)

# Crear objeto para el caudalimetro
sensor_pin = ADC(Pin(26))
sensor_pin.atten(ADC.ATTN_11DB)
# Configurar el límite de caudal
flow_limit = 4000



def conectaWifi (red, password):
      global miRed
      miRed = network.WLAN(network.STA_IF)     
      if not miRed.isconnected():              #Si no está conectado…
          miRed.active(True)                   #activa la interface
          miRed.connect(red, password)         #Intenta conectar con la red
          print('Conectando a la red', red +"…")
          timeout = time.time ()
          while not miRed.isconnected():           #Mientras no se conecte..
              if (time.ticks_diff (time.time (), timeout) > 10):
                  return False
      return True




if conectaWifi ("SALP-SEM", "860533206"):

    print ("Conexión exitosa!")
    print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())
     
    url_2= "https://maker.ifttt.com/trigger/Alerta_Estanque/with/key/d0qUQL0-_qUEqCycNe-a7k-cunknvvhOnmmaCypErGd" # url de ifttt 
    url = "https://api.thingspeak.com/update?api_key=C759FG3BO4HR33X2" # url de thingspeak

while True:
    # Escanear los dispositivo
    roms = ds.scan() 
    ds.convert_temp()
    time.sleep_ms(750)
    # Obtener la temperatura
    temp = ds.read_temp(roms[0])
   
            # Comprobar la temperatura contra los límites de alerta
    if temp > 32:   
        print("Temperatura: {}°C, \n !Alerta¡ esta muy alta.".format(temp))  
    elif temp < 23:   
        print("Temperatura: {}°C, !Alerta¡ esta muy Baja.".format(temp))  
    else:
        print("La temperatura {}°C Temperatura optima.".format(temp))
     
        respuesta = urequests.get(url_2+"&value1="+str(temp))
        print(respuesta.text)
        print(respuesta.status_code)
        respuesta.close ()
               
          # Leer la turbidez actual
    turbidity = sensor_pin.read()
    print("Turbidez actual: {}".format(turbidity))
    
                                                                                                                                                                        
    # Comprobar si la turbidez supera el límite
    if turbidity > turbidity_limit:
        print("Turbidez excedida! ")
    else:
        print("Turbidez normal.")
    
    
    try:    
        distance = hcsr04.distance_cm()
        print("Nivel Estanque:", distance, "cm")
        
    except:
        print ("Error!")
        
      # Leer el caudal actual
    flow = sensor_pin.read()
    print("Caudal actual: {} L/min".format(flow))

 
    # Comprobar si el caudal es menor al limite
    if flow <= flow_limit:
        print("Caudal bajo!. Peligro...")
    else:
        print("Caudal normal.")
         
    envio_thingspeak = urequests.get(url+"&field1="+str(temp)+"&field2="+str(flow)+"&field3="+str(distance)+"&field4="+str(turbidity))      
    print(envio_thingspeak.text, envio_thingspeak.status_code)
    envio_thingspeak.close ()
         
        
        
    oled.fill(0)
    oled.text("Estado del Estanque", 0, 0)
    oled.text("Temperatura:{}°C,".format(temp), 0, 20)
    if temp < 23 or temp > 32:
        oled.text("ALERTA TEMP!".format(temp), 0, 10)
    oled.text("Caudal: {} L/min".format(flow), 0, 30)
    if flow <=0:
        oled.text("ALERTA CAUDAL!".format(temp), 0, 10)
    oled.text("Nivel Agua: " + str(distance) + " cm", 0, 40)
    if flow >1:
        oled.text("ALERTA NIVEL!".format(temp), 0, 10)
    oled.text("Turbidez:{}".format(turbidity), 0, 50)
    if turbidity > 1000:
        oled.text("ALERTA TURBIDEZ!".format(temp), 0, 10)
    # Mostrar la pantalla    
    oled.show()
        
    # Esperar antes de volver a leer la temperatura
    time.sleep(2)
