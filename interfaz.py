from tkinter import *
import tkinter as tk
from ttkthemes import ThemedTk
from tkinter import ttk
import threading
import time
import subprocess
import random
import socket

def stop_process(process, boton, label):
    process.kill()
    boton["state"] = tk.NORMAL
    label.config(text = "Presiona el botón para subir o actualizar el código al ESP32." )

def actualizarCodigo(controladores):
    
    archivoCodigo = open("./code.py", "w")
    
    if controladores[0].get() == 0:
        tiempo = 0.5
    else:
        tiempo = 2

    codigo = f"from machine import Pin\nimport time\nrelay_pin_2 = Pin(2, Pin.OUT)\nwhile True:\n\trelay_pin_2.value(1)\n\ttime.sleep({tiempo})\n\trelay_pin_2.value(0)\n\ttime.sleep({tiempo})"

    archivoCodigo.write(codigo)

def upload_code():
    command = "ampy --port COM4 run code.py"
    botonSubirCodigo["state"] = tk.DISABLED
    botonDetenerCodigo["state"] = tk.DISABLED

    procesoCodigo = subprocess.Popen(command)
    botonDetenerCodigo.configure(command=lambda: stop_process(procesoCodigo, botonSubirCodigo, labelCodigo))

    def wait_upload_code():
        time.sleep(16)
        labelCodigo.config(text="Código subido correctamente. En cuanto quieras actualizar o detener el código, pulsa el botón.")
        botonDetenerCodigo["state"] = tk.NORMAL

    thread = threading.Thread(target=wait_upload_code)
    thread.start()


def generateTemperature():
    minTemp = 20
    maxTemp = 40
    diff = maxTemp - minTemp
    temperatures = []
    
    for i in range(0, 8):
        temperature = minTemp + random.random() * diff
        temperatures.append(temperature)

    return temperatures

def update_temperature(temperatures):

    # Delete any existing temperature bar in the canvas
    myCanvas.delete("all")
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
        myCanvas.create_rectangle(x1, initial_y - bar_height, x2, initial_y, fill=color)
        texto = textSensores[i] + " : " + str(int(temp)) + " °C"
        myCanvas.create_text(x1 + 25, 100, text = texto)
        i += 1
    
    # Schedule the next temperature update in 1 second
    root.after(500, func = lambda: update_temperature(generateTemperature()))

def create_client():
    host = '192.168.1.9'
    port = 8000

    # create socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to the server
    client_socket.connect((host, port))
    print("Connected to server")

    # send two numbers to the server
    client_socket.sendall("10,20".encode())

    # receive the sum from the server
    result = client_socket.recv(1024).decode()
    print("The sum is: ", result)

#ranges 
#20 - 25 : blue
#26 - 33 : orange
#34 - 40 : red
create_client()
colors = ["blue", "orange", "red"]
textSensores = ["Sensor 1", "Sensor 2","Sensor 3", "Sensor 4", "Sensor 5", "Sensor 6", "Sensor 7", "Sensor 8"]
root = ThemedTk(theme="blue")
style = ttk.Style(root)
root.geometry("960x740")
stop_event = threading.Event()
root.title("Interfaz Gráfica del aire acondicionado")
labelCodigo = tk.Label(root, text="Presiona el botón para subir o actualizar el código al ESP32.")
labelCodigo.pack(pady=10)

botonSubirCodigo = ttk.Button(root, text="Subir código", command=upload_code)
botonSubirCodigo.pack(pady = 10)
botonDetenerCodigo = ttk.Button(root, text="Detener ejecución", state="disabled")
botonDetenerCodigo.pack(pady=10)
botonActualizarCodigo = ttk.Button(root, text="Actualizar código", command = lambda: actualizarCodigo(controladores))
botonActualizarCodigo.pack(pady = 10)

ventiladorFrio1 = IntVar()
ventiladorFrio2 = IntVar()
ventiladorCaliente1 = IntVar()
ventiladorCaliente2 = IntVar()
bombaFrioM = IntVar()
bombaCalienteM = IntVar()
bombaFrioHVAC = IntVar()
bombaCalienteHVAC = IntVar()
peltier1 = IntVar()
peltier2 = IntVar()
ventiladorEmergencia = IntVar()
ventiladorInyeccion = IntVar()

controladores = [ventiladorFrio1, ventiladorFrio2, ventiladorCaliente1, ventiladorCaliente2, bombaFrioM, bombaCalienteM, bombaFrioHVAC, bombaCalienteHVAC, peltier1, peltier2, ventiladorEmergencia, ventiladorInyeccion]

checkVentiladorFrio1 = Checkbutton(text="Ventilador Frio 1", variable=ventiladorFrio1, onvalue=1, offvalue=0)
checkVentiladorFrio1.place(x=10, y=10)

checkVentiladorFrio2 = Checkbutton(text="Ventilador Frio 2", variable=ventiladorFrio2, onvalue=1, offvalue=0)
checkVentiladorFrio2.place(x=10, y=35)

checkVentiladorCaliente1 = Checkbutton(text="Ventilador Caliente 1", variable=ventiladorCaliente1, onvalue=1, offvalue=0)
checkVentiladorCaliente1.place(x=10, y=60)

checkVentiladorCaliente2 = Checkbutton(text="Ventilador Caliente 2", variable=ventiladorCaliente2, onvalue=1, offvalue=0)
checkVentiladorCaliente2.place(x=10, y=85)

checkBombaFrioM = Checkbutton(text="Bomba Frio M", variable=bombaFrioM, onvalue=1, offvalue=0)
checkBombaFrioM.place(x=10, y=110)

checkBombaCalienteM = Checkbutton(text="Bomba Caliente M", variable=bombaCalienteM, onvalue=1, offvalue=0)
checkBombaCalienteM.place(x=10, y=135)

checkBombaFrioHVAC = Checkbutton(text="Bomba Frio HVAC", variable=bombaFrioHVAC, onvalue=1, offvalue=0)
checkBombaFrioHVAC.place(x=10, y=160)

checkBombaCalienteHVAC = Checkbutton(text="Bomba Caliente HVAC", variable=bombaCalienteHVAC, onvalue=1, offvalue=0)
checkBombaCalienteHVAC.place(x=10, y=185)

checkPeltier1 = Checkbutton(text="Peltier 1", variable=peltier1, onvalue=1, offvalue=0)
checkPeltier1.place(x=10, y=210)

checkPeltier2 = Checkbutton(text="Peltier 2", variable=peltier2, onvalue=1, offvalue=0)
checkPeltier2.place(x=10, y=235)

checkVentiladorEmergencia = Checkbutton(text="Ventilador Emergencia", variable=ventiladorEmergencia, onvalue=1, offvalue=0)
checkVentiladorEmergencia.place(x=10, y=260)

checkVentiladorInyeccion = Checkbutton(text="Ventilador Inyeccion", variable=ventiladorInyeccion, onvalue=1, offvalue=0)
checkVentiladorInyeccion.place(x=10, y=285)

gas_detection_label = Label(root, text="Detección de gas: ")
gas_detection_label.place(x=800, y=10)

gas_detection = IntVar()
gas_detection.set(0)

rb_gas_off = Radiobutton(root, text="No Detectado", variable=gas_detection, value=0, state="disabled")
rb_gas_off.place(x=800, y=30)

rb_gas_on = Radiobutton(root, text="Detectado", variable=gas_detection, value=1, state="disabled")
rb_gas_on.place(x=800, y=50)

flame_detection_label = Label(root, text="Detección de flama: ")
flame_detection_label.place(x=800, y=70)

flame_detection = IntVar()
flame_detection.set(0)

rb_flame_off = Radiobutton(root, text="No Detectado", variable=flame_detection, value=0, state="disabled")
rb_flame_off.place(x=800, y=90)

rb_flame_on = Radiobutton(root, text="Detectado", variable=flame_detection, value=1, state="disabled")
rb_flame_on.place(x=800, y=110)


myCanvas = tk.Canvas(root, bg="white", height=300, width=750)
myCanvas.pack(side = LEFT)
update_temperature(generateTemperature())
root.mainloop()