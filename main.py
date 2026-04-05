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
ultra = UltrasonicSensor(Port.S4)
color_sensor = ColorSensor(Port.S1)
gyro = GyroSensor(Port.S3)
tlacitko = TouchSensor(Port.S2)


robot = DriveBase(left_motor, right_motor, 56, 145)
gyro.reset_angle(0)


# Write your program here.
ev3.speaker.beep()


def diagnostika(data):
    i = 1
    for angle, distance in data:
        ev3.screen.print(i)
        ev3.screen.print("Vzdalenost:", distance)
        ev3.screen.print("Uhel:", angle)
        i += 1
        wait(5000)
    
    i = 1
    for y_axis, x_axis in coordinates:
        ev3.screen.print(i)
        ev3.screen.print("Y AXIS: ", y_axis)
        ev3.screen.print("X AXIS: ", x_axis)
        i += 1
        wait(5000)

    
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

    if(distance <= 2550):
        data.append((angle, distance))
        return data
    else:
        ev3.screen.print("Zadny blok")
        wait(5000)


def is_correct(TARGET_COLOR):
    colour = color_sensor.color()
    if (colour == TARGET_COLOR):
        gate_motor.run(100)
        return True
    else:
        return False


def turn_360_on_spot(speed=200):
    gyro.reset_angle(0)

    left_motor.run(speed)
    right_motor.run(-speed)

    next_stop = 30  # první zastavení na 30°
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
            next_stop += 30  # další zastávka (60, 90, ...)
        wait(1000)
    
    gyro.reset_angle(0)
    ev3.screen.print("Dokonceno:")
    ev3.screen.print("otaceni")
    left_motor.stop()
    right_motor.stop()

#new stuff
def calculation(data):
    for angle, distance in data:
        if(angle % 90 == 0):
            y_axis = distance
            x_axis = 0
            coordinates.append((y_axis, x_axis))
            return coordinates
        else:
            rad = math.radians(angle)
            y_axis = math.cos(rad) * dist
            x_axis = math.sin(rad) * dist
            coordinates.append((y_axis, x_axis))
            return coordinates


def go_to_blocks(coordinates):
    for y_axis, x_axis in coordinates:
        robot.straight(y_axis)
        if(x_axis != 0):
            robot.turn(90)
        robot.straight(x_axis)
        gyro.reset_angle(0)
        if(is_correct(TARGET_COLOR) == True):
            robot.straight(-x_axis)
            robot.turn(-90)
            robot.straight(-y_axis)
        else:
            robot.straight(-x_axis)
            robot.turn(-90)
            robot.straight(-y_axis)
            gyro.reset_angle(0)
            robot.turn(90)


# Hlavní program

data = []
coordinates = []
TARGET_COLOR = choose_color()
ev3.screen.print("Hledaná barva: ")
ev3.screen.print(TARGET_COLOR)
wait(5000)
turn_360_on_spot()
diagnostika(data)
wait(5000)

#new stuff untested
calculation(data)
diagnostika(coordinates)
wait(5000)
go_to_blocks(coordinates)

gate_motor.run(100)
wait(5000)



'''
Dear programmer:
When I wrote this code, only god and
I knew how it worked.
Now, only god knows it!
 
Therefore, if you are trying to optimize
this routine and it fails (most surely),
please increase this counter as a
warning for the next person(e.i. me):

total hours wasted here = 

23. 3. 2026 - 1.5h
24. 3. 2026 - 2h (hodina robotiky)
27. 3. 2026 - 0.5h
30. 3. 2026 - 2h
31. 3. 2026 - 2h (hodina robotiky)
3. 4. 2026 - 4h
4. 4. 2026 - 0.5h

Praise the omnissiah:
01110000 01110010 01100001 01101001 01110011 01100101 00100000 01110100 01101000 01100101 00100000 01101111 01101101 01101110 01101001 01110011 01110011 01101001 01100001 01101000
'''