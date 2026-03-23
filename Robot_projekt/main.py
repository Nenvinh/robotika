#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import math

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()

# motory
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
radar_motor = Motor(Port.A)

# senzory
ultra = UltrasonicSensor(Port.S1)
color_sensor = ColorSensor(Port.S2)
gyro = GyroSensor(Port.S3)


robot = DriveBase(left_motor, right_motor, 56, 120)
gyro.reset_angle(0)


# Write your program here.
ev3.speaker.beep()

def choose_color():
    colors = [
        (Color.RED, "CERVENA"),
        (Color.GREEN, "ZELENA"),
        (Color.BLUE, "MODRA"),
        (Color.BLACK, "CERNA")
    ]
    i = 0
    while True:
        ev3.screen.clear()
        ev3.screen.print(colors[i][1])
        b = ev3.buttons.pressed()
        if Button.LEFT in b:
            i = (i - 1) % len(colors)
            wait(300)
        if Button.RIGHT in b:
            i = (i + 1) % len(colors)
            wait(300)
        if Button.CENTER in b:
            ev3.speaker.beep()
            return colors[i][0]

TARGET_COLOR = choose_color()

def radar():


def turn_360_on_spot(speed=200):
    # reset gyra
    gyro.reset_angle(0)

    # rozjeti motoru (tank otaceni)
    left_motor.run(-speed)
    right_motor.run(speed)

    # cekani dokud nedosahneme 360°
    while abs(gyro.angle()) < 360:
        wait(10)

    # zastaveni motoru
    left_motor.stop()
    right_motor.stop()

# Hlavní program

turn_360_on_spot()
