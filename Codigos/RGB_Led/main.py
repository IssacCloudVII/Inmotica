import time

from machine import Pin, PWM

# set up the pins for the RGB LED
red_pin = Pin(32, Pin.OUT)
green_pin = Pin(33, Pin.OUT)
blue_pin = Pin(2, Pin.OUT)

# set up PWM objects for each pin
red_pwm = PWM(red_pin, freq=1000)
green_pwm = PWM(green_pin, freq=1000)
blue_pwm = PWM(blue_pin, freq=1000)

# set initial RGB values
red_value = 0
green_value = 0
blue_value = 0

# set the RGB values to turn on the LED to white
#red_value = 255
#green_value = 255
#blue_value = 255

# set the duty cycles for each pin
red_pwm.duty(red_value)
green_pwm.duty(green_value)
blue_pwm.duty(blue_value)
tEspera = 3

while True:
    #Color rojo
    red_pwm.duty(255)
    green_pwm.duty(0)
    blue_pwm.duty(0)
    time.sleep(tEspera)
    #Color azul
    red_pwm.duty(0)
    green_pwm.duty(0)
    blue_pwm.duty(255)
    time.sleep(tEspera)
    #Color verde
    red_pwm.duty(0)
    green_pwm.duty(255)
    blue_pwm.duty(0)
    time.sleep(tEspera)
    #Color morado
    red_pwm.duty(100)
    green_pwm.duty(0)
    blue_pwm.duty(140)
    time.sleep(tEspera)
    #Color blanco
    red_pwm.duty(255)
    green_pwm.duty(255)
    blue_pwm.duty(255)
    time.sleep(tEspera)