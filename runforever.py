#!/usr/bin/env python3
from ev3dev.ev3 import *
from time import sleep
motorD = LargeMotor('outB')
motorE = LargeMotor('outA')
#Anda pra sempre com velocidade 900 do motor
motorD.run_forever(speed_sp=900)
motorE.run_forever(speed_sp=900)
sleep(5)
motorD.stop(stop_action="hold")
motorE.stop(stop_action="hold")



