#!/usr/bin/env python3

from ev3dev.ev3 import *
from time import sleep

us = UltrasonicSensor()
us.mode='US-DIST-CM'
units = us.units

Leds.all_off()

while True:
    distancia = us.value()/10  # converte mm to cm/10
    print(distancia)

    vermelho = 1/((distancia/5)**2)

    if(distancia > 30):
        vermelho = 0

    Leds.set_color(Leds.LEFT, (vermelho,1,0))
    sleep(0.01)
    Leds.set_color(Leds.RIGHT, (vermelho,1,0))
    sleep(0.01)

