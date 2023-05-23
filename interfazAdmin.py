from tkinter import *
from statistics import mean
import tkinter as tk
from ttkthemes import ThemedTk
from tkinter import messagebox
from tkinter import ttk
import threading
import time
import serial
import subprocess
import socket

IPSERVER  = "192.168.1.10"
PORTSERVER = 8000

def create_client(IP, port):
    # create socket object
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    global status_text
    # connect to the server
    try:
        client_socket.connect((IP, port))
        status_text.config(text = "Conexión establecida. Los sensores empezarán a funcionar y el programa se regulará automáticamente.")
    except socket.error:
        messagebox.showerror("Error", "No se pudo establecer la conexión con el servidor.")

def upload_code():
    # Logic to upload the code
    print("Uploading code...")
    create_client(IPSERVER, PORTSERVER)

def stop_execution():
    # Logic to stop the execution
    print("Execution stopped.")

def update_code(checkboxes):
    # Logic to update the code
    print("Updating code...")
    
    code = '''
from machine import Pin, PWM, ADC
import time
import dht

def changeColor(red, green, blue):
    red_pwm.duty(red)
    green_pwm.duty(green)
    blue_pwm.duty(blue)

def read_temperature(pins):
    temperatures = []
    for pin in pins:
        temp = pin.read()
        temperatures.append(temp)
    return temperatures

# Pines de termopar
termoparActive = Pin(18, Pin.OUT)
bombaPin1 = Pin(15, Pin.OUT)  # Bomba caliente
bombaPin2 = Pin(2, Pin.OUT)  # Bomba fría
placaPeltierPin1 = Pin(4, Pin.OUT)  # Peltier caliente
placaPeltierPin2 = Pin(16, Pin.OUT)  # Peltier fría
ventiladorPin = Pin(5, Pin.OUT)

# Pines de detección
buzzerPin = Pin(3, Pin.OUT)  # Detector de llama
flamePin = ADC(Pin(12))  # Pin ADC para detección de llama
smokeLED = Pin(21, Pin.OUT)  # LED de detección de humo
smokePin = ADC(Pin(13))  # Pin ADC para detección de humo

# Pines para el LED RGB
red_pin = Pin(1, Pin.OUT)
green_pin = Pin(22, Pin.OUT)
blue_pin = Pin(23, Pin.OUT)

# Pines de termopar
termopar_pins = [
    ADC(Pin(14)),  # Serpentin frio
    ADC(Pin(27)),  # Serpentin caliente
    ADC(Pin(25)),  # Peltier caliente
    ADC(Pin(26)),  # Peltier fria
    ADC(Pin(33)),  # Entrada
    ADC(Pin(32)),  # Salida
]

# Sensor DHT11
sensor = dht.DHT11(Pin(19))

# set up PWM objects for each pin
red_pwm = PWM(red_pin, freq=1000)
green_pwm = PWM(green_pin, freq=1000)
blue_pwm = PWM(blue_pin, freq=1000)

# set initial RGB values
red_value = 0
green_value = 0
blue_value = 0

# set the RGB values to turn on the LED to white
# red_value = 255
# green_value = 255
# blue_value = 255

# set the duty cycles for each pin
red_pwm.duty(red_value)
green_pwm.duty(green_value)
blue_pwm.duty(blue_value)
changeColor(0, 0, 255)

verde = False
blanco = True
apagado = False

while True:
    termoparActive.on()
    temperatures = read_temperature(termopar_pins)
    temperatureAverage = sum(temperatures) / len(temperatures)
    # read the analog voltage from the ADC pin
    flameVoltage = flamePin.read() / 1023 * 2.727
    if flameVoltage < 1.8:
        changeColor(255, 0, 0)
        buzzerPin.on()
    else:
        changeColor(0, 0, 255)
        buzzerPin.off()

    valuePPM = smokePin.read()
    if valuePPM > 1200:
        changeColor(255, 0, 255)
        smokeLED.on()
    else:
        changeColor(0, 0, 255)
        smokeLED.off()
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    temp_f = temp * (9/5) + 32.0
'''
    # Open the file in write mode ("w") to erase its contents
    with open("auxiliar.py", "w") as file:
        # Write your new code content to the file
        file.write(code)
        if checkboxes[0].get() == 1:
            file.write("\n\tventiladorPin.on()\n")
        else:
            file.write("\n\tventiladorPin.off()\n")
        if checkboxes[1].get() == 1:
            file.write("\n\tplacaPeltierPin1.on()\n")
        else:
            file.write("\n\tplacaPeltierPin1.off()\n")
        if checkboxes[2].get() == 1:
            file.write("\n\tplacaPeltierPin2.on()\n")
        else:
            file.write("\n\tplacaPeltierPin2.off()\n")
        if checkboxes[3].get() == 1:
            file.write("\n\tbombaPin1.on()\n")
        else:
            file.write("\n\tbombaPin1.off()\n")
        if checkboxes[4].get() == 1:
            file.write("\n\tbombaPin2.on()\n")
        else:
            file.write("\n\tbombaPin2.off()\n")
        
        if checkboxes[0].get() == 0 and checkboxes[1].get() == 1 and checkboxes[2].get() == 1 and checkboxes[3].get() == 0 and checkboxes[4].get() == 0:
           file.write("\n\tchangeColor(255, 255, 255)\n")
        elif checkboxes[0].get() == 1 and checkboxes[1].get() == 1 and checkboxes[2].get() == 1 and checkboxes[3].get() == 0 and checkboxes[4].get() == 0:
           file.write("\n\tchangeColor(0, 255, 0)\n")
        elif checkboxes[0].get() == 0 and checkboxes[1].get() == 0 and checkboxes[2].get() == 0 and checkboxes[3].get() == 0 and checkboxes[4].get() == 0:
            file.write("\n\tchangeColor(0, 0, 0)\n")

def emergencyStop(checkboxes):
    stop_execution()
    for check in checkboxes:
        check.set(0)
    update_code(checkboxes)

def show_temperature(temperatures):

    # Delete any existing temperature bar in the canvas
    canvas.delete("all")
    initial_x = 20
    initial_y = 300
    width = 50
    dif_x = 90
    i = 0

    for temp in temperatures:
        x1 = initial_x + dif_x * i
        x2 = x1 + width
        # Calculate the temperature bar height based on the temperature value
        bar_height = int((temp - 19) * 5)
        
        # Choose a color based on the temperature value
        if temp > 20 and temp <= 25:
            color_index = 0
        elif temp > 26 and temp <= 33:
            color_index = 1
        else:
            color_index = 2

        color = colors[color_index]
        
        # Draw the temperature bar
        canvas.create_rectangle(x1, initial_y - bar_height, x2, initial_y, fill=color)
        texto = textSensores[i] + " : " + str(int(temp)) + " °C"
        canvas.create_text(x1 + 25, 100, text = texto)
        i += 1
    
    average = sum(temperatures) / len(temperatures)
    average_text.config(text=f"Average Temperature: {average:.2f} °C")

textSensores = ["Sensor 1", "Sensor 2","Sensor 3", "Sensor 4", "Sensor 5", "Sensor 6", "Sensor 7", "Sensor 8"]
colors = ["blue", "orange", "red"]

# Create the main window
root = tk.Tk()
root.geometry("960x640")  # Set the window size to 960x740 pixels

# Create a frame to hold the checkboxes
checkbox_frame = tk.Frame(root)
checkbox_frame.pack(side=tk.LEFT, padx=20)

# Create the checkboxes
var_fans = tk.BooleanVar()
chk_fans = tk.Checkbutton(checkbox_frame, text="Ventiladores", variable=var_fans)

var_peltier_hot = tk.BooleanVar()
chk_peltier_hot = tk.Checkbutton(checkbox_frame, text="Peltier Caliente", variable=var_peltier_hot)

var_peltier_cold = tk.BooleanVar()
chk_peltier_cold = tk.Checkbutton(checkbox_frame, text="Peltier Fría", variable=var_peltier_cold)

var_cold_pump = tk.BooleanVar()
chk_cold_pump = tk.Checkbutton(checkbox_frame, text="Bomba Fría", variable=var_cold_pump)

var_hot_pump = tk.BooleanVar()
chk_hot_pump = tk.Checkbutton(checkbox_frame, text="Bomba Caliente", variable=var_hot_pump)

checkBoxList = [var_fans, var_peltier_hot, var_peltier_cold, var_hot_pump, var_cold_pump]

# Pack the checkboxes in the frame
chk_fans.pack(anchor=tk.W)
chk_peltier_hot.pack(anchor=tk.W)
chk_peltier_cold.pack(anchor=tk.W)
chk_hot_pump.pack(anchor=tk.W)
chk_cold_pump.pack(anchor=tk.W)
# Create a frame to hold the buttons
button_frame = tk.Frame(root)
button_frame.pack()

# Create the buttons
btn_upload = tk.Button(button_frame, text="Subir código", command=upload_code)
btn_stop = tk.Button(button_frame, text="Detener Ejecución", command=stop_execution)
btn_update = tk.Button(button_frame, text="Actualizar Código", command = lambda:update_code(checkBoxList))
btn_emergency = tk.Button(button_frame, text="Paro de emergencia", command = lambda:emergencyStop(checkBoxList))

# Pack the buttons in the frame with spacing
btn_upload.pack(pady=5)
btn_stop.pack(pady=5)
btn_update.pack(pady=5)
btn_emergency.pack(pady = 5)

# Create a canvas
canvas = tk.Canvas(root, width=750, height=350, bg="white")
canvas.pack(pady=20)

average_text = tk.Label(root, text="Average Temperature: ")
average_text.pack()

status_text = tk.Label(root, text = "Estado Actual: Sin actividad. Sube el código para empezar")
status_text.place(x = 50, y = 50)

client_socket = None

# Start the main event loop
root.mainloop()
