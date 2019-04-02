#!/usr/bin/env python3
from ev3dev.ev3 import *
from time import sleep
motorD = LargeMotor('outB')
motorE = LargeMotor('outA')
motorD.run_to_rel_pos(position_sp=360,speed_sp=900)
motorE.run_to_rel_pos(position_sp=360,speed_sp=900)
