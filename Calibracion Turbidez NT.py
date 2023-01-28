#programa diseñado por Angela Rico y Javier Cristancho
#Importamos módulos

import machine
import time

pin_sensor = machine.Pin(35, machine.Pin.IN) #Configura el pin 32 como entrada
pin_gnd = machine.Pin(33 , machine.Pin.OUT) #Configura el pin 35 como salida

#Valores de referencia para calibrar el sensor
ref_values = [100, 50, 20, 10, 5]

#Función para calibrar el sensor
def calibrate_sensor():
    print("Iniciando calibración del sensor...")
    for value in ref_values:
        print("Coloque el sensor en una solución con una turbidez de", value, "NTU y presione Enter.")
        input()
        reading = pin_sensor.value()
        print("Lectura del sensor:", reading)
        print("Ajuste el valor del sensor si es necesario.")
        input()
    print("Calibración completada.")

calibrate_sensor()