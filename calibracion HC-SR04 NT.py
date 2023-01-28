#programa diseñado por Angela Rico y Javier Cristancho
#Importamos módul

import machine
import time

#se crean los objetos
trig_pin = machine.Pin(18, machine.Pin.OUT)
echo_pin = machine.Pin(19, machine.Pin.IN)

#Valores de referencia para calibrar el sensor
ref_values = [10, 15, 20,]

#Función para calibrar el sensor
def calibrate_sensor():
    print("Iniciando calibración del sensor...")
    for value in ref_values:
        print("Coloque un objeto a una distancia de ", value, "cm del sensor y presione Enter.")
        input()
        # Enviar un pulso de trigger
        trig_pin.value(1)
        time.sleep_us(10)
        trig_pin.value(0)

        # Medir el tiempo de echo
        while echo_pin.value() == 0:
            pass
        start = time.ticks_us()
        while echo_pin.value() == 1:
            pass
        end = time.ticks_us()
        duration = time.ticks_diff(end, start)
        distance = duration * 0.276
        print("Lectura del sensor: {:.2f} cm".format(distance))
        print("Ajuste el valor del sensor si es necesario.")
        input()
    print("Calibración completada.")

calibrate_sensor()