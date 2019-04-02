#!/usr/bin/env python3
from ev3dev.ev3 import *
from time import sleep
motorD = LargeMotor('outB')
motorE = LargeMotor('outA')
motorD.run_forever(speed_sp=900)
motorE.run_forever(speed_sp=900)
sleep(5)
#fica 5 segundos andando e para "tirando o pé do acelerador"
motorD.stop(stop_action="coast")
motorE.stop(stop_action="coast")
