#!/usr/bin/env python3
from ev3dev.ev3 import *
from time import sleep
import math

def odometria(dCentro, rRoda):
    C = 2 * math.pi * dCentro
    c = 2 * math.pi * rRoda
    return C/c

motorD = LargeMotor('outB')
motorE = LargeMotor('outA')

dCentro = 5.5
rRoda = 3
razaoRobo = odometria(dCentro, rRoda)

i = 1
while(i<=4):
    motorD.run_timed(time_sp=1000,speed_sp=1000,stop_action="brake")
    motorE.run_timed(time_sp=1000,speed_sp=1000,stop_action="brake")
    sleep(1)
    motorD.run_to_rel_pos(position_sp=(razaoRobo*90),speed_sp=900)
    motorE.run_to_rel_pos(position_sp=-(razaoRobo*90),speed_sp=900)
    sleep(1)
    i = i + 1

motorD.stop(stop_action="brake")
motorE.stop(stop_action="brake")
