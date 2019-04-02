#!/usr/bin/env python3
from ev3dev.ev3 import *
from time import sleep
motorD = LargeMotor('outB')
motorE = LargeMotor('outA')
motorD.run_timed(time_sp=1000,speed_sp=900)
motorE.run_timed(time_sp=1000,speed_sp=900)
