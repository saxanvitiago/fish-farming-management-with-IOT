import machine
import time

#se crean los objetos
trig_pin = machine.Pin(18, machine.Pin.OUT)
echo_pin = machine.Pin(19, machine.Pin.IN)
