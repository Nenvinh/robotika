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
left_motor = Motor(Port.D)
right_motor = Motor(Port.C)
gate_motor = Motor(Port.A)

# senzory
ultra = UltrasonicSensor(Port.S1)
#color_sensor = ColorSensor(Port.S2)
gyro = GyroSensor(Port.S3)
tlacitko = TouchSensor(Port.S2)


robot = DriveBase(left_motor, right_motor, 56, 145)
gyro.reset_angle(0)


# Write your program here.
ev3.speaker.beep()

def diagnostika(data[]):
    for angle, distance in data:
        ev3.speaker.print("Uhel:", angle, "Vzdalenost:", distance)
    

def choose_color():
    colors = [
        (Color.RED, "CERVENA"),
        (Color.GREEN, "ZELENA"),
        (Color.BLUE, "MODRA"),
        (Color.YELLOW, "ZLUTÁ")
    ]
    i = 0
    while True:
        #ev3.screen.clear()
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

def radar():
    distance = ultra.distance()
    angle = abs(gyro.angle())

    if(distance <= 255):
        data.append((angle, distance))



def turn_360_on_spot(speed=200):
    gyro.reset_angle(0)

    left_motor.run(speed)
    right_motor.run(-speed)

    next_stop = 24  # první zastavení na 24°
    stop_counter = 0
    while abs(gyro.angle()) < 360:
        angle = abs(gyro.angle())
        ev3.screen.print(stop_counter)
        ev3.screen.print(angle)
        # pokud jsme dosáhli dalšího milníku
        if angle >= next_stop:
            left_motor.stop()
            right_motor.stop()
            radar()
            wait(2000)  # pauza 2 sekundy
            stop_counter = stop_counter + 1
            # znovu rozjet
            left_motor.run(speed)
            right_motor.run(-speed)

            next_stop += 20  # další zastávka (40, 60, ...)

        wait(10)

    left_motor.stop()
    right_motor.stop()

# Hlavní program
data = []
TARGET_COLOR = choose_color()
ev3.screen.print("Hledaná barva: ")
ev3.screen.print(TARGET_COLOR)
turn_360_on_spot()
